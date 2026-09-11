import os
import cv2


from edge_impulse_linux.image import ImageImpulseRunner


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # .../python
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)                # /app

DEFAULT_PHOTO_PATH = os.path.join(PROJECT_DIR, "fotos", "foto.jpg")


"Classifies the image frame"
"If the classifier sees something with confidence >= confidence_threshold it returns the name of that object"
"Otherwise it returns None"
def classify_image(runner, img, confidence_threshold=0.70):
    if img is None:
        return "Error"

    features, _ = runner.get_features_from_image(img)
    res = runner.classify(features)

    bounding_boxes = res.get("result", {}).get("bounding_boxes", [])
    for box in bounding_boxes:
        label = box.get("label")
        score = box.get("value", 0.0)

        if score >= confidence_threshold:
            print(f"Detected {label} with {int(score * 100)}% confidence")
            return label

    return None