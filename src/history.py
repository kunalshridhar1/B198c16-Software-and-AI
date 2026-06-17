from src.database import get_connection


def add_view(product):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO view_history(product_name)
        VALUES(?)
        """,
        (product,)
    )

    conn.commit()
    conn.close()


def get_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT product_name, viewed_at
        FROM view_history
        ORDER BY viewed_at DESC
        LIMIT 10
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data