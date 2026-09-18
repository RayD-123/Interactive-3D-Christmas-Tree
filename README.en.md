# 🎄 Christmas Magic — Gesture-Controlled Christmas Tree

> Light up a Christmas tree with your hands. Fist for tree, open hand for galaxy, heart gesture for pink heart, and gaze at a gift box to open the photo inside.

**中文** | [English](./README.md)

**🌐 Live Demo**: https://RayD-123.github.io/christmas-magic/  
(Webcam access required. Chrome / Edge recommended.)

<!-- Placeholder: replace with ![Demo](assets/demo.gif) once recorded -->

---

## ✨ Gestures

| Gesture | Effect |
|---|---|
| ✊ Fist | Christmas tree shape |
| 🖐️ Open hand | Galaxy shape (particles scatter into a nebula) |
| ❤️ Two-hand heart | Pink heart shape |
| 👀 Gaze at gift box for 2s | Opens the box, displays the photo |
| 👌 OK sign | Closes the currently opened photo |
| ✊ Hold fist for 5s | Locks the view; then use index finger to rotate in 3D |
| 📷 Add Photos | Upload photos to become gift boxes on the tree |

**Tip**: Add gifts in Tree mode; use Galaxy mode to find and open them.

---

## 🚀 Quick Start

### Online
Visit the GitHub Pages link above.

### Local
Browsers require HTTPS or localhost to access the webcam. **Opening `index.html` directly via `file://` will not work for gestures.** Use a local server:

