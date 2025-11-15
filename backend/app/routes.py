from fastapi import APIRouter, UploadFile, File
from app.service import save_image, compare_images_and_report
from app.schemas import CompareResponse
import uuid

router = APIRouter(prefix="/api")

# -------------------------------------
# Compare endpoint (session-free)
# -------------------------------------
@router.post("/compare", response_model=CompareResponse)
def compare(before_image: UploadFile = File(...), after_image: UploadFile = File(...)):
    """
    Compare before vs after vehicle images.
    Returns detected damages, severity, and estimated repair cost.
    """
    # Generate temporary unique filenames
    before_path = save_image(before_image.file.read(), f"{uuid.uuid4()}_before.jpg")
    after_path = save_image(after_image.file.read(), f"{uuid.uuid4()}_after.jpg")

    # Run YOLO comparison
    report = compare_images_and_report(before_path, after_path)
    return report
