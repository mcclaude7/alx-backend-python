# import mysql.connector

# def stream_users_in_batches(batch_size):
#     connection = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='',
#         database='ALX_prodev'
#     )
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM user_data")

#     while True:
#         rows = cursor.fetchmany(batch_size)
#         if not rows:
#             break
#         yield rows  # ✅ Yield a batch

#     cursor.close()
#     connection.close()

# def batch_processing(batch_size):
#     for batch in stream_users_in_batches(batch_size):  # ✅ 1st loop
#         filtered_batch = (user for user in batch if user[3] > 25)  # ✅ generator expression (no extra loop)
#         yield list(filtered_batch)  # ✅ Yield filtered results (users with age > 25)
#!/usr/bin/python3
"""
Module for batch processing user data from MySQL database
"""

import mysql.connector


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL
    
    Returns:
        connection: MySQL connection object or None if connection fails
    """
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
    """
    Generator function that fetches rows from the user_data table in batches
    
    Args:
        batch_size: Number of records to fetch in each batch
        
    Yields:
        list: A batch of user records
    """
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
            
        # Clean up
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")
        yield []


def batch_processing(batch_size):
    """
    Processes batches of user data and prints users over age 25
    
    Args:
        batch_size: Number of records to fetch in each batch
    """
    # Get data batches from the stream generator
    for batch in stream_users_in_batches(batch_size):
        # Filter users over age 25
        filtered_users = [user for user in batch if user['age'] > 25]
        
        # Print each filtered user with a blank line between users
        for user in filtered_users:
            print(user)
            print()