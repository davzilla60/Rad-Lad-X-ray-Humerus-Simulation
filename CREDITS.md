# Credits

## Radiographs

The two films are from **different people**. They were combined into one teaching case.

### Lateral humerus

**Adapted from:** Abedeen, Iftekharul; Rahman, Md. Ashiqur; Zohra Prottyasha, Fatema; Ahmed, Tasnim; Mohmud
Chowdhury, Tareque; Shatabda, Swakkhar (2023). *FracAtlas: A Dataset for Fracture Classification, Localization and
Segmentation of Musculoskeletal Radiographs.* figshare. Dataset. https://doi.org/10.6084/m9.figshare.22363012.v7

Source file: https://figshare.com/articles/dataset/The_dataset/22363012?file=65518038

Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The film shows a plate and screws from earlier fixation. That metalwork belongs to the source film, not to the
simulated patient.

### AP humerus

A normal AP humerus radiograph from **Shutterstock**, used under the Rad-Lad Shutterstock subscription licence. It
isn't covered by an open licence and mustn't be reused outside this simulator.

### Changes made

1. **Lateral:**
   - A faint corner mark and a flat grey redaction block (over the abdomen) were removed by inpainting, with grain
     added back.
   - The film was scaled (≈0.93 mm/px, **estimated**), rotated 2.7° and aligned to the AP on the humeral head and
     the distal humerus.
2. **AP:** converted from a tinted image to greyscale. The pixel spacing is **estimated** at 0.2 mm from the length
   of the humerus. The originals carry no calibration.
3. Both films were resampled onto one shared canvas at 0.25 mm/px. Each was extended beyond its edges with a
   progressively blurred edge-replicate. This **synthetic** margin is only seen if you collimate wider than the
   original film. It also covers the top of the lateral, above the humeral head.
4. In the browser, every image you make is the real film:
   - cropped to your light field;
   - magnified for SID and position;
   - overlaid with a **simulated** bra strap and slider, and a necklace;
   - blurred for movement;
   - re-contrasted / noised for your kV, grid and exposure;
   - stamped with your lead marker.

   None of these effects is a real finding.
5. Exposure index, deviation index, AEC behaviour and DAP come from a simplified teaching model, not a calibrated
   system.
6. The 3-D room and patient are generic and procedural.

Educational simulation. It isn't a medical device and isn't for clinical use.
