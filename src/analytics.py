from src.database import get_connection
import pandas as pd


def get_view_statistics():

    conn = get_connection()

    query = """
    SELECT product_name
    FROM view_history
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df