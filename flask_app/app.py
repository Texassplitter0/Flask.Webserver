import os

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="flask_app/Webserver-main/images", template_folder=os.path.abspath('flask_app/Webserver-main/templates'))
app.secret_key = 'your_secret_key'


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'db'),  # Richtig für Docker
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'rootpassword'),
        database=os.getenv('MYSQL_DATABASE', 'flask_app')
    )


def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('user', 'admin', 'editor') DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        session['role'] = user['role']
        return redirect(url_for('welcome'))
    else:
        return "Login fehlgeschlagen!", 401

@app.route('/welcome')
def welcome():
    if 'user' in session:
        return render_template('welcome.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user' in session and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, username, role FROM users')
        users = cursor.fetchall()
        conn.close()

        if request.method == 'POST':
            new_username = request.form['username']
            new_password = generate_password_hash(request.form['password'])
            role = request.form['role']
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', 
                           (new_username, new_password, role))
            conn.commit()
            conn.close()
            
            return redirect(url_for('admin'))
        
        return render_template('admin.html', users=users)
    return redirect(url_for('index'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'user' in session and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('admin'))

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user' in session and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        
        if request.method == 'POST':
            new_username = request.form['username']
            new_password = generate_password_hash(request.form['password'])
            role = request.form['role']
            
            cursor.execute('UPDATE users SET username = %s, password = %s, role = %s WHERE id = %s', 
                           (new_username, new_password, role, user_id))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))
        
        conn.close()
        return render_template('edit_user.html', user=user)
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
