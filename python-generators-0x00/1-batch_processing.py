import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows  # 👈 Yield a batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # 1st loop
        filtered = [user for user in batch if user[3] > 25]  # user[3] = age (index in tuple)
        yield filtered  # 👈 Yield only users older than 25
