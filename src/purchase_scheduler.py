from src.database import get_connection


def schedule_purchase(product, date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO scheduled_purchases(
            product_name,
            purchase_date
        )
        VALUES(?,?)
        """,
        (product, date)
    )

    conn.commit()
    conn.close()


def get_scheduled_purchases():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM scheduled_purchases
        ORDER BY purchase_date
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data