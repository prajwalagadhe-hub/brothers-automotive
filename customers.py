from .database import connect_db


def register_customer(name, phone, email):

    if not name or not phone:
        return False, "Name and phone are required."

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO customers (name, phone, email)
            VALUES (?, ?, ?)
        """, (name, phone, email))

        conn.commit()
        return True, "Customer registered successfully!"

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def get_customers():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    conn.close()

    return customers