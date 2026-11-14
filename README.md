# Real-Time Vision-Controlled Head-Tracking Engine

A hands-free, low-latency computer vision arcade game built with **Python**, **OpenCV**, and **NumPy**. The engine captures live webcam frames, segments dark hair regions via intensity/HSV thresholding, computes the horizontal head centroid using spatial image moments, and maps head movements directly to spacecraft navigation in an accelerating meteor-survival game.

---

## Key Features

- **Hands-Free Head Tracking:** Real-time horizontal tracking driven by binary inverse thresholding (`cv2.THRESH_BINARY_INV`) and configurable HSV dark-color masking (`cv2.inRange`).
- **Noise-Filtered Contour Segmentation:** Extracts external contours (`cv2.findContours`) and filters background noise using minimum contour-area thresholds (`> 1000 px²`) before isolating the primary region of interest.
- **Spatial Image Moments:** Computes the exact horizontal centroid ($c_x = M_{10} / M_{00}$) via `cv2.moments` for smooth, responsive spacecraft steering.
- **Alpha-Blended Sprite Compositing:** Supports 4-channel `RGBA` PNG sprites (`shuttle1.png`, `asteroid.png`) with boundary-safe alpha compositing over live mirrored video frames.
- **Padded AABB Collision & Progressive Difficulty:** Implements forgiving Axis-Aligned Bounding Box (AABB) collision detection (`10%` hitbox padding) and dynamic difficulty scaling that increases meteor speed and spawn count every 10 seconds.

---

## Computer Vision Pipeline

```text
Webcam Frame (cv2.VideoCapture)
       │
       ▼
Horizontal Mirroring (cv2.flip)
       │
       ▼
Grayscale / HSV Color Thresholding
       │
       ▼
External Contour Detection & Area Filtering (> 1000 px²)
       │
       ▼
Spatial Moments Centroid Extraction (cx = M10 / M00)
       │
       ▼
Spacecraft Clamping, AABB Collision & RGBA Rendering
```

---

## Repository Structure

The repository is organized incrementally from foundational OpenCV primitives to the complete sprite-rendered game engine:

| File | Module / Milestone |
| :--- | :--- |
| `step1_video_loop.py` | Webcam capture initialization and horizontal frame mirroring (`cv2.flip`) |
| `step2_image_on_image.py` | Static image overlay (`shuttle3.png`) onto live webcam frames |
| `step3_color_tracking.py` | Grayscale conversion, inverse binary thresholding, and largest-contour detection |
| `step4_centroid_punch.py` | Spatial moment calculation (`cv2.moments`) and real-time centroid tracking |
| `step5_asteroid_logic.py` | Object-oriented falling obstacle (`Asteroid`) kinematics and screen boundary recycling |
| `step6_all_together.py` | Initial integration of contour-centroid tracking with dynamic obstacle spawning and scoring |
| `step7_collision_logic.py` | HSV dark-range masking and padded AABB collision detection (`has_collision`) |
| `step8_scoring_and_game_over.py` | Time-stepped level progression, translucent Game Over overlay, and instant reset (`R`) |
| `step9_actual_images.py` | **Main Entry Point** — Full game loop with `RGBA` alpha-blended shuttle and asteroid sprites |

---

## Installation & Usage

### Prerequisites
- Python 3.8+
- A working webcam

### Setup
```bash
git clone [https://github.com/TusharSingh098/Real-Time-Vision-Controlled-Head-Tracking-Engine.git](https://github.com/TusharSingh098/Real-Time-Vision-Controlled-Head-Tracking-Engine.git)
cd Vision-Head-Tracking-Engine
pip install opencv-python numpy
```

### Run the Game
Ensure `shuttle1.png` and `asteroid.png` are in the project root directory, then run:
```bash
python step9_actual_images.py
```

### Controls
- **Move Head Left / Right:** Steer the spacecraft horizontally across the screen
- **`R` Key:** Restart immediately after Game Over
- **`Q` Key:** Quit the application

---

## Acknowledgments

Developed as part of the Digital Image Processing (DIP) workshop at the **Embedded Systems and Robotics (EMR) Club, NIT Kurukshetra**.
