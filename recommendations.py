from database import connect_db


def generate_recommendations(findings):

    if not findings:
        return ["Please provide inspection findings."]

    text = findings.lower()
    recommendations = []

    rules = {
        "brake": "Brake system inspection",
        "tyre": "Tyre condition inspection",
        "tire": "Tyre condition inspection",
        "engine": "Engine diagnostic check",
        "battery": "Battery health check",
        "oil": "Engine oil level and condition check",
        "coolant": "Coolant system inspection",
        "suspension": "Suspension system inspection",
        "ac": "Air conditioning inspection",
        "light": "Vehicle lighting inspection"
    }

    for keyword, recommendation in rules.items():
        if keyword in text:
            recommendations.append(recommendation)

    if not recommendations:
        recommendations.append(
            "General vehicle inspection recommended"
        )

    return list(dict.fromkeys(recommendations))


def save_recommendations(inspection_id, recommendations):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inspection_id INTEGER,
            recommendation TEXT
        )
    """)

    for recommendation in recommendations:
        cursor.execute("""
            INSERT INTO recommendations
            (inspection_id, recommendation)
            VALUES (?, ?)
        """, (inspection_id, recommendation))

    conn.commit()
    conn.close()

    return True
