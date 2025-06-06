import cv2
import numpy as np
import os

output_dir = "C:\\Users\\nshei\\Desktop\\youtube code\\Expert System\\high_movement"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture('C:\\Users\\nshei\\Desktop\\youtube code\\Expert System\\gameplay.mp4')

ret, prev_frame = cap.read()
prev_frame = cv2.resize(prev_frame, (640, 480))
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

frame_count = 0
save_cooldown = 100
last_saved_frame = -save_cooldown
save_index = 0

low, mid, hi = 0, 0, 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(prev_gray, gray)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    motion_score = np.count_nonzero(thresh)

    if motion_score < 30000:
        level = "LOW"
        low += 1
        color = (255, 0, 0)
    elif motion_score < 50000:
        level = "MID"
        mid += 1
        color = (0, 255, 255)
    else:
        level = "HIGH"
        hi += 1
        color = (0, 0, 255)

        if frame_count - last_saved_frame >= save_cooldown:
            save_path = os.path.join(output_dir, f"high_{save_index}.jpg")
            cv2.imwrite(save_path, frame)
            print(f"Saved: {save_path}")
            last_saved_frame = frame_count
            save_index += 1

    cv2.putText(frame, f'Motion: {level}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
    cv2.putText(frame, f'Score: {motion_score}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow('Motion Visualizer', frame)
    prev_gray = gray
    frame_count += 1

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"LOW: {low}, MID: {mid}, HIGH: {hi}")
