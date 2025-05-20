import mysql.connector


def connect_to_prodev():
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None


def stream_user_ages():

    try:
        # Connect to the database
        connection = connect_to_prodev()
        if not connection:
            return
        
        cursor = connection.cursor()
        
        # Query to fetch only the age column to minimize memory usage
        cursor.execute("SELECT age FROM user_data")
        
        # Yield each age one by one
        for (age,) in cursor:
            yield age
            
        # Clean up
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error streaming ages: {err}")
        

def calculate_average_age():


    total_age = 0
    count = 0
    
    # Stream ages and calculate running sum and count
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    # Calculate and return the average
    average_age = total_age / count if count > 0 else 0
    return average_age


if __name__ == "__main__":
    # Calculate and print the average age
    avg_age = calculate_average_age()
    print(f"Average age of users: {avg_age}")