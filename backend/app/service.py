import os
from typing import List
from ultralytics import YOLO
from app.schemas import Damage, CompareResponse, DamageType
import uuid

# -----------------------------
# Folders and model paths
# -----------------------------
UPLOAD_FOLDER = "app/uploads"                 # Temporary folder to store uploaded images
DATASET_FOLDER = "dataset"                    # Dataset folder for training (data.yaml)
MODEL_PATH = "yolov8n.pt"                     # Base pretrained YOLOv8 model
TRAINED_MODEL_PATH = "runs/detect/car_damage_training/best.pt"  # Optional fine-tuned model

# Load the base YOLOv8 model once at module load
model = YOLO(MODEL_PATH)

# Cost mapping per damage type (used to estimate repair costs)
COST_MAP = {
    "Scratch": 50,
    "Dent": 150,
    "Broken glass": 200,
    "front-end-damage": 500,
    "rear-end-damage": 400,
    "side-impact-damage": 300,
    "other_damage": 100
}

# -----------------------------
# Utility: Save uploaded image
# -----------------------------
def save_image(file, filename: str) -> str:
    """
    Save uploaded file to disk and return file path.
    """
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if missing
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(file)
    return file_path

# -----------------------------
# Quick YOLO training (~3 mins)
# -----------------------------
def train_model(
    data_yaml: str = os.path.join(DATASET_FOLDER, "data.yaml"),
    epochs: int = 2,       # Slightly more epochs for better demo (~2-3 mins)
    imgsz: int = 320,      # Low resolution for speed
    batch: int = 2,        # Small batch to reduce memory usage
    subset: float = 0.2    # Use only 20% of dataset to speed up
):
    """
    Quick YOLO fine-tuning for demonstration purposes (~3 mins)
    - Subset allows using a small fraction of images to speed up training
    - Saves model at TRAINED_MODEL_PATH
    """
    if not os.path.exists(data_yaml):
        raise FileNotFoundError(f"Dataset YAML not found: {data_yaml}")

    # Train YOLO
    model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project="runs/detect",
        name="car_damage_training",
        exist_ok=True,
        subset=subset  # Only use a fraction of images
    )
    print(f"Quick training complete. Model saved at {TRAINED_MODEL_PATH}")
    return TRAINED_MODEL_PATH

# -----------------------------
# IoU calculation for damage comparison
# -----------------------------
def compute_iou(box1: List[int], box2: List[int]) -> float:
    """
    Compute Intersection over Union (IoU) between two bounding boxes.
    Each box = [x1, y1, x2, y2]
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    if inter_area == 0:
        return 0.0

    box1_area = (box1[2]-box1[0]) * (box1[3]-box1[1])
    box2_area = (box2[2]-box2[0]) * (box2[3]-box2[1])
    iou = inter_area / (box1_area + box2_area - inter_area)
    return iou

# -----------------------------
# Check if damage already exists
# -----------------------------
def is_damage_in_list(damage: Damage, damage_list: List[Damage], iou_thresh: float = 0.5) -> bool:
    """
    Determine if a damage in after-image already exists in before-image.
    Uses IoU threshold to allow minor coordinate shifts.
    """
    for d in damage_list:
        if d.type != damage.type:
            continue
        iou = compute_iou(damage.coordinates, d.coordinates)
        if iou > iou_thresh:
            return True
    return False

# -----------------------------
# Extract detected damages from YOLO results
# -----------------------------
def extract_damages(results) -> List[Damage]:
    """
    Parse YOLOv8 results to return a list of Damage objects.
    """
    damages = []
    for r in results:
        for box in r.boxes:
            cls_idx = int(box.cls)                     # Class index
            confidence = float(box.conf)               # Confidence score 0-1
            coords = box.xyxy[0].tolist()             # Bounding box: [x1, y1, x2, y2]
            try:
                damage_type = DamageType(r.names[cls_idx])  # Map class index to enum
            except:
                damage_type = DamageType.other_damage

            # Severity = 1–10, scaled from confidence
            severity = max(1, min(10, int(confidence * 10)))

            # Estimated cost based on severity and type
            estimated_cost = severity * COST_MAP.get(damage_type.value, 100)

            damages.append(Damage(
                type=damage_type,
                severity=severity,
                confidence=confidence,
                coordinates=[int(c) for c in coords],
                estimated_cost=estimated_cost
            ))
    return damages

# -----------------------------
# Main comparison function
# -----------------------------
def compare_images_and_report(before_image: str, after_image: str) -> CompareResponse:
    """
    Run YOLO detection on before and after images,
    identify new damages, compute total estimated cost,
    and return a structured report.
    """
    # Use fine-tuned model if it exists
    trained_model_path = TRAINED_MODEL_PATH if os.path.exists(TRAINED_MODEL_PATH) else MODEL_PATH
    inference_model = YOLO(trained_model_path)

    # Run predictions
    results_before = inference_model.predict(before_image)
    results_after = inference_model.predict(after_image)

    # Extract detected damages
    damages_before = extract_damages(results_before)
    damages_after = extract_damages(results_after)

    # Determine new damages appearing in after-image
    new_damages = [d for d in damages_after if not is_damage_in_list(d, damages_before)]

    # Total estimated repair cost
    total_cost = sum(d.estimated_cost for d in new_damages)

    summary = f"Detected {len(new_damages)} new damages. Estimated total cost: ${total_cost}"

    return CompareResponse(
        before_image=before_image,
        after_image=after_image,
        new_damages=new_damages,
        total_cost_estimate=total_cost,
        summary=summary
    )