```bash
# Option 1: Python (most systems have it)
python -m http.server 8000
# Then visit http://localhost:8000

# Option 2: VS Code with Live Server extension — right-click index.html → Open with Live Server
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Three.js r160** | 3D rendering engine — scene, camera, lighting, materials |
| **MediaPipe Tasks Vision** | Hand landmark detection (21 keypoints, dual-hand support) |
| **GLSL Shader** | Custom particle system + per-bulb twinkle effect |
| **InstancedMesh** | Single draw call for rendering tens of thousands of bulbs |
| **Web Audio / Canvas** | Background starfield, aurora effects |
| **Pygame + OpenCV** | Initial prototyping phase (archived in legacy/) |

**Key technical points**:
- Hand openness calculation (finger-tip to wrist distance / palm base length) to recognize fist / open hand / two hands
- Center-screen raycasting for gaze-based gift opening
- Hold-to-lock accumulator with priority interruption to avoid gesture conflicts
- `onBeforeCompile` shader injection for independent bulb twinkling

---

## 🧭 Evolution History

This project went through a full migration from a Python desktop app to a web-based 3D interaction. Here is the chronological breakdown.

| Stage | Tech | Problem Solved | Remaining Issue |
|---|---|---|---|
| 1. Pygame mouse prototype | Python + Pygame | Validated "particles converge into a tree" visual | No interactivity |
| 2. Hand tracking | MediaPipe Hands + Pygame | Replaced mouse with index finger position | Low FPS, particle count dropped to 1200 |
| 3. Migration to web | Three.js + InstancedMesh | Smooth rendering of 10k+ particles | Mouse-only |
| 4. Gesture + 3D interaction | MediaPipe Tasks Vision | Fist/open/two-hand mode switching | Opening gift boxes was awkward |
| 5. Gaze open + view lock | Raycaster + hold accumulator | Eye-gaze opens boxes | Heart was green |
| 6. Particle system refactor (attempt) | Points + custom shader | Wanted finer leaves | Density too low, z-fighting, reverted |
| 7. Back to InstancedMesh | onBeforeCompile injection | Independent bulb twinkle | — |
| 8. Pink heart (final) | Per-mode particle color | Visual theme match | — |

### Stage 1: Pygame Mouse Prototype

The original goal was simple: can a thousand particles flow from random positions into the shape of a Christmas tree?

Implementation was straightforward — Pygame circles, mouse position as gravitational center, particles attracted and rotated into a spiral cone. Crude, but the first moment of seeing particles converge into a tree was still breathtaking.

📄 `legacy/v1_pygame_mouse.py`

### Stage 2: Hand Tracking

Mouse didn't feel "magical" enough. Wanted hands in the air. Integrated MediaPipe Hands, mapped index fingertip coordinates to screen, particles react to fingertip position.

**Pitfall**: Python + MediaPipe only hit ~15fps. Particle count had to drop from 1500 to 1200. MediaPipe's early `mp.solutions.hands` API was also awkward to coordinate with Pygame's event loop — you can see the commented-out iterations in the code.

📄 `legacy/v2_pygame_handtrack.py`

### Stage 3: Migration to Web

Python performance was the bottleneck. Moved to the browser. Used Three.js `InstancedMesh` to render 10k+ spheres in one draw call, boosting FPS from 15 to 60.

This version added the gift box system: users upload photos, boxes hang on the tree, click to open. Still mouse-driven.

📄 `legacy/v3_threejs_mouse_ai.html`

### Stage 4: Gesture + 3D Interaction

Integrated MediaPipe's JS version (Tasks Vision). Calculated palm "openness" (sum of fingertip-to-wrist distances / palm base length) to detect fist, open hand, two hands:

- Openness < 2.5 → fist → tree
- Openness > 5.5 → open hand → galaxy
- Two hands detected → heart

**Pitfall**: Gestures were jittery. Added a 12-frame sliding window average to smooth them out.

📄 `legacy/v4_gaze_lock.html`

### Stage 5: Gaze Open + View Lock

Mouse-clicking gift boxes felt wrong in a gesture-only context. Switched to **gaze detection** — raycast from screen center, accumulate 2s on hit to auto-open.

Also added **view lock**: hold fist for 5s to enter locked state; index finger position then maps to 3D rotation (X pitch, Y yaw) of the tree group.

**Pitfall**: Gaze timer and lock timer conflicted. Added priority logic — gaze target forces lock accumulator to interrupt.

📄 `legacy/v5_stitched.html`

### Stage 6: Particle System Refactor (Attempt)

Wanted finer leaves. Replaced InstancedMesh spheres with a `Points` particle system and custom shader for circular light dots.

**Result**: Visuals were finer, but density dropped too low and z-fighting appeared with bulb blending. Reverted.

📄 `legacy/v6_particle_refactor.html`

### Stage 7: Back to InstancedMesh

Reverted to sphere approach, kept twinkle shader. Used `onBeforeCompile` to inject a `uTime`-based sine wave per instance, achieving "each bulb twinkles independently."

📄 `legacy/v7_interaction_ok.html`

### Stage 8: Final Version

Based on v7:
- Added pink heart mode (particle color switches to Hot Pink in heart form)
- Photo aspect ratio auto-adaptation (frame sized to image proportions)
- Adjusted bulb ratio to reduce visual noise

📄 `index.html`

---

## 🧩 Key Technical Points

### 1. InstancedMesh for 10k+ Particles

`MAX_PARTICLES = 15000` spheres would explode draw calls if each were a separate `Mesh`. Used `InstancedMesh` in 5 categories (red vintage / red bright / gold vintage / gold bright / silver), one draw call each.

```js
meshRedVintage = new THREE.InstancedMesh(sphereGeo, matRedVintage, MAX_PARTICLES);
// Update each instance position per frame via setMatrixAt
```

### 2. Per-Bulb Twinkle (Shader Injection)

Used `onBeforeCompile` to inject `gl_InstanceID` and `uTime` into MeshPhysicalMaterial, making each bulb twinkle at a different phase:

```js
shader.fragmentShader = shader.fragmentShader.replace(
  '#include <emissivemap_fragment>',
  `#include <emissivemap_fragment>
   float flashSpeed = 2.0 + mod(vInstanceID, 4.0);
   float twinkle = 0.6 + 0.4 * sin(uTime * flashSpeed + flashOffset);
   totalEmissiveRadiance *= twinkle;`
);
```

### 3. Gesture Smoothing (Sliding Window Average)

Raw palm openness is noisy. Added 12-frame window average:

```js
opennessHistory.push(currentOpenness);
if (opennessHistory.length > HISTORY_LENGTH) opennessHistory.shift();
const avgOpenness = opennessHistory.reduce((a, b) => a + b, 0) / opennessHistory.length;
```

### 4. Gaze Open (Raycaster + Time Accumulation)

Raycast from screen center `(0, 0)`, accumulate time on gift box hit, trigger at 2s:

```js
centerRaycaster.setFromCamera(centerVector, camera);
const intersects = centerRaycaster.intersectObjects(activeGiftMeshes, true);
// On hit: giftGazeTimer += delta * 1000; open when >= GIFT_OPEN_TIME
```

### 5. Lock Accumulator + Priority Interruption

Hold fist for 5s to enter locked view. But if gaze target is a gift box, interrupt lock accumulation — prevents accidental locking when trying to open a box:

```js
if (gazeTargetBox !== null) {
    triggerLock = false;
    lockAccumulator = 0;
}
```

### 6. Smooth Shape Transitions

Target positions for each form (tree / galaxy / heart) are pre-computed and stored in a `shapes` object. Each frame lerps current positions toward targets, creating a flowing effect:

```js
currentPositions[ix] += (tPos[ix] * scaleMult - currentPositions[ix]) * speed;
```

---

## 📁 Legacy Versions

All historical versions are in `legacy/`, filenames corresponding to evolution stages:

- `v1_pygame_mouse.py` — Pygame mouse prototype
- `v2_pygame_handtrack.py` — Pygame + MediaPipe gestures
- `v3_threejs_mouse_ai.html` — Migration to Three.js
- `v4_gaze_lock.html` — Gestures + gaze open
- `v5_stitched.html` — Appearance + interaction stitched
- `v6_particle_refactor.html` — Particle system refactor (abandoned)
- `v7_interaction_ok.html` — InstancedMesh reverted

---

## 📄 License

MIT License — free to use, modify, and distribute.
