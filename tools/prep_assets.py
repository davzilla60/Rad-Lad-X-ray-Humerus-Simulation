"""Prepare the humerus X-ray assets from the originals in assets/src (run from inside assets/).
   Both films are resampled onto ONE canonical "arm frame" (mm, AP-film orientation: patient's right on the
   viewer's left) so the simulator can show either film for any set-up:
     - AP (stock, source not stated): greyscale; pixel spacing ESTIMATED at 0.2 mm/px from humeral length.
     - Lateral (FracAtlas, CC BY 4.0): corner mark and the flat grey redaction block inpainted, then a similarity
       transform maps its humeral head top / distal humerus onto the AP's.
   The canvas is extended beyond each real film with a progressively blurred synthetic margin."""
import cv2, numpy as np, json

MM = 0.25                       # canvas mm per px
X0, Y0, WMM, HMM = -120, -80, 440, 560
W, H = round(WMM/MM), round(HMM/MM)
AP_MMPP = 0.2                   # estimated

# landmarks: humeral head top, distal humerus (articular end) - source px
AP_LM  = np.float32([[690, 340], [430, 1890]])
LAT_LM = np.float32([[241, 10], [170, 339]])

def sim_from(src, dst):
    """similarity (scale+rot+shift) taking 2 src points to 2 dst points; returns 2x3"""
    s0, s1 = src; d0, d1 = dst
    vs, vd = s1 - s0, d1 - d0
    k = np.linalg.norm(vd)/np.linalg.norm(vs)
    a = np.arctan2(vd[1], vd[0]) - np.arctan2(vs[1], vs[0])
    c, s = k*np.cos(a), k*np.sin(a)
    R = np.float32([[c, -s], [s, c]])
    t = d0 - R @ s0
    return np.hstack([R, t[:, None]]).astype(np.float32), k, np.degrees(a)

def to_canvas(M_mm):
    """compose src->mm with mm->canvas px"""
    C = np.float32([[1/MM, 0, -X0/MM], [0, 1/MM, -Y0/MM], [0, 0, 1]])
    return (C @ np.vstack([M_mm, [0, 0, 1]]))[:2]

def extend(img, M, trim):
    """warp img onto the canvas; outside the real film, blend in a blurred edge-replicate"""
    core = img[trim:-trim, trim:-trim].astype(np.float32)
    Mc = M.copy(); Mc[:, 2] += M[:, :2] @ np.float32([trim, trim])
    ext = cv2.warpAffine(core, Mc, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    mask = cv2.warpAffine(np.ones(core.shape, np.uint8), Mc, (W, H), flags=cv2.INTER_NEAREST, borderValue=0)
    d = cv2.distanceTransform((1 - mask).astype(np.uint8), cv2.DIST_L2, 5)     # px outside the film
    out = ext.copy()
    for s in (6, 16, 36, 70):
        b = cv2.GaussianBlur(ext, (0, 0), s)
        w = np.clip(d/(s*5.0), 0, 1)
        out = out*(1 - w) + b*w
    out = out*(1 - 0.18*np.clip(d/320, 0, 1))
    out += np.random.default_rng(5).normal(0, 2.0, out.shape)*np.clip(d/40, 0, 1)
    return np.clip(out, 0, 255).astype(np.uint8), mask

# ---- AP ----
ap = cv2.imread("src/ap.jpg").astype(np.float32).mean(axis=2)
M_ap_mm = np.float32([[AP_MMPP, 0, 0], [0, AP_MMPP, 0]])
ap_x, ap_m = extend(ap, to_canvas(M_ap_mm), 3)
cv2.imwrite("ap_x.jpg", ap_x, [cv2.IMWRITE_JPEG_QUALITY, 86])

# ---- lateral ----
lat = cv2.imread("src/lat.jpg", 0)
mask = np.zeros_like(lat)
mask[3:24, 10:28] = 255                                                   # corner mark (faint bracket)
blk = (np.abs(lat.astype(int) - 177) < 9).astype(np.uint8)
blk[:315, :] = 0; blk[:, :245] = 0
blk = cv2.morphologyEx(blk, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))       # the flat block only
mask |= blk*255
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), 1)
print("lat inpaint px", int((mask > 0).sum()))
lat = cv2.inpaint(lat, mask, 15, cv2.INPAINT_TELEA).astype(np.float32)
m = cv2.GaussianBlur(mask.astype(np.float32)/255, (7, 7), 2)
lat = np.clip(lat + np.random.default_rng(3).normal(0, 4, lat.shape)*m, 0, 255)
AP_MM = AP_LM*AP_MMPP
M_lat_mm, k, ang = sim_from(LAT_LM, AP_MM)
print("lateral: %.3f mm/px, rotated %.1f deg" % (k, ang))
lat_x, lat_m = extend(lat, to_canvas(M_lat_mm), 2)
cv2.imwrite("lat_x.jpg", lat_x, [cv2.IMWRITE_JPEG_QUALITY, 88])

# thumbnails for the title screen (real-film area only)
for n, im, M, sh in (("ap", ap, M_ap_mm, ap.shape), ("lat", lat, M_lat_mm, lat.shape)):
    t = cv2.resize(im.astype(np.uint8), (round(84*sh[1]/sh[0]), 84), interpolation=cv2.INTER_AREA)
    cv2.imwrite(n + "_t.jpg", t, [cv2.IMWRITE_JPEG_QUALITY, 85])

# where each real film lies in the arm frame (mm), for the credits / sanity
def bbox(msk):
    ys, xs = np.nonzero(msk)
    return [round(X0 + xs.min()*MM), round(Y0 + ys.min()*MM), round(X0 + xs.max()*MM), round(Y0 + ys.max()*MM)]
info = {"mmpp": MM, "x0": X0, "y0": Y0, "w": W, "h": H, "apFilm": bbox(ap_m), "latFilm": bbox(lat_m),
        "latScale": round(float(k), 3)}
print(json.dumps(info))
