from .database import connect_db


def add_vehicle(customer_id, car_name, model, registration_number):

    if not car_name or not registration_number:
        return False, "Vehicle details are required."

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO vehicles
            (customer_id, car_name, model, registration_number)
            VALUES (?, ?, ?, ?)
        """, (customer_id, car_name, model, registration_number))

        conn.commit()
        return True, "Vehicle added successfully!"

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def get_vehicles(customer_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM vehicles WHERE customer_id = ?",
        (customer_id,)
    )

    vehicles = cursor.fetchall()
    conn.close()

    return vehicles