from src.database import get_connection


def add_reminder(product, date):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reminders
        (product_name, reminder_date)
        VALUES (?, ?)
        """,
        (product, date)
    )

    conn.commit()
    conn.close()


def get_reminders():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM reminders
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data