from pathlib import Path
from admin import admin
from database import connect_db, create_tables
from booking import delete_booking, create_booking, get_bookings
from customers import register_customer, get_customers
from vehicles import add_vehicle, get_vehicles
from services import add_service, get_services

import streamlit as st
import sqlite3
import os
from datetime import datetime

# ==========================================
# BROTHERS AUTOMOTIVE - MAIN CONFIGURATION
# ==========================================

import streamlit as st
import os

DB_PATH = "data/brothers_automotive.db"

os.makedirs("data", exist_ok=True)

st.set_page_config(
    page_title="Brothers Automotive",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>

/* Main website background */
.stApp {
    background-color: #000000;
    color: #FFFFFF;
}

/* All headings */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
}

/* Normal text */
p, label, span {
    color: #E5E5E5;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111111;
}

/* Buttons */
.stButton > button {
    background-color: #FFFFFF;
    color: #000000;
    border: 1px solid #FFFFFF;
    border-radius: 8px;
    font-weight: bold;
}

/* Button hover */
.stButton > button:hover {
    background-color: #CCCCCC;
    color: #000000;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    background-color: #1A1A1A;
    color: #FFFFFF;
    border: 1px solid #FFFFFF;
}

/* Links */
a {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

/* Navigation buttons */
.stButton > button {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 2px solid #FFFFFF !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    padding: 12px 20px !important;
    width: 100%;
    transition: 0.3s ease;
}

/* Hover effect */
.stButton > button:hover {
    background-color: #222222 !important;
    color: #FFFFFF !important;
    border: 2px solid #FFFFFF !important;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)

create_tables()

# ==========================================
# DATABASE
# ==========================================

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                car TEXT NOT NULL,
                service TEXT NOT NULL,
                date TEXT NOT NULL,
                message TEXT,
                created_at TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                message TEXT,
                created_at TEXT
            )
        """)


create_database()


# ==========================================
# PREMIUM BLACK & GOLD DESIGN
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');

.stApp {
    background-color: #090909;
    color: #F5F5F5;
    font-family: 'Montserrat', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 1.5rem;
    max-width: 1250px;
}

h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: #D4AF37 !important;
}

p, label, li {
    color: #E2E2E2;
}

[data-testid="stBaseButton-primary"] {
    background: linear-gradient(90deg, #A77B19, #F3D77A);
    color: #080808;
    border: none;
    border-radius: 6px;
    font-weight: 700;
}

.stButton button {
    border-radius: 6px;
    font-weight: 600;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stDateInput input {
    background-color: #171717;
    color: white;
    border: 1px solid #80631D;
}

.ba-header {
    text-align: center;
    padding: 18px 0 25px;
    border-bottom: 1px solid #80631D;
    margin-bottom: 25px;
}

.ba-logo {
    font-family: 'Cinzel', serif;
    font-size: 35px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #E2BD55;
}

.ba-subtitle {
    color: #BDBDBD;
    letter-spacing: 5px;
    font-size: 11px;
}

.hero {
    padding: 65px 30px;
    text-align: center;
    border: 1px solid #8B6B24;
    border-radius: 12px;
    background: linear-gradient(
        135deg, #191919, #080808, #29200D
    );
}

.hero h1 {
    font-size: 44px;
}

.hero p {
    font-size: 17px;
    color: #D0D0D0;
}

.service-card {
    background: #171717;
    border: 1px solid #55431C;
    padding: 23px;
    border-radius: 10px;
    min-height: 175px;
    margin-bottom: 15px;
}

.service-card h3 {
    font-size: 20px;
}

.gold-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #D4AF37, transparent);
    margin: 25px 0;
}

.footer {
    border-top: 1px solid #55431C;
    text-align: center;
    padding: 25px;
    color: #AFAFAF;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# COMMON HEADER
# ==========================================

def header():
    st.markdown("""
    <div class="ba-header">
        <div class="ba-logo">BROTHERS AUTOMOTIVE</div>
        <div class="ba-subtitle">PREMIUM AUTOMOTIVE CARE</div>
    </div>
    """, unsafe_allow_html=True)


def footer():
    st.markdown("""
    <div class="footer">
        <h3>BROTHERS AUTOMOTIVE</h3>
        Premium Care. Professional Service.
        <br><br>
        © 2026 Brothers Automotive. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HOME PAGE
# ==========================================

def home():

    header()

    st.markdown("""
    <div class="hero">
        <h1>DRIVE WITH CONFIDENCE</h1>
        <p>
            Experience premium automotive care,
            intelligent car inspection and
            professional vehicle services.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-line"></div>',
                unsafe_allow_html=True)

    st.subheader("WELCOME TO BROTHERS AUTOMOTIVE")

    st.write("""
    We bring professional automotive services together
    with modern technology to help customers care for
    their vehicles.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="service-card">
        <h3>01. Premium Care</h3>
        <p>Professional detailing, polishing and vehicle care.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="service-card">
        <h3>02. AI Inspection</h3>
        <p>Upload a car image and get inspection assistance
        and care recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="service-card">
        <h3>03. Easy Booking</h3>
        <p>Request your preferred automotive service online.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gold-line"></div>',
                unsafe_allow_html=True)

    st.subheader("WHY CHOOSE US?")

    a, b, c = st.columns(3)

    a.write("✓ Professional Service")
    b.write("✓ Modern Technology")
    c.write("✓ Customer Satisfaction")

    footer()


# ==========================================
# SERVICES PAGE
# ==========================================
def services():

    header()

    # =====================================
    # SERVICE PAGE DESIGN
    # =====================================

    st.markdown("""
    <style>

    .service-heading {
        text-align: center;
        color: #D4AF37;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .service-subheading {
        text-align: center;
        color: #cccccc;
        font-size: 17px;
        margin-bottom: 35px;
    }

    .service-card {
        background: #151515;
        border: 1px solid #B89635;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        min-height: 150px;
        margin-bottom: 25px;
    }

    .service-card h2 {
        color: #D4AF37;
        font-size: 25px;
    }

    .service-card h3 {
        color: #D4AF37;
        font-size: 21px;
    }

    .service-card p {
        color: #eeeeee;
        font-size: 15px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="service-heading">OUR SERVICES</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="service-subheading">'
        'Premium Automotive Care & Protection'
        '</div>',
        unsafe_allow_html=True
    )

    # =====================================
    # SERVICE LIST
    # =====================================

    service_list = [
        ("🚗", "Car Washing",
         "Exterior cleaning and interior cleaning."),

        ("💎", "Car Coating",
         "Paint protection and enhanced surface finish."),

        ("✨", "Car Detailing",
         "Detailed interior and exterior vehicle care."),

        ("🌟", "Car Polishing",
         "Paint finishing and surface enhancement."),

        ("🛡️", "Paint Protection",
         "Vehicle paint protection solutions."),

        ("🔧", "General Maintenance",
         "Routine vehicle maintenance and inspection.")
    ]

    # =====================================
    # LOAD IMAGES FROM GITHUB IMAGES FOLDER
    # =====================================

    image_folder = Path(__file__).parent / "images"

    image_files = []

    if image_folder.exists():
        image_files = sorted([
            f for f in image_folder.iterdir()
            if f.suffix.lower() in
            [".jpg", ".jpeg", ".png", ".webp"]
        ])

    # Match available images by filename
    image_keywords = {
        "Car Washing": ["carwash", "wash"],
        "Car Coating": ["coating", "ceramic"],
        "Car Detailing": ["detailing", "detail"],
        "Car Polishing": ["polishing", "polish"],
        "Paint Protection": ["protection", "paint"],
        "General Maintenance": ["repair", "maintenance"]
    }

    used_images = set()

    # =====================================
    # DISPLAY SERVICE CARDS
    # =====================================

    for i in range(0, len(service_list), 3):

        cols = st.columns(3)

        for j, col in enumerate(cols):

            index = i + j

            if index < len(service_list):

                icon, name, description = service_list[index]

                with col:

                    keywords = image_keywords.get(name, [])

                    photo = next(
                        (
                            file for file in image_files
                            if file not in used_images
                            and any(
                                word in file.name.lower()
                                for word in keywords
                            )
                        ),
                        None
                    )

                    # Use another available image if no match
                    if photo is None:
                        photo = next(
                            (
                                file for file in image_files
                                if file not in used_images
                            ),
                            None
                        )

                    if photo:
                        used_images.add(photo)

                        st.image(
                            str(photo),
                            use_container_width=True
                        )
                    else:
                        st.info("Service image coming soon")

                    st.markdown(f"""
                    <div class="service-card">
                        <h2>{icon}</h2>
                        <h3>{name}</h3>
                        <p>{description}</p>
                    </div>
                    """, unsafe_allow_html=True)

    # =====================================
    # FOOTER
    # =====================================

    st.markdown("""
    <div style="
        text-align:center;
        padding:25px;
        color:#D4AF37;
        border-top:1px solid #B89635;
        margin-top:25px;
    ">
        <h3>BROTHERS AUTOMOTIVE</h3>
        <p>Professional Care. Premium Protection.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# AI CAR INSPECTION PAGE
# ==========================================

def ai_inspection():

    header()

    st.title("AI CAR INSPECTION")

    st.write("""
    Upload your vehicle photograph and provide
    information about its condition.
    """)

    uploaded_image = st.file_uploader(
        "Upload vehicle photograph",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:

        st.image(
            uploaded_image,
            caption="Uploaded Vehicle",
            use_container_width=True
        )

    st.markdown('<div class="gold-line"></div>',
                unsafe_allow_html=True)

    st.subheader("Vehicle Information")

    car_type = st.selectbox(
        "Vehicle type",
        ["Hatchback", "Sedan", "SUV", "Luxury Car", "Other"]
    )

    symptoms = st.multiselect(
        "Select the conditions you have noticed",
        [
            "Dull paint",
            "Minor visible scratches",
            "Dust and dirt",
            "Water spots",
            "Interior stains",
            "Faded exterior finish",
            "No visible issue"
        ]
    )

    if st.button("GET CARE RECOMMENDATIONS",
                 type="primary"):

        if not uploaded_image:
            st.warning("Please upload a vehicle photograph.")

        elif not symptoms:
            st.warning("Please select at least one condition.")

        else:

            st.success("Inspection assistance generated.")

            st.subheader("Recommended Services")

            recommendations = {
                "Dull paint": "Car polishing",
                "Minor visible scratches": "Professional paint assessment",
                "Dust and dirt": "Car washing and detailing",
                "Water spots": "Exterior detailing",
                "Interior stains": "Interior deep cleaning",
                "Faded exterior finish": "Paint condition assessment",
                "No visible issue": "Routine maintenance inspection"
            }

            for symptom in symptoms:

                st.markdown(
                    f"✓ **{symptom}:** "
                    f"{recommendations[symptom]}"
                )

            st.info("""
            This is a preliminary, rule-based recommendation
            tool, not an actual AI image diagnosis.
            A professional inspection is needed to confirm
            vehicle condition and service requirements.
            """)

    footer()


# ==========================================
# BOOKING PAGE
# ==========================================

def booking():

    header()

    st.title("BOOK YOUR SERVICE")

    st.write("Fill in your details to request an appointment.")

    with st.form("booking_form"):

        name = st.text_input("Customer Name")

        phone = st.text_input("Mobile Number")

        car = st.text_input("Car Model")

        service = st.selectbox(
            "Select Service",
            [
                "Car Washing",
                "Car Detailing",
                "Ceramic Coating",
                "Car Polishing",
                "Paint Protection",
                "General Maintenance"
            ]
        )

        date = st.date_input("Preferred Appointment Date")

        message = st.text_area("Additional Requirements")

        submitted = st.form_submit_button(
            "SUBMIT BOOKING",
            type="primary"
        )

        if submitted:

            if not name.strip() or not phone.strip() or not car.strip():
                st.error("Please complete all required fields.")

            elif not phone.strip().isdigit() or len(phone.strip()) != 10:
                st.error("Enter a valid 10-digit mobile number.")

            elif date < datetime.today().date():
                st.error("Please select a future appointment date.")

            else:

                with get_connection() as conn:

                    conn.execute("""
                        INSERT INTO bookings
                        (name, phone, car, service, date, message, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        name.strip(),
                        phone.strip(),
                        car.strip(),
                        service,
                        str(date),
                        message.strip(),
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ))

                st.success(
                    "Your booking request has been submitted successfully!"
                )

    footer()


# ==========================================
# ABOUT US PAGE
# ==========================================

def about():

    header()

    st.title("ABOUT BROTHERS AUTOMOTIVE")

    st.write("""
    Brothers Automotive aims to provide professional
    vehicle care and modern automotive solutions.

    Our goal is to combine quality services, customer
    convenience and innovative technology.

    We focus on:

    - Professional vehicle care
    - Quality workmanship
    - Customer satisfaction
    - Modern automotive solutions
    - Convenient online service requests
    """)

    st.markdown('<div class="gold-line"></div>',
                unsafe_allow_html=True)

    st.subheader("OUR VISION")

    st.write("""
    To build a trusted automotive service brand
    known for quality, innovation and customer care.
    """)

    footer()


# ==========================================
# CONTACT PAGE
# ==========================================
def contact():

    import streamlit as st
    import urllib.parse

    st.title("Contact Brothers Automotive")

    st.write("We are here to help you!")

    # CONTACT DETAILS
    st.subheader("Get In Touch")

    st.write("📍 Address:Sangamner-Akole road,near manas beer bar and restro Tel-sangamner 422605")
    st.write("📞 Phone:7558492095 ")
    st.write("✉️ Email: brothersautomotive@email.com")

    st.markdown("---")

    # CONTACT FORM
    st.subheader("Send Us a Message")

    with st.form("contact_form"):

        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")

        submitted = st.form_submit_button("Send Message")

        if submitted:
            if name and email and message:
                st.success("Thank you! Your message has been received.")
            else:
                st.warning("Please fill all fields.")

    st.markdown("---")

    # WHATSAPP CHAT
    st.subheader("Chat With Us on WhatsApp")

    st.write(
        "Need quick assistance? "
        "Connect with Brothers Automotive directly."
    )

    WHATSAPP_NUMBER = "7558492095"

    MESSAGE = (
        "Hello Brothers Automotive! "
        "I would like to enquire about your services."
    )

    whatsapp_url = (
        "https://wa.me/"
        + WHATSAPP_NUMBER
        + "?text="
        + urllib.parse.quote(MESSAGE)
    )

    st.link_button(
        "💬 Chat on WhatsApp",
        whatsapp_url,
        use_container_width=True
    )

# ==========================================
# ADMIN DASHBOARD
# ==========================================

def admin():

    header()

    st.title("ADMIN DASHBOARD")

    st.write("Authorized business administration only.")

    if not st.session_state.get("admin_authenticated", False):

        password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button("LOGIN", type="primary"):

            admin_password = os.getenv("BA_ADMIN_PASSWORD", "prajwala@123")

            if admin_password and password == admin_password:

                st.session_state.admin_authenticated = True
                st.rerun()

            else:
                st.error("Invalid password or admin password not configured.")

        footer()
        return

    if st.button("LOGOUT"):
        st.session_state.admin_authenticated = False
        st.rerun()

    with get_connection() as conn:

        bookings = conn.execute("""
            SELECT id, name, phone, car, service, date, message
            FROM bookings ORDER BY id DESC
        """).fetchall()

        messages = conn.execute("""
            SELECT id, name, email, message, created_at
            FROM messages ORDER BY id DESC
        """).fetchall()

    st.subheader("Booking Statistics")

    col1, col2 = st.columns(2)

    col1.metric("Total Bookings", len(bookings))
    col2.metric("Customer Messages", len(messages))

    st.markdown('<div class="gold-line"></div>',
                unsafe_allow_html=True)

    st.subheader("Customer Bookings")

    if bookings:

        booking_data = [
            {
                "ID": row[0],
                "Name": row[1],
                "Phone": row[2],
                "Car": row[3],
                "Service": row[4],
                "Date": row[5],
                "Message": row[6]
            }
            for row in bookings
        ]

        st.dataframe(
            booking_data,
            use_container_width=True,
            hide_index=True
        )
         # BOOKING MANAGEMENT
        st.subheader("Manage Bookings")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check booking table columns
        cursor.execute("PRAGMA table_info(bookings)")
        columns = [col[1] for col in cursor.fetchall()]

        # Add status column if missing
        if "status" not in columns:
            cursor.execute("""
                ALTER TABLE bookings
                ADD COLUMN status TEXT DEFAULT 'Pending'
            """)
            conn.commit()

        id_col = "id" if "id" in columns else "booking_id"

        booking_ids = [row[0] for row in bookings]

        selected_id = st.selectbox(
            "Select Booking ID",
            booking_ids
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Confirm Booking"):
                cursor.execute(
                    f"UPDATE bookings SET status=? WHERE {id_col}=?",
                    ("Confirmed", selected_id)
                )
                conn.commit()
                st.success("Booking confirmed!")
                conn.close()
                st.rerun()

        with col2:
            confirm_delete = st.checkbox(
                "I want to delete this booking"
            )

            if st.button("Delete Booking"):
                if confirm_delete:
                    cursor.execute(
                        f"DELETE FROM bookings WHERE {id_col}=?",
                        (selected_id,)
                    )
                    conn.commit()
                    st.success("Booking deleted!")
                    conn.close()
                    st.rerun()
                else:
                    st.warning("Please confirm deletion first.")

        conn.close()

    st.subheader("Customer Messages")

    if messages:

        message_data = [
            {
                "ID": row[0],
                "Name": row[1],
                "Email": row[2],
                "Message": row[3],
                "Date": row[4]
            }
            for row in messages
        ]

        st.dataframe(
            message_data,
            use_container_width=True,
            hide_index=True
        )
        # DELETE CUSTOMER MESSAGE
        st.subheader("Manage Customer Messages")

        if messages:
            message_ids = [row[0] for row in messages]

            selected_message_id = st.selectbox(
                "Select Message ID to Delete",
                message_ids,
                key="delete_message_id"
            )

            confirm_message_delete = st.checkbox(
                "Confirm message deletion",
                key="confirm_message_delete"
            )

            if st.button("🗑️ Delete Message"):
                if confirm_message_delete:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()

                    cursor.execute(
                        "DELETE FROM messages WHERE id = ?",
                        (selected_message_id,)
                    )

                    conn.commit()
                    conn.close()

                    st.success("Message deleted successfully!")
                    st.rerun()
                else:
                    st.warning("Please confirm before deleting.")
        else:
            st.info("No customer messages available.")
    else:
        st.info("No customer messages available.")

    footer()


# ==========================================
# WEBSITE NAVIGATION
# ==========================================

pages = [
    st.Page(home, title="Home", icon="🏠", default=True),
    st.Page(services, title="Services", icon="🚘"),
    st.Page(ai_inspection, title="AI Inspection", icon="🤖"),
    st.Page(booking, title="Book a Service", icon="📅"),
    st.Page(about, title="About Us", icon="ℹ️"),
    st.Page(contact, title="Contact Us", icon="📞"),
    st.Page(admin, title="Admin", icon="🔐")
]

selected_page = st.navigation(
    pages,
    position="top"
)

st.markdown("""
<style>

/* Navigation buttons */
.stButton > button {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 2px solid #FFFFFF !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    padding: 12px 20px !important;
    width: 100%;
    transition: 0.3s ease;
}

/* Hover effect */
.stButton > button:hover {
    background-color: #222222 !important;
    color: #FFFFFF !important;
    border: 2px solid #FFFFFF !important;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)

selected_page.run()

