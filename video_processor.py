import cv2
from ultralytics import YOLO
from collections import Counter

model = YOLO("yolov8n.pt")

def generate_summary(all_objects):
    counter = Counter(all_objects)

    if not counter:
        return "No significant objects detected."

    most_common = counter.most_common(3)
    objects = [obj for obj, _ in most_common]

    summary = "This video mainly contains "

    if len(objects) == 1:
        summary += f"{objects[0]}."
    else:
        summary += ", ".join(objects[:-1]) + f" and {objects[-1]}."

    # Add interpretation
    if "person" in objects:
        summary += " Human activity is prominent."
    if "car" in objects or "bus" in objects:
        summary += " It appears to include traffic or transportation scenes."

    return summary


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    results_data = []
    all_detected_objects = []

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 10 == 0:
            results = model(frame)

            detected_objects = []
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    detected_objects.append(label)
                    all_detected_objects.append(label)

            results_data.append({
                "frame": frame_count,
                "objects": list(set(detected_objects))
            })

        frame_count += 1

    cap.release()

    summary = generate_summary(all_detected_objects)

    return results_data, summary