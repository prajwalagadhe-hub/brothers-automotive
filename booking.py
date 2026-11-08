from database import connect_db


def create_booking(customer_id, vehicle_id, service_name, booking_date):

    if not customer_id or not vehicle_id or not service_name:
        return False, "Please provide all booking details."

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO bookings
            (customer_id, vehicle_id, service_name, booking_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            customer_id,
            vehicle_id,
            service_name,
            booking_date,
            "Pending"
        ))

        conn.commit()
        return True, "Booking created successfully!"

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def get_bookings(customer_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM bookings
        WHERE customer_id = ?
        ORDER BY id DESC
    """, (customer_id,))

    bookings = cursor.fetchall()
    conn.close()

    return bookings

def delete_booking(booking_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bookings WHERE id = ?",
        (booking_id,)
    )

    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    return deleted


def update_booking_status(booking_id, status):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE bookings
        SET status = ?
        WHERE id = ?
    """, (status, booking_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0
