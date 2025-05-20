import mysql.connector

def stream_users():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Kabe@9168Clde',
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row  # Yield each row one by one

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
