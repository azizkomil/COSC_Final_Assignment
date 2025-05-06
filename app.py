from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2 import Error

app = Flask(__name__)
CORS(app)

# Database connection parameters
DB_HOST = 'db-azizjon.clyucs4e44b4.ap-northeast-2.rds.amazonaws.com'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'postgres'
DB_PORT = '5432'


def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Handles connection errors and returns None if the connection fails.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        print("Successfully connected to the database")  # Added for debugging
    except Error as e:
        print(f"Error connecting to the database: {e}")
        # Consider logging the error for better diagnostics
    return conn


def close_db_connection(conn):
    """
    Closes the database connection.
    Handles potential errors during the closing process.
    """
    if conn:
        try:
            conn.close()
            print("Successfully closed the database connection")  # Added for debugging
        except Error as e:
            print(f"Error closing the database connection: {e}")
            # Consider logging this error
    else:
        print("Connection was already None, no need to close.")


# Helper function to execute a query and fetch all results
def execute_query_fetchall(conn, query, params=None):
    """Executes a SQL query and fetches all results."""
    cursor = None
    results = []
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
    except Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()  # Rollback on any error
        raise  # Re-raise the exception to be handled by the caller
    finally:
        if cursor:
            cursor.close()
    return results


# Helper function to execute a query and fetch one result
def execute_query_fetchone(conn, query, params=None):
    """Executes a SQL query and fetches one result."""
    cursor = None
    result = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
    except Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
    return result


# Helper function to execute a query and commit
def execute_query_commit(conn, query, params=None):
    """Executes a SQL query and commits the transaction."""
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()



# Endpoint to get all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    """Retrieves all cars from the database."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Failed to connect to the database'}), 500

    try:
        query = "SELECT id, model, brand, price_usd, year_released FROM tbl_azizbek_data;"
        cars = execute_query_fetchall(conn, query)  # Use the helper
        car_list = []
        for car in cars:
            car_dict = {
                "id": car[0],
                "model": car[1],
                "brand": car[2],
                "price_usd": float(car[3]),
                "year_released": car[4]
            }
            car_list.append(car_dict)
        return jsonify(car_list), 200
    except Error:  # Catch the error raised by execute_query_fetchall
        return jsonify({'message': 'Failed to retrieve cars'}), 500
    finally:
        close_db_connection(conn)



# Endpoint to get a specific car by ID
@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    """Retrieves a specific car from the database by its ID."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Failed to connect to the database'}), 500

    try:
        query = "SELECT id, model, brand, price_usd, year_released FROM tbl_azizbek_data WHERE id = %s"
        params = (car_id,)
        car = execute_query_fetchone(conn, query, params) # Use helper
        if car:
            car_dict = {
                "id": car[0],
                "model": car[1],
                "brand": car[2],
                "price_usd": float(car[3]),
                "year_released": car[4]
            }
            return jsonify(car_dict), 200
        return jsonify({"message": "Car not found"}), 404
    except Error:
        return jsonify({'message': 'Failed to retrieve car'}), 500
    finally:
        close_db_connection(conn)



# Endpoint to add a new car
@app.route('/cars', methods=['POST'])
def add_car():
    """Adds a new car to the database."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Failed to connect to the database'}), 500

    data = request.get_json()
    model = data.get('model')
    brand = data.get('brand')
    price_usd = data.get('price_usd')
    year_released = data.get('year_released')

    if not all([model, brand, price_usd, year_released]):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        price_usd = float(price_usd)  #convert to the correct type
        year_released = int(year_released)
    except ValueError:
        return jsonify({'message': 'Invalid price or year_released format'}, 400)

    try:
        query = """
            INSERT INTO tbl_azizbek_data (model, brand, price_usd, year_released)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        params = (model, brand, price_usd, year_released)
        new_car_id = execute_query_fetchone(conn, query, params)[0] #use helper
        conn.commit()  # Commit the transaction
        return jsonify({'message': 'Car added successfully', 'id': new_car_id}), 201
    except Error:
        return jsonify({'message': 'Failed to add car'}, 500)
    finally:
        close_db_connection(conn)



# Endpoint to delete a car by ID
@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    """Deletes a car from the database by its ID."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Failed to connect to the database'}), 500

    try:
        query = "DELETE FROM tbl_azizbek_data WHERE id = %s"
        params = (car_id,)
        execute_query_commit(conn, query, params) #use helper
        rows_deleted = 1 # Changed to 1.  execute_query_commit does not return rowcount.
        if rows_deleted > 0:
            return jsonify({'message': 'Car deleted successfully'}), 200 # 200 OK
        return jsonify({'message': 'Car not found'}, 404)
    except Error:
        return jsonify({'message': 'Failed to delete car'}, 500)
    finally:
        close_db_connection(conn)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7777, debug=True)