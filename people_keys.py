import os
import cv2
from ultralytics import YOLO

model = YOLO('C:\\Users\\nshei\\Desktop\\youtube code\\Expert System\\best.pt')

image_folder = r"C:\Users\nshei\Desktop\youtube code\Expert System\high_movement"

# Define the folder to save output images
output_folder = r"C:\Users\nshei\Desktop\youtube code\Expert System\people_moments"
os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist

# List all image files
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]



for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    results = model(image_path)

    # Get boxes and class labels
    boxes = results[0].boxes.xyxy
    labels = results[0].boxes.cls

    img = cv2.imread(image_path)

    # Draw boxes and labels
    for box, label in zip(boxes, labels):
        xmin, ymin, xmax, ymax = map(int, box)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    num_boxes = len(results[0].boxes)

    if num_boxes > 0:
        output_path = os.path.join(output_folder, f"labeled_{image_file}")
        cv2.imwrite(output_path, img)

cv2.destroyAllWindows()
