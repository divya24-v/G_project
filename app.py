from flask import Flask,render_template,jsonify, request

import sqlite3
 

app = Flask(__name__)
DATABASE = 'C:/Users/DIVYA DUSHMAN/Downloads/josler.sqlite3'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM users;')
    data = cursor.fetchall()
    conn.close()
    return jsonify({'data': [dict(row) for row in data]})

@app.route('/api/data/<int:data_id>', methods=['GET'])
def get_single_data(data_id):
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM users WHERE id = ?;', (data_id,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return jsonify(dict(data))
    else:
        return jsonify({'error': 'Data not found'}), 404

#organization


@app.route('/api/data/organization', methods=['GET'])
def get_data_Organization():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM employees;')
    data = cursor.fetchall()
    conn.close()
    return jsonify({'data': [dict(row) for row in data]})

@app.route('/api/data/organization/<int:data_id>', methods=['GET'])
def get_single_data_Organization(data_id):
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM employees WHERE employees_id = ?;', (data_id,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return jsonify(dict(data))
    else:
        return jsonify({'error': 'Data not found'}), 404

import hashlib

@app.route('/api/data/insert', methods=['GET'])
def add_user():
    try:
        conn = get_db_connection()

        name = request.args.get('name')
        user_id = request.args.get('user_id')
        phone = request.args.get('phone')
        password = request.args.get('password')
        organization_id = request.args.get('organization_id')
        role = request.args.get('role')
        accessiblity = request.args.get('accessibility')
        allocated_area = request.args.get('allocated_area')

        if not all([name, user_id, phone, password, organization_id, role, accessiblity, allocated_area]):
            return jsonify({"error": "Missing required fields"}), 400

        cursor = conn.execute("""INSERT INTO `users` (`id`,`name`, `user_id`, `phone`, `password`, `organization_id`, `role`, `accessiblity`, `allocated_area`) 
                                VALUES (1,'divya',123,7564232321,123,1234,'user','platform','ahemdabad')""")
        conn.commit()

        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/data/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    try:
        conn = get_db_connection()

        cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({"error": "User not found"}), 404

        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/update/<int:user_id>', methods=['GET'])
def update_user(user_id):
    try:
        conn = get_db_connection()

        cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({"error": "User not found"}), 404

        # Update user data with new_data, if provided
        conn.execute("UPDATE users SET allocated_area = 'maninagar' WHERE id = ?", (user_id,))
        conn.commit()

        return jsonify({"message": "User data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/data/orgnazation/insert', methods=['GET'])
def add_orgnazation():
    try:
        conn = get_db_connection()

        name = request.args.get('name')
        email = request.args.get('email')
     
        # if not all([name, email]):
        #     return jsonify({"error": "Missing required fields"}), 400

        cursor = conn.execute("""INSERT INTO `employees` (`employee_id`,`employee_name`, `employee_email`) 
                                VALUES (1,'divya','d@gmail.com')""")
        conn.commit()

        return jsonify({"message": "Employee added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/data/orgnazation/delete/<int:user_id>', methods=['GET'])
def delete_orgnazation(user_id):
    try:
        conn = get_db_connection()

        cursor = conn.execute("SELECT * FROM employees WHERE employee_id = ?", (user_id,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({"error": "User not found"}), 404

        conn.execute("DELETE FROM employees WHERE employee_id = ?", (user_id,))
        conn.commit()

        return jsonify({"message": "Employee deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/orgnazation/update/<int:user_id>', methods=['GET'])
def update_orgnazation(user_id):
    try:
        conn = get_db_connection()

        cursor = conn.execute("SELECT * FROM employees WHERE employee_id = ?", (user_id,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({"error": "employee not found"}), 404

        # Update user data with new_data, if provided
        conn.execute("UPDATE employees SET employee_name = 'dup' WHERE employee_id = ?", (user_id,))
        conn.commit()

        return jsonify({"message": "Employee data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
