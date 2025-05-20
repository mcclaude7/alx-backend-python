import mysql.connector
import csv
import os
import uuid

 # Connect MySQL

def connect_db():
    try:
        connection= mysql.connector.connect(
            host='localhost',
            user='root',
            password='Kabe@9168Clde',
        )
        if connection.is_connected():
            print('Cnnected to MySql server')
            return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MYSQL server: {err}")
        return None
 # Create database (ALX_prodev)  
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS ALX_prodev')
        print('Database created or already exist')
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

 # Connect to the ALX_prodev database

# def connect_to_prodev():
#     try:
#         connection = mysql.connector.connect(
#             host = 'localhost',
#             user = 'root',
#             password = 'Kabe@9168Clde',
#             database = 'ALX_prodev'
#         )
#         return connection
    
#     except mysql.connector.Error as err:
#         print(f"Error connecting to ALX_prodev database: {err}")
#         return None
    
# def create_table(connection):
#     try:
#         cursor = connection.cursor()
#         cursor.execute(""" 
#                        CREATE TABLE IF NOT EXISTS user_data(
#                        user_id VARCHAR(36) PRIMARY KEY,
#                        name VARCHAR(250) NOT NULL,
#                        email VARCHAR(255) NOT NULL,
#                        age DECIMAL(5,0)NOT NULL,
#                        INDEX idx_user_id (user_id))
#                        """)
#         connection.commit()
#         cursor.close()
#         print('Table user_data created successfully')

#     except mysql.connector.Error as err:
#         print(f'Error creating table: {err}')

# def insert_data(connection, csv_file):
#     if not os.path.exists(csv_file):
#         print(f"Error: file {csv_file} does not exist")
#         return
#     try:
#         cursor = connection.cursor()
#         cursor.execute("SELECT COUNT(*) FROM user_data")
#         count = cursor.fetchone()[0]

#         if count > 0:
#             print(f"Data already exists in the table. {count} records found.")
#             return
        
#         with open(csv_file, 'r') as file:
#             csv_reader = csv.reader(file)
#             next(csv_reader)

#             for row in csv_reader:
#                 if len(row) >=4:
#                     try:
#                         user_id = str(uuid.UUID(row[0])) if row[0] else str(uuid.uuid4())
#                     except ValueError:
#                         user_id= str(uuid.uuid4())

#                     name = row[1]
#                     email = row[2]

#                     try:
#                         age = int(float(row[3]))
#                     except (ValueError, IndexError):
#                         age = 0

#                     cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (user_id))
#                     if not cursor.fetchone():
#                         cursor.execute(
#                             "INSERT INTO user_data(user_id, name, email, age) VALUES (%s, %s, %s, %s)",
#                             (user_id, name, email, age)
#                         )

#             connection.commit()
#             cursor.close()
#             print("Data inserted successfully")
#     except mysql.connector.Error as err:
#         print(f"Error inserting data: {err}")
#     except Exception as e:
#         print(f"Error processing CSV file: {e}")
    
# if __name__=="__main__":
#     # Connection:
    
#     # create_database(connection)
#     # connection.close()

#     connection = connect_to_prodev()
#     if connection:
#         create_table(connection)
#         insert_data(connection, 'user_data.csv')
#         connection.close()