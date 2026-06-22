import cv2
import mediapipe as mp
import numpy as np
import time

# ========== KONFIGURASI MEDIAPIPE ==========
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# ========== FUNGSI DETEKSI GESTUR ==========
def is_index_finger(landmarks):
    """1 jari: hanya telunjuk terangkat"""
    index_up = landmarks[8].y < landmarks[6].y
    middle_up = landmarks[12].y < landmarks[10].y
    ring_up = landmarks[16].y < landmarks[14].y
    pinky_up = landmarks[20].y < landmarks[18].y
    return index_up and not middle_up and not ring_up and not pinky_up

def is_peace(landmarks):
    """2 jari: telunjuk + tengah terangkat"""
    index_up = landmarks[8].y < landmarks[6].y
    middle_up = landmarks[12].y < landmarks[10].y
    ring_up = landmarks[16].y < landmarks[14].y
    pinky_up = landmarks[20].y < landmarks[18].y
    return index_up and middle_up and not ring_up and not pinky_up

def is_three_fingers(landmarks):
    """3 jari: telunjuk + tengah + manis terangkat, kelingking tidak"""
    index_up = landmarks[8].y < landmarks[6].y
    middle_up = landmarks[12].y < landmarks[10].y
    ring_up = landmarks[16].y < landmarks[14].y
    pinky_up = landmarks[20].y < landmarks[18].y
    return index_up and middle_up and ring_up and not pinky_up

# ========== FUNGSI EFEK ==========
def apply_spotlight(frame, center_x, center_y, radius=100, brightness=1.8):
    """Efek spotlight: area sekitar jari terang, sisanya gelap"""
    h, w = frame.shape[:2]
    output = frame.copy().astype(np.float32) / 255.0
    mask = np.zeros((h, w), dtype=np.float32)
    cv2.circle(mask, (center_x, center_y), radius, 1.0, -1)
    mask = cv2.GaussianBlur(mask, (51, 51), 20)
    mask_3ch = np.stack([mask, mask, mask], axis=2)
    output = output * (1.0 - mask_3ch) * 0.3 + output * mask_3ch * brightness
    output = np.clip(output * 255, 0, 255).astype(np.uint8)
    return output

def apply_blur(frame, kernel_size=(51, 51)):
    """Efek Gaussian blur"""
    return cv2.GaussianBlur(frame, kernel_size, 0)

def apply_sketch(frame):
    """
    Efek sketsa pensil (gabungan grayscale + edge detection + blending)
    Menghasilkan gambar seperti sketsa pensil hitam-putih.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Invert warna untuk efek sketsa
    inv_gray = 255 - gray
    # Gaussian blur pada gambar inverted
    blur = cv2.GaussianBlur(inv_gray, (21, 21), 0)
    # Divide grayscale dengan blur (dodge blending)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    # Kembalikan ke BGR agar bisa ditampilkan (walaupun grayscale)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

# ========== FUNGSI UTAMA ==========
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Kamera tidak terdeteksi.")
        return

    print("🎥 Kamera aktif. Tekan [ESC] atau [Q] untuk keluar.")
    print("🖐️  Kontrol Gestur:")
    print("   1 Jari (Telunjuk) = Spotlight")
    print("   2 Jari (Peace) = Blur")
    print("   3 Jari = Sketsa Pensil")
    print("   Lainnya = Normal")

    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        mode = "Normal"
        output = frame.copy()
        tip_x, tip_y = 0, 0

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2)
                )

                landmarks = hand_landmarks.landmark
                tip_x = int(landmarks[8].x * w)
                tip_y = int(landmarks[8].y * h)

                # Prioritas gestur (jika lebih dari 1 terdeteksi, ambil yang paling spesifik)
                if is_three_fingers(landmarks):
                    mode = "Sketch"
                elif is_peace(landmarks):
                    mode = "Blur"
                elif is_index_finger(landmarks):
                    mode = "Spotlight"
                # selain itu Normal

        # ---------- TERAPKAN EFEK ----------
        if mode == "Spotlight" and tip_x > 0 and tip_y > 0:
            output = apply_spotlight(output, tip_x, tip_y)
        elif mode == "Blur":
            output = apply_blur(output, (51, 51))
        elif mode == "Sketch":
            output = apply_sketch(output)
        # else: Normal

        # ---------- HUD (Informasi di Layar) ----------
        # Tampilkan mode dengan warna berbeda
        color_mode = (255, 255, 0)  # default kuning
        if mode == "Spotlight":
            color_mode = (0, 255, 255)  # cyan
        elif mode == "Blur":
            color_mode = (0, 0, 255)  # merah
        elif mode == "Sketch":
            color_mode = (255, 0, 255)  # magenta

        cv2.putText(output, f"Mode: {mode}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, color_mode, 2)

        # Instruksi di bawah
        cv2.putText(output, "1:Spotlight  2:Blur  3:Sketch  ESC/Q:Keluar", (10, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # FPS Counter
        curr = time.time()
        if prev_time:
            fps = 1 / (curr - prev_time)
            cv2.putText(output, f"FPS: {int(fps)}", (w - 120, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        prev_time = curr

        cv2.imshow("Gesture Camera - 1:Spotlight 2:Blur 3:Sketch", output)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("👋 Selesai.")

if __name__ == "__main__":
    main()