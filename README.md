# X Marks the Spot — Humerus X-ray

An embeddable, single-file teaching simulator for the Rad-Lad website. It's the second plain-film sim in
*X Marks the Spot*, after the chest. It uses the same console layout and engine. The radiographs are a real AP (Shutterstock, licensed) and a
real lateral humerus (FracAtlas, CC BY 4.0), from **two different people** (see `CREDITS.md`). Your set-up is then simulated onto them in the
browser.

Marker: **That's so Humerus!** (glyph "H"). You earn it when both views score 45/50 or more on the first exposure,
with no repeats.

## Flow

1. **Request & checks.** Choose today's patient. Both are booked for an AP and lateral right humerus (aching
   upper-arm pain, no injury, ?bone lesion):
   - **Outpatient, walked in** (46-year-old woman). She can stand.
   - **Ward patient, on a trolley** (81-year-old woman). She can't stand, or sit without support.

   Then tick the pre-exposure checks: ID, justification, top and bra off with a gown on, necklace and jewellery off.
   Anything left unticked shows up on the film as a bra strap and slider, or a necklace.
2. **AP set-up (3-D room).** The room has an erect stand, a patient table with a bucky tray and a ceiling tube on a
   wide bridge. You choose:
   - **Patient position:** standing at the stand, seated on a stool at the stand, or **supine on the table**. The
     tube tilts to beam straight down for the table.
   - **Arm:** slightly abducted with the hand supinated (AP), or elbow flexed with the back of the hand on the abdomen
     (internal rotation, which is the lateral position).
   - **SID:** 100 / 150 / 180 cm.

   The correct position depends on the patient. Standing or seated scores full marks for the outpatient, and supine
   is marked down as an unnecessary transfer. For the ward patient, supine is correct and standing or seated is
   unsafe.
3. **Light beam.** You see her from the tube side (her front, so her right arm is on your left). This view is the
   same way round as the film. Then:
   - Drag the field to put the cross-wires on mid-shaft.
   - Drag the edges to collimate from the shoulder to the elbow joint.
   - Drop an **L / R** lead marker.
   - *Palpate* shows the acromion, the greater tuberosity and the epicondyles. *AEC* shows the chambers.
4. **Exposure.** Set kV, AEC chambers or manual mAs, grid, and the instruction (stop breathing / keep still /
   none).
5. **Review.** Accept, or repeat for 5 points plus the extra dose.
6. **Lateral.** She stays in the same position and only the arm is re-rotated. A note explains that with a suspected
   fracture you'd turn the patient, or use a horizontal-beam lateral, instead of rotating the arm.
7. **Debrief.** Both films, the image criteria, a scored breakdown (50 per view) and the total DAP.

### The key trick: one arm frame, two films

Both films are resampled onto one canonical "arm frame". This is in mm, in AP-film orientation, with the AP pixel
spacing estimated at 0.2 mm. The lateral is aligned to it on the humeral head top and the distal humerus, at
≈0.93 mm/px, rotated 2.7°. The **arm rotation you set**, not the step you're on, decides which film you get:

- Supinate the arm for the "lateral" and you get a second AP.
- Internally rotate it for the AP and you get the lateral.

### What is simulated on the real films

- Cropping to your field.
- Magnification for SID and for the table (object–image distance of 6 cm erect, 7 cm through the table).
- Bra strap and slider, and a necklace.
- Movement blur toward the shoulder when the breath isn't held.
- Exposure: kV contrast, no-grid fog, noise when underexposed, burn-out when overexposed.
- The **AEC** reads what each chamber sees on that film:
  - Over air, the raw beam ends the exposure far too early.
  - Over the chest wall, the exposure runs long.
  - A chamber outside the collimated field means the back-up timer ends the exposure.
  - The lesson is to use manual exposure for a limb.
- Your lead marker.

Grading references (arm-frame mm) are in `assets/calib.json`:

- **Centre:** mid-shaft at (113, 215), ±15 / 25 mm.
- **Field must include:** the shoulder joint (top ≤ 45), the elbow joint (bottom ≥ 385), the lateral soft tissue
  (left ≤ 62) and the medial head / glenoid (right ≥ 165).
- **Field must not reach:** the neck (top < 0), the forearm (bottom > 440), beyond the skin (left < 20) or the chest
  wall (right > 215).
- **Exposure reference:** 65 kV / 6.3 mAs with the grid at 100 cm gives DI 0.

## Files

- `humerus.embed.html` is the self-contained deliverable (~850 KB). `index.html` is an identical copy for one-drop
  hosting.
- `humerus.html` is the source. It loads `assets/`, `assets/calib.js` and `room3d.js`. Run `python inline.py` to
  rebuild both deliverables.
- `room3d.js` is the procedural three.js room (three.js from jsDelivr): the erect stand, the table and bucky, the
  stool, the tube with a tilting head, the light-beam spotlight, and the standing, seated and supine patient with
  her arm poses. If you change it, bump `?v=N` in `humerus.html` **and** `inline.py` together.
- `assets/`:
  - `ap_x.jpg`, `lat_x.jpg`: the films on the shared arm-frame canvas, with a synthetic margin.
  - `*_t.jpg`: title thumbnails.
  - `calib.json` / `calib.js`: geometry, tolerances, film reference values.
  - The logos.
- `assets/src/` holds the original images. The Shutterstock AP original (`ap.jpg`) is licensed and is **not** in the repo, so keep your own copy there to rebuild. Run `python ../tools/prep_assets.py` from inside `assets/` to rebuild.

Debug hooks: `window.__xr` (`S()`, `cur()`, `setCase(k)`, `startProj(p)`, `gotoCentre()`, `gotoExpose()`,
`ideal()`, `expose()`, `accept()`, `grade(p, shot)`, `parse(cmd)`) and `window.__room()`.
