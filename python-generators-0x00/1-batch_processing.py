
import mysql.connector


def connect_to_prodev():
 
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kabe@9168Clde",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None


def stream_users_in_batches(batch_size):

    try:
        # Connect to the database
        connection = connect_to_prodev()
        if not connection:
            return
        
        cursor = connection.cursor(dictionary=True)
        
        # Get total count of records
        cursor.execute("SELECT COUNT(*) as count FROM user_data")
        total_count = cursor.fetchone()['count']
        
        # Process in batches
        offset = 0
        while offset < total_count:
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            batch = cursor.fetchall()            
            if not batch:
                break
                
            yield batch
            offset += batch_size
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
        yield []

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 25]
        for user in filtered_users:
            print(user)
            print()