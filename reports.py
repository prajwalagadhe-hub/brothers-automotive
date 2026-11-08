from database import connect_db


def get_all_inspection_reports():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            inspections.id,
            customers.name,
            vehicles.car_name,
            vehicles.model,
            inspections.findings,
            inspections.recommendations,
            inspections.inspection_date
        FROM inspections
        LEFT JOIN customers
            ON inspections.customer_id = customers.id
        LEFT JOIN vehicles
            ON inspections.vehicle_id = vehicles.id
        ORDER BY inspections.id DESC
    """)

    reports = cursor.fetchall()
    conn.close()

    return reports


def get_customer_report(customer_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM inspections
        WHERE customer_id = ?
        ORDER BY id DESC
    """, (customer_id,))

    reports = cursor.fetchall()
    conn.close()

    return reports
