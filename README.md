# 🧊 Rubik’s Cube Solver using Computer Vision & Python

A real-time **Rubik’s Cube Solver** that uses your webcam to:

1. Scan each face of a real cube  
2. Classify sticker colors with HSV thresholds  
3. Solve the cube using the [Kociemba two-phase algorithm](https://github.com/hkociemba/RubiksCube-TwophaseSolver)  
4. Guide you through each move with 2D overlays and a separate viewer  

---

## 🎥 Features

- **Webcam scanning** of all 6 faces  
- **HSV-based color classification**  
- **Kociemba solver** via the `kociemba` Python package  
- **Arrow overlays** for visual move guidance  
- **Real-time state tracking** after every move  
- **Separate viewer window** rendering the cube state via sockets  

---

## 🧰 Tech Stack & Libraries

- **Python 3.10.8**  
- **[OpenCV](https://opencv.org/)** – Camera capture, image display, overlays  
- **[NumPy](https://numpy.org/)** – Numerical operations  
- **[kociemba](https://pypi.org/project/kociemba/)** – Cube solving algorithm  
- **socket** – Real-time communication between solver and viewer  
- **pickle** – Serializing cube state data  
- **os**, **copy** – Standard library utilities  

---

## 📁 Project Structure

```
rubiks-cube-solver/
│
├── Main.py       # Main script: scanning, solving & overlay guidance  
├── State.py      # Viewer script: renders current cube state  
├── resources/    # Static assets
│   ├── colors/   # PNG tiles for each sticker color (W, Y, R, O, G, B)
│   ├── U.png      # Arrow overlay images for each move (e.g., U, R, F, etc.)
│   └── …          # Other move arrow PNGs  
└── README.md     # This file  
```
---

### 🛠️ HSV Calibration Notice

> ⚠️ **Important:** The default HSV thresholds used to detect sticker colors are tuned for **one specific cube under specific lighting**.  
> Since color perception varies between different Rubik’s Cubes, cameras, and lighting conditions, you **must calibrate the HSV ranges** for accurate detection on your setup.

---

### 🎯 How to Calibrate Sticker Colors

1. **Run the color calibrator tool** (a Python script with HSV trackbars and webcam feed).
2. Show a sticker (e.g., white face) in front of the webcam and adjust sliders until only that color is detected.
3. Note down the **Hue, Saturation, and Value** ranges that isolate each color clearly.
4. Repeat this process for all 6 colors: White, Red, Yellow, Green, Blue, and Orange.

---

### 📝 Where to Update HSV Values

Open `Main.py`, and locate this function:

```python
def classify_hue(h, s, v):
    if h >= 5 and h <= 36 and s >= 9 and s <= 60 and v >= 45 and v <= 179:
        return "W"
    elif h >= 0 and h <= 25 and s >= 156 and s <= 232 and v >= 82 and v <= 143:
        return "R"
    elif h >= 28 and h <= 39 and s >= 146 and s <= 255 and v >= 132 and v <= 194:
        return "Y"
    elif h >= 42 and h <= 160 and s >= 133 and s <= 255 and v >= 97 and v <= 190:
        return "G"
    elif h >= 55 and h <= 121 and s >= 129 and s <= 255 and v >= 26 and v <= 84:
        return "B"
    elif h >= 1 and h <= 85 and s >= 211 and s <= 248 and v >= 75 and v <= 148:
        return "O"
    else:
        return "O"
```
🔧 **Update the HSV ranges** for each color (`h`, `s`, `v`) based on your calibrated values from the color calibrator tool.

---

## 🚀 Getting Started

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Goddbott/Rubiks-s-Cube-Solver.git
   cd Rubiks-s-Cube-Solver
   ```

2. **Install dependencies**  
   ```bash
   pip install opencv-python numpy kociemba
   ```

3. **Run the viewer** (in one terminal)  
   ```bash
   python State.py
   ```

4. **Run the solver** (in another terminal)  
   ```bash
   python Main.py
   ```

---

## 🎮 Controls

- **During scanning (Main.py)**  
  - Press `U`, `R`, `F`, `D`, `L`, `B` to scan that face  
  - Press `ESC` once all six faces are scanned  

- **During solving**  
  - Press `SPACE` to confirm each move  
  - Press `ESC` to exit at any time  

---

## 📸 Resources

- `resources/colors/` – Sticker tiles for white, yellow, red, orange, green, blue  
- `resources/*.png` – Overlay arrows for each face turn (e.g., `R.png`, `U'.png`, etc.)  

---

Built with ❤️ by **Aditya Ajay**
