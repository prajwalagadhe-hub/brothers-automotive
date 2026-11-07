from .database import connect_db


def add_service(service_name, description):

    if not service_name:
        return False, "Service name is required."

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO services (service_name, description)
            VALUES (?, ?)
        """, (service_name, description))

        conn.commit()
        return True, "Service added successfully!"

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def get_services():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()

    conn.close()

    return services