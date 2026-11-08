import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "brothers_automotive.db"


def connect_admin_db():
    return sqlite3.connect(DB_PATH)


def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'


def get_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """)
    return [row[0] for row in cursor.fetchall()]


def get_columns(conn, table):
    cursor = conn.cursor()
    cursor.execute(
        f"PRAGMA table_info({quote_identifier(table)})"
    )
    return [row[1] for row in cursor.fetchall()]


def find_table(tables, keywords):
    for table in tables:
        if table.lower() in keywords:
            return table

    for table in tables:
        if any(word in table.lower() for word in keywords):
            return table

    return None


def get_count(conn, table):
    if not table:
        return 0

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT COUNT(*) FROM {quote_identifier(table)}"
    )
    return cursor.fetchone()[0]


# ==========================================
# ADMIN DASHBOARD
# ==========================================

def admin():

    st.title("Brothers Automotive")
    st.subheader("Admin Dashboard")

    st.markdown("---")

    if not DB_PATH.exists():
        st.error(f"Database not found: {DB_PATH}")
        return

    try:
        conn = connect_admin_db()

        tables = get_tables(conn)

        if not tables:
            st.warning("No database tables found.")
            conn.close()
            return

        # Find existing database tables
        customer_table = find_table(
            tables, ["customers", "customer", "users", "user"]
        )

        booking_table = find_table(
            tables, ["bookings", "booking", "appointments", "appointment"]
        )

        service_table = find_table(
            tables, ["services", "service"]
        )

        # ==================================
        # BUSINESS OVERVIEW
        # ==================================

        st.header("Business Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Customers",
                get_count(conn, customer_table)
            )

        with col2:
            st.metric(
                "Total Bookings",
                get_count(conn, booking_table)
            )

        with col3:
            st.metric(
                "Total Services",
                get_count(conn, service_table)
            )

        st.markdown("---")

        # ==================================
        # BOOKING MANAGEMENT
        # ==================================

        st.header("Booking Management")

        if booking_table:

            columns = get_columns(conn, booking_table)

            id_col = next(
                (c for c in columns
                 if c.lower() in ["id", "booking_id"]),
                None
            )

            status_col = next(
                (c for c in columns
                 if c.lower() in ["status", "booking_status"]),
                None
            )
            if not status_col:
               conn.execute(
                 f'ALTER TABLE "{booking_table}" '
                 'ADD COLUMN status TEXT DEFAULT "Pending"'
            )
            conn.commit()
            status_col = "status"

            # Add status column if it does not exist
            if not status_col:
                conn.execute(
                    f"ALTER TABLE {quote_identifier(booking_table)} "
                    "ADD COLUMN status TEXT DEFAULT 'Pending'"
                )
                conn.commit()
                status_col = "status"

            if not id_col:
                st.error("Booking ID column not found.")

            else:

                bookings = pd.read_sql_query(
                    f"SELECT * FROM {quote_identifier(booking_table)}",
                    conn
                )

                if bookings.empty:
                    st.info("No bookings available.")

                else:

                    st.dataframe(
                        bookings,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.markdown("### Manage Selected Booking")

                    booking_ids = bookings[id_col].tolist()

                    selected_id = st.selectbox(
                        "Select Booking ID",
                        booking_ids,
                        key="admin_booking_select"
                    )

                    selected_booking = bookings[
                        bookings[id_col] == selected_id
                    ].iloc[0]

                    st.write(
                        "Current Status:",
                        selected_booking[status_col]
                    )

                    col1, col2 = st.columns(2)

                    # CONFIRM BOOKING
                    with col1:

                        if st.button(
                            "Confirm Booking",
                            use_container_width=True,
                            key="confirm_booking"
                        ):

                            conn.execute(
                                f"""
                                UPDATE {quote_identifier(booking_table)}
                                SET {quote_identifier(status_col)} = ?
                                WHERE {quote_identifier(id_col)} = ?
                                """,
                                ("Confirmed", selected_id)
                            )

                            conn.commit()

                            st.session_state["booking_message"] = (
                                "Booking confirmed successfully!"
                            )

                            st.session_state.pop(
                                "delete_booking_id", None
                            )

                            st.rerun()

                    # DELETE BOOKING
                    with col2:

                        if st.button(
                            "Delete Booking",
                            use_container_width=True,
                            key="delete_booking"
                        ):

                            st.session_state["delete_booking_id"] = (
                                selected_id
                            )

                    # DELETE CONFIRMATION
                    if "delete_booking_id" in st.session_state:

                        delete_id = st.session_state[
                            "delete_booking_id"
                        ]

                        st.warning(
                            f"Are you sure you want to delete booking "
                            f"{delete_id}?"
                        )

                        yes_col, no_col = st.columns(2)

                        with yes_col:

                            if st.button(
                                "Yes, Delete Permanently",
                                key="yes_delete"
                            ):

                                conn.execute(
                                    f"""
                                    DELETE FROM {quote_identifier(booking_table)}
                                    WHERE {quote_identifier(id_col)} = ?
                                    """,
                                    (delete_id,)
                                )

                                conn.commit()

                                st.session_state.pop(
                                    "delete_booking_id", None
                                )

                                st.session_state["booking_message"] = (
                                    "Booking deleted successfully!"
                                )

                                st.rerun()

                        with no_col:

                            if st.button(
                                "Cancel",
                                key="cancel_delete"
                            ):

                                st.session_state.pop(
                                    "delete_booking_id", None
                                )

                                st.rerun()

        else:
            st.warning("Booking table not found in database.")

        if "booking_message" in st.session_state:
            st.success(st.session_state.pop("booking_message"))

        st.markdown("---")

        # ==================================
        # CUSTOMER MANAGEMENT
        # ==================================

        st.header("Customer Management")

        if customer_table:

            customers = pd.read_sql_query(
                f"SELECT * FROM {quote_identifier(customer_table)}",
                conn
            )

            st.dataframe(
                customers,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("Customer table not found.")

        st.markdown("---")

        # ==================================
        # SERVICE MANAGEMENT
        # ==================================

        st.header("Service Management")

        if service_table:

            services = pd.read_sql_query(
                f"SELECT * FROM {quote_identifier(service_table)}",
                conn
            )

            st.dataframe(
                services,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("Service table not found.")

        st.markdown("---")

        # ==================================
        # DATABASE TABLE VIEWER
        # ==================================

        st.header("Database Management")

        selected_table = st.selectbox(
            "Select Database Table",
            tables,
            key="admin_table_select"
        )

        if st.button("View Table Records"):

            records = pd.read_sql_query(
                f"SELECT * FROM {quote_identifier(selected_table)}",
                conn
            )

            st.dataframe(
                records,
                use_container_width=True,
                hide_index=True
            )

        conn.close()

    except Exception as e:

        try:
            conn.close()
        except Exception:
            pass

        st.error(f"Admin Dashboard Error: {e}")
