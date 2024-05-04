# How to run the application

## Prerequisites

1. **Install PostgreSQL**: Download and install PostgreSQL for your operating system from [here](https://www.postgresql.org/download/).

## Setup

1. **Create a PostgreSQL server**: Set up a PostgreSQL server and create a connection for the database.
   - Modify the `db_string` variable in `db_tables.py` if necessary. This variable stores the connection string containing credentials and information to connect to the database.
   - The `db_string` pattern is as follows:
     ```
     "database_type://user:password@database_url:port/database_name"
     ```
     Replace the placeholders with the appropriate values:
     - `database_type`: postgresql
     - `user`: Your PostgreSQL username
     - `password`: Your PostgreSQL password
     - `host`: localhost or your PostgreSQL server's hostname
     - `port`: 5432 or your PostgreSQL server's port
     - `database_name`: The name of your PostgreSQL database

## Running the Application

1. **Clone the repository**: Clone the repository to your local machine.
2. **Open the repository**: Use your preferred integrated development environment (IDE), such as Visual Studio Code.
3. **Install dependencies**: Open a terminal in the repository directory and run the following command to install all dependencies and Python (Python 3.11.6 was used) packages:
   ```
   python -m pip install -r requirements.txt
   ```
4. **Run data preprocessing**: Execute the `data_preprocessing.py` script to fetch all necessary data:
   ```
   python data_preprocessing.py
   ```
5. **Initialize the database and insert data**: Run the `insert_data_to_db.py` script to initialize the database schema and fill it with data:
   ```
   python insert_data_to_db.py
   ```
6. **Run the application**: Launch the application using Streamlit by running the following command:
   ```
   streamlit run app.py
   ```


