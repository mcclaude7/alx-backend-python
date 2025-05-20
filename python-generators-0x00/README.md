# MySQL CSV Seeder with Python

This project demonstrates how to use Python to:

- Connect to a MySQL server
- Create a database (`ALX_prodev`)
- Create a table (`user_data`)
- Insert data from a CSV file (`user_data.csv`)

## Features

- Connects to MySQL using `mysql.connector`
- Creates a database if it doesn't exist
- Creates a `user_data` table with the fields:
  - `user_id` (UUID, Primary Key)
  - `name`
  - `email`
  - `age`
- Imports user data from a CSV file
- Avoids duplicate data insertion

## Requirements

- Python 3.x
- MySQL Server
- Python packages:
  - `mysql-connector-python`

