from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import database
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Path to the SQLite database
DATABASE_PATH = 'C:\\Users\\Bongeka.Mpofu\\DB Browser for SQLite\\flight.db'

# Function to initialize the database (run this once to set up the database schema)
def init_db():
    if not os.path.exists(DATABASE_PATH):
        with app.app_context():
            # Assuming you have a function in `database` module that creates tables
            database.create_tables(DATABASE_PATH)
            print("Database created successfully.")
    else:
        print("Database already exists.")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        email_address = request.form.get('email_address')
        address = request.form.get('address')

        print(f"Received Data: {first_name}, {second_name}, {last_name}, {phone_number}, {email_address}, {address}")

        try:
            database.add_passenger(DATABASE_PATH, first_name, second_name, last_name, phone_number, email_address, address)
            print("Database insertion attempted.")
        except Exception as e:
            print(f"Error in database insertion: {e}")

        return redirect(url_for('index'))
    return render_template('Customer_details.html')

@app.route('/save_customer_data', methods=['POST'])
def save_customer_data():
    try:
        # Get JSON data from the request
        data = request.get_json()
        print("Request received:", data)

        # Extract individual fields from the JSON data
        first_name = data.get('first_name')
        second_name = data.get('second_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')
        email_address = data.get('email_address')
        address = data.get('address')

        print(first_name, second_name)

        # Validate JSON data
        if not all([first_name, second_name, last_name, phone_number, email_address, address]):
            return jsonify({"error": "All fields are required!"}), 400

        # Save to the database
        database.add_passenger(DATABASE_PATH, first_name, second_name, last_name, phone_number, email_address, address)

        # Return a success response
        return jsonify({"message": "Customer data successfully saved to the database!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    # Initialize the database when the app runs
    init_db()
    app.run(debug=True)
