from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="zohaib0099",
        database="mydatabase"
    )
    return conn

# Route: Get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# Route: Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data['name']
    email = data['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User added successfully"}), 201

# Route: Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (name, email, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User updated successfully"})

# Route: Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
