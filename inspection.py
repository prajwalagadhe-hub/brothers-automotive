from pathlib import Path
from uuid import uuid4
from database import connect_db

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads" / "inspections"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def save_inspection(
    customer_id,
    vehicle_id,
    uploaded_file,
    findings,
    recommendations,
    inspection_date
):
    if not customer_id or not vehicle_id or not uploaded_file:
        return False, "Required inspection details are missing."

    extension = Path(uploaded_file.name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return False, "Only JPG, JPEG, PNG and WEBP images are allowed."

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}{extension}"
    image_path = UPLOAD_DIR / filename

    try:
        image_path.write_bytes(uploaded_file.getvalue())

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO inspections (
                customer_id,
                vehicle_id,
                image_path,
                findings,
                recommendations,
                inspection_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            vehicle_id,
            str(image_path.relative_to(BASE_DIR)),
            findings,
            recommendations,
            inspection_date
        ))

        conn.commit()
        conn.close()

        return True, "Inspection saved successfully!"

    except Exception as error:
        if image_path.exists():
            image_path.unlink()

        return False, str(error)


def get_inspections(customer_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM inspections
        WHERE customer_id = ?
        ORDER BY id DESC
    """, (customer_id,))

    records = cursor.fetchall()
    conn.close()

    return records
