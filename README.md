# AI Virtual Mouse

> A lightweight hand-tracking based virtual mouse using a webcam and MediaPipe landmarks.

## Overview

`AI Virtual Mouse` turns simple hand gestures into mouse actions using your webcam. It detects hand landmarks with MediaPipe, interprets finger states and distances to control cursor movement, left-clicks, and scrolling — all without touching a physical mouse.

## Features

- **Cursor movement**: Move the cursor by pointing with the index finger (index-finger-only mode).
- **Left click**: Perform a left-click by pinching the index and middle fingers (two-finger close gesture).
- **Smooth scrolling**: Scroll by moving two fingers vertically while keeping them apart.
- **Configurable settings**: Camera resolution, active frame margin, movement smoothening, and scroll speed are exposed in the main script.
- **Lightweight, real-time**: Built with optimized MediaPipe hand landmarks and simple interpolation for responsive control.

## Technical details

- Hand detection and landmark extraction: `HandTrackingModule.py` uses MediaPipe Hands to detect landmarks and compute landmark coordinates.
- Gesture interpretation: The script calculates which fingers are up with a simple tip-position test and measures pairwise distances to detect clicks and scrolling gestures.
- Cursor mapping: Camera coordinates are interpolated and mapped to screen coordinates using `autopy.screen.size()` and `numpy.interp()`, with a configurable `smoothening` factor to reduce jitter.
- Scrolling: A `pynput.mouse.Controller` instance is used to perform smoother, programmatic scroll events based on vertical finger motion.

## Files

- `AiVirtualMouseProject.py` — Main application. Captures webcam frames, uses `HandTrackingModule` to detect gestures, and maps them to mouse actions.
- `HandTrackingModule.py` — MediaPipe-based helper module providing `handDetector` with utilities: `findHands`, `findPosition`, `fingersUp`, and `findDistance`.

## Dependencies

- Python 3.8+ recommended
- opencv-python
- mediapipe
- numpy
- autopy
- pynput

Install with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install opencv-python mediapipe numpy autopy pynput
```

Note: `autopy` may require platform-specific binaries; on macOS it typically installs via pip, but check the project README if installation fails.

## Usage

1. Activate your virtual environment (if used).
2. Connect a webcam and ensure it is accessible by OpenCV (default device index 0).
3. Run:

```bash
python AiVirtualMouseProject.py
```

- The application opens a window titled "AI Virtual Mouse" showing the camera feed and landmark overlays.
- Press `ESC` to exit.

## Configuration knobs (in `AiVirtualMouseProject.py`)

- `wCam, hCam` — camera capture width and height (default 640×480).
- `frameR` — active rectangle margin around the camera frame used for mapping to screen coordinates.
- `smoothening` — smoothing factor for cursor movement (higher = smoother/slower).
- `scrollSpeed` — multiplier for scroll sensitivity.

## Real-world applications

- Accessibility: hands-free cursor control for users with limited dexterity.
- Presentations: navigate slides and control on-screen content without touching a device.
- Public kiosks & hygiene-sensitive environments: touchless interaction to reduce surface contact.
- Prototyping gesture UIs for AR/VR and interactive exhibits.
- Rapid prototyping for robotics or embedded systems where camera-based gesture control is desired.

## Troubleshooting & Tips

- If the cursor is jittery, increase `smoothening` or improve lighting for better landmark detection.
- If landmarks are not detected, ensure MediaPipe and your webcam are working and that the camera index is correct.
- For higher resolution screens, adjust `frameR`, `wCam/hCam`, and `smoothening` to tune mapping and responsiveness.

## License

This project is provided as-is for educational and prototyping use. Feel free to adapt and improve it.
