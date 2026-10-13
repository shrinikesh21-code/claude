# 5 Thumbnail Style Directions

Each style is a layout recipe. The Claude Project fills in the car model and writes a full ChatGPT prompt from it. Pick one and tell me which, and I'll lock it into `PROJECT_INSTRUCTIONS.md`.

| # | Name | Layout | Headline | Mood |
|---|---|---|---|---|
| 1 | Classic Split | Vertical split, dirty left, clean right, thin white divider | REVIVE YOUR RIDE | Clean, familiar, safest |
| 2 | Diagonal + Van | Angled split with the Cleanwheels van parked in a home driveway behind the car | WE COME TO YOU | Sells the mobile service |
| 3 | Stacked | Before on top, after below, BEFORE / AFTER chips | Car model as headline | Bold, scroll-stopping |
| 4 | Driveway Scene | Full-bleed suburban house, car mid-detail, small before inset | DETAILED AT YOUR DOOR | Lifestyle, trust |
| 5 | Minimal Black | Black studio, blue accent line, car model in huge type, two small photo chips | Car model | Premium, luxury look |

## Sample prompts (example car: Toyota Fortuner)

Paste each one into ChatGPT (image mode). Attach `logo/cleanwheels-logo.png` every time. If you have a photo of the finished car, attach it too (see the "with photo" line). These are the same prompts the Project will produce.

### Sample 1: Classic Split

```
Create an Instagram post image, portrait 4:5 (1080x1350).

Attached: (1) the Cleanwheels logo, (2) [OPTIONAL: a photo of the finished, detailed Toyota Fortuner]. 
If photo (2) is attached, use that exact car as the right-hand "AFTER" half and keep its colour, angle and surroundings. Create the left-hand "BEFORE" half as the SAME car, same angle, same lighting, but filthy. If no photo is attached, create both halves yourself.

Layout: a perfect vertical split down the middle with a thin white divider line.
LEFT (BEFORE): a white Toyota Fortuner, front three-quarter view, covered in road dust, mud splatter, water spots, dull paint, brown brake-dust on the wheels, grimy glass. Overcast, flat light.
RIGHT (AFTER): the same Fortuner, same angle, deep mirror-gloss paint, sharp reflections, glossy black tyres, bright clean alloys, spotless glass. Brighter, crisp light.
Setting: a quiet Adelaide suburban street, soft blurred background.

Text (exact spelling, bold white Helvetica-style uppercase):
- Top center: "REVIVE YOUR RIDE"
- Below it, smaller: "MOBILE CAR DETAILING"
- Bottom center: place the attached Cleanwheels logo exactly as provided, do not redraw it, about 28% of image width.
Small corner tags: "BEFORE" bottom-left, "AFTER" bottom-right.
No other text. Blur any licence plate. Photorealistic, high-end automotive photography, not cartoonish.
```

### Sample 2: Diagonal + Van

```
Create an Instagram post image, portrait 4:5 (1080x1350).

Attached: (1) the Cleanwheels logo, (2) [OPTIONAL: photo of the finished Toyota Fortuner]. If (2) is attached, use that exact car for the AFTER half and make the BEFORE half the same car, same angle, but dirty. Otherwise create both.

Layout: one diagonal split from top-right to bottom-left. Upper-left triangle = BEFORE (dusty, muddy, dull Fortuner, grey overcast light). Lower-right triangle = AFTER (same Fortuner, mirror gloss, golden-hour light). Thin white diagonal divider.
Behind the car, in a suburban Adelaide home driveway, a white detailing van with a blue "Cleanwheels" look (no readable text on the van except a tiny blue wordmark). The home and garage are blurred in the background, which shows we come to the customer's house.

Text (exact, bold white uppercase Helvetica-style):
- Top: "WE COME TO YOU"
- Under it, small: "MOBILE CAR DETAILING · ADELAIDE"
- Bottom center: the attached logo, unchanged, about 25% width.
Tags: "BEFORE" and "AFTER" small, blue pill shapes with white text.
No other text. Blur any plate. Photorealistic.
```

### Sample 3: Stacked

```
Create an Instagram post image, portrait 4:5 (1080x1350).

Attached: (1) the Cleanwheels logo, (2) [OPTIONAL: photo of the finished Toyota Fortuner]. If (2) is attached, use it for the AFTER panel and recreate the same car filthy for the BEFORE panel, same angle. Otherwise create both.

Layout: two equal horizontal panels stacked, separated by a thin electric blue (#0A3CFF) line. TOP = BEFORE: Fortuner dusty, muddy, dull paint, dirty wheels. BOTTOM = AFTER: same car, same angle, mirror-gloss, spotless. Black background behind the panels with 40px margins.
Large bold white uppercase Helvetica-style headline across the top margin: "TOYOTA FORTUNER".
Panel chips: "BEFORE" on the top panel, "AFTER" on the bottom panel, white text in electric blue rounded chips.
Bottom margin: the attached logo unchanged, about 25% width, centered.
No other text. Blur plates. Photorealistic automotive photography.
```

### Sample 4: Driveway Scene

```
Create an Instagram post image, portrait 4:5 (1080x1350).

Attached: (1) the Cleanwheels logo, (2) [OPTIONAL: photo of the finished Toyota Fortuner]. If (2) is attached, the main car must be that exact Fortuner looking gleaming. Otherwise create one.

Scene: full-bleed photo of a gleaming white Toyota Fortuner in the driveway of a modern Adelaide suburban home, late-afternoon sun, a white detailing van parked behind it, a detailer in dark overalls buffing the bonnet. Cinematic, shallow depth of field.
Small inset at the top-left corner (rounded corners, white border): the same Fortuner BEFORE, dusty and muddy, labelled "BEFORE". Main image labelled "AFTER" small, bottom-left.
Text (exact, bold white uppercase Helvetica-style): "DETAILED AT YOUR DOOR" near the top, with a smaller line below "MOBILE CAR DETAILING · ADELAIDE".
Bottom center: the attached logo unchanged, about 25% width, on a subtle dark gradient for legibility.
No other text. Blur plates. Photorealistic.
```

### Sample 5: Minimal Black

```
Create an Instagram post image, portrait 4:5 (1080x1350).

Attached: (1) the Cleanwheels logo, (2) [OPTIONAL: photo of the finished Toyota Fortuner]. If (2) is attached, use that exact car for the AFTER chip and recreate it filthy for the BEFORE chip, same angle. Otherwise create both.

Layout: pure black (#000000) background. Huge bold white uppercase Helvetica-style text "FORTUNER" across the upper third, with "TOYOTA" small in electric blue (#0A3CFF) above it. Centre: a large hero image of the gleaming AFTER Fortuner, floating on black with soft blue rim light and a glossy floor reflection. Two small rounded photo chips bottom-left (BEFORE, dusty) and bottom-right (AFTER, gleaming), labelled in tiny white caps. A thin electric blue line separates content from the footer.
Footer: the attached logo unchanged, about 25% width, centered, with "MOBILE CAR DETAILING · ADELAIDE" tiny in white beneath it.
No other text. Blur plates. Premium, luxury, photorealistic.
```
