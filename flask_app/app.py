import os
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="/flask_app/Webserver-main/images", template_folder=os.path.abspath('/flask_app/Webserver-main'))
app.secret_key = 'your_secret_key'


def get_db_connection():
    """Stellt eine Verbindung zur MySQL-Datenbank her"""
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'db'),  # Richtig für Docker
        user=os.getenv('MYSQL_USER', 'flas_user'),
        password=os.getenv('MYSQL_PASSWORD', 'rootpassword'),
        database=os.getenv('MYSQL_DATABASE', 'flask_app')
    )


def create_database():
    """Erstellt die Datenbank-Tabelle 'users', falls sie nicht existiert, und fügt den Admin-User hinzu"""
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

    # Sicherstellen, dass der Admin-User existiert
    admin_password_hash = generate_password_hash("Lappen01")
    cursor.execute("""
        INSERT INTO users (username, password, role) 
        VALUES ('Admin', %s, 'admin')
        ON DUPLICATE KEY UPDATE username=username;
    """, (admin_password_hash,))

    conn.commit()
    cursor.close()
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
    cursor.close()
    conn.close()

    if user and user['password'] and check_password_hash(user['password'], password):
        session['user'] = username
        session['role'] = user['role']
        return redirect(url_for('welcome-user'))
    else:
        return "Login fehlgeschlagen!", 401


@app.route('/welcome')
def welcome():
    if 'user' in session:
        return render_template('welcome-user.html', user=session['user'], role=session.get('role', 'user'))
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
        cursor.close()
        conn.close()

        if request.method == 'POST':
            new_username = request.form['username']
            new_password = request.form['password']
            role = request.form['role']

            # 🔥 Stelle sicher, dass das Passwort gehasht wird
            hashed_password = generate_password_hash(new_password)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', 
                           (new_username, hashed_password, role))
            conn.commit()
            cursor.close()
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
        cursor.close()
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
            new_password = request.form['password']
            role = request.form['role']

            # Falls der Admin kein Passwort ändert, bleibt das alte bestehen
            if new_password:
                hashed_password = generate_password_hash(new_password)
                cursor.execute('UPDATE users SET username = %s, password = %s, role = %s WHERE id = %s', 
                               (new_username, hashed_password, role, user_id))
            else:
                cursor.execute('UPDATE users SET username = %s, role = %s WHERE id = %s', 
                               (new_username, role, user_id))

            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('admin'))

        cursor.close()
        conn.close()
        return render_template('edit_user.html', user=user)
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
