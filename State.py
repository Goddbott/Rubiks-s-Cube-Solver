import cv2
import numpy as np
import pickle
import socket


def load_image_with_alpha(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Image not found: {path}")
    return img

def resize_keep_aspect(img, target_width, target_height):
    h, w = img.shape[:2]
    scale = min(target_width / w, target_height / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

def overlay_image_alpha(bg, overlay, pos):
    x, y = pos
    h, w = overlay.shape[:2]
    if x + w > bg.shape[1] or y + h > bg.shape[0]:
        return bg
    if overlay.shape[2] == 4:
        alpha = overlay[:, :, 3] / 255.0
        for c in range(3):
            bg[y:y+h, x:x+w, c] = alpha * overlay[:, :, c] + (1 - alpha) * bg[y:y+h, x:x+w, c]
    else:
        bg[y:y+h, x:x+w] = overlay
    return bg

faces = {
    "U": [(235, 10), (305, 10), (375, 10), (235, 80), (305, 80), (375, 80), (235, 150), (305, 150), (375, 150)],
    "F": [(235, 220), (305, 220), (375, 220), (235, 290), (305, 290), (375, 290), (235, 360), (305, 360), (375, 360)],
    "R": [(445, 220), (515, 220), (585, 220), (445, 290), (515, 290), (585, 290), (445, 360), (515, 360), (585, 360)],
    "B": [(655, 220), (725, 220), (795, 220), (655, 290), (725, 290), (795, 290), (655, 360), (725, 360), (795, 360)],
    "L": [(25, 220), (95, 220), (165, 220), (25, 290), (95, 290), (165, 290), (25, 360), (95, 360), (165, 360)],
    "D": [(235, 430), (305, 430), (375, 430), (235, 500), (305, 500), (375, 500), (235, 570), (305, 570), (375, 570)]
}

def cube_to_string(cube):
    order = ['U', 'R', 'F', 'D', 'L', 'B']
    return ''.join(cube[face][i] for face in order for i in range(9))



color_map = {
    'W': "Resources/Colors/white.png",
    'Y': "Resources/Colors/yellow.png",
    'R': "Resources/Colors/red.png",
    'O': "Resources/Colors/orange.png",
    'G': "Resources/Colors/green.png",
    'B': "Resources/Colors/blue.png"
}
for color in color_map:
    color_map[color] = resize_keep_aspect(load_image_with_alpha(color_map[color]), 70, 70)

HOST = 'localhost'
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("🔄 Viewer waiting for cube state updates...")

conn, _ = s.accept()
print("✅ Viewer connected to sender.")
conn.setblocking(False)

cube = None

while True:
    frame = np.zeros((640, 870, 3), dtype=np.uint8)

    try:
        data = conn.recv(4096)
        if data:
            cube = pickle.loads(data)
    except BlockingIOError:
        pass

    if cube:
        cube_str = cube_to_string(cube)
        idx = 0
        for face in ['U', 'R', 'F', 'D', 'L', 'B']:
            for i in range(9):
                color = cube_str[idx]
                img = color_map[color]
                frame = overlay_image_alpha(frame, img, faces[face][i])
                idx += 1

    cv2.imshow("Rubik's Cube State Viewer", frame)
    if cv2.waitKey(1) == 27:
        break

conn.close()
cv2.destroyAllWindows()
