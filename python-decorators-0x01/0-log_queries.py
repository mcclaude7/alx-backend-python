import mysql.connector
import functools
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='database_queries.log'
)

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query from the first argument
        query = args[0] if args else "Unknown query"
        
        # Log the query
        logging.info(f"Executing query: {query}")
        
        try:
            # Execute the original function
            result = func(*args, **kwargs)
            logging.info(f"Query executed successfully")
            return result
        except Exception as e:
            # Log any errors that occur during query execution
            logging.error(f"Query failed: {str(e)}")
            raise
    
    return wrapper

@log_queries
def fetch_all_users(query):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="your_username",  # Replace with your MySQL username
        password="your_password",  # Replace with your MySQL password
        database="users_db"  # Replace with your database name
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    try:
        users = fetch_all_users(query="SELECT * FROM users")
        print(users)
    except Exception as e:
        print(f"Error: {str(e)}")