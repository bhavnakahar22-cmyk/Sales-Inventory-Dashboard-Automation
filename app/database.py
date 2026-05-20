import sqlite3


def create_connection():
    conn = sqlite3.connect('sales_inventory.db')
    return conn


def load_data_to_db(df, table_name):
    conn = create_connection()
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()