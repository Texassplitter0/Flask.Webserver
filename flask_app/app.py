import os
from flask import Flask, render_template, request, redirect, url_for, session, abort
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="/app/flask_app/Webserver-main/images", template_folder=os.path.abspath('/app/flask_app/Webserver-main'))
app.secret_key = 'your_secret_key'


def get_db_connection(use_root=False):
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'db'),
        user='root' if use_root else os.getenv('MYSQL_USER', 'flask_user'),
        password=os.getenv('MYSQL_ROOT_PASSWORD') if use_root else os.getenv('MYSQL_PASSWORD', 'flask_password'),
        database=os.getenv('MYSQL_DATABASE', 'flask_app')
    )


import time

import time

def create_database():
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection(use_root=True)
            cursor = conn.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS flask_app;")
            cursor.execute("USE flask_app;")

            # Tabellen erstellen
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('user', 'admin', 'editor') DEFAULT 'user'
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS registration_requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)

            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Datenbank erfolgreich erstellt!")
            break  # Schleife verlassen, wenn erfolgreich

        except mysql.connector.Error as err:
            print(f"❌ Fehler bei der Datenbankerstellung: {err}")
            retries -= 1
            print(f"🔄 Neuer Versuch in 5 Sekunden... ({5 - retries}/5)")
            time.sleep(5)

    if retries == 0:
        print("❌ Konnte die Datenbank nach mehreren Versuchen nicht erstellen!")


def initialize_database():
    """Führt die ini.sql aus, um die Datenbank zu initialisieren"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        with open("init.sql", "r") as f:
            sql_commands = f.read()

        for command in sql_commands.split(";"):
            if command.strip():
                cursor.execute(command)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Datenbank erfolgreich aus ini.sql initialisiert!")

    except Exception as e:
        print(f"❌ Fehler beim Laden der ini.sql: {e}")


from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('flask_app/Webserver-main/static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html')


# <------------------------------------------Routes-für-HTML-Dateien-setzen------------------------------------------------------------>
@app.route('/adminpanel')
def adminpanel():
    if session.get('logged_in') and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, username FROM registration_requests")
        registration_requests = cursor.fetchall()

        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('admin.html', users=users, registration_requests=registration_requests)

    return redirect(url_for('index'))


@app.route('/datenschutz')
def datenschutz():
    if session.get('logged_in'):
        return render_template('datenschutz.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/gamedivers')
def gamedivers():
    if session.get('logged_in'):
        return render_template('gamedivers.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/helldivers')
def helldivers():
    if session.get('logged_in'):
        return render_template('helldivers.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/impressum')
def impressum():
    if session.get('logged_in'):
        return render_template('impressum.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/memecoin')
def memecoin():
    if session.get('logged_in'):
        return render_template('memecoin.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/minecraft')
def minecraft():
    if session.get('logged_in'):
        return render_template('minecraft.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/palworld')
def palworld():
    if session.get('logged_in'):
        return render_template('palworld.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    if session.get('logged_in'):
        username = session['user']

        # Benutzerdaten aus der Datenbank abrufen
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, username, role FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return render_template('profile.html', user=user)
    
    return redirect(url_for('index'))


@app.route('/registration')
def registration():
    if session.get('logged_in'):
        return render_template('registration.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/satisfactory')
def satisfactory():
    if session.get('logged_in'):
        return render_template('satisfactory.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/spaceengineers')
def spaceengineers():
    if session.get('logged_in'):
        return render_template('spaceengineers.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/spaceengineerstwo')
def spaceengineerstwo():
    if session.get('logged_in'):
        return render_template('spaceengineerstwo.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/underdevelopement')
def underdevelopement():
    if session.get('logged_in'):
        return render_template('under-developement.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/welcomeuser')
def welcomeuser():
    if session.get('logged_in'):
        return render_template('welcome-user.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


@app.route('/welcome')
def welcome():
    if session.get('logged_in'):
        return render_template('welcome.html', user=session['user'], role=session.get('role', 'user'))
    return redirect(url_for('index'))


# <------------------------------------------Restliche-Routes------------------------------------------------------------>
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Standardmäßig keine Fehlermeldung

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user['password'] and check_password_hash(user['password'], password):
            session['logged_in'] = True 
            session['user'] = username
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('welcomeuser'))
        else:
            error = "⚠ Benutzername oder Passwort ist falsch!"

    return render_template('index.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Prüfen, ob Benutzername bereits existiert
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = "⚠ Benutzername bereits vergeben!"
        else:
            # Registrierung als ausstehende Anfrage speichern
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO registration_requests (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            success = "✅ Registrierung erfolgreich! Ein Admin muss die Anfrage bestätigen."

        cursor.close()
        conn.close()

    return render_template('registration.html', error=error, success=success)


@app.route('/admin_approve/<int:request_id>')
def admin_approve(request_id):
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Benutzer aus der Registrierungstabelle holen
        cursor.execute("SELECT * FROM registration_requests WHERE id = %s", (request_id,))
        request_data = cursor.fetchone()

        if request_data:
            # In die Haupt-User-Tabelle einfügen
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'user')",
                           (request_data['username'], request_data['password']))
            # Registrierungsanfrage löschen
            cursor.execute("DELETE FROM registration_requests WHERE id = %s", (request_id,))
            conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('adminpanel'))


@app.route('/admin_reject/<int:request_id>')
def admin_reject(request_id):
    if 'role' in session and session['role'] == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM registration_requests WHERE id = %s", (request_id,))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('adminpanel'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('logged_in') and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':  
            new_username = request.form['username']
            new_password = request.form['password']
            role = request.form['role']

            hashed_password = generate_password_hash(new_password)

            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', 
                           (new_username, hashed_password, role))
            conn.commit()

        cursor.execute('SELECT id, username, role FROM users')
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('admin.html', users=users)

    return redirect(url_for('index'))


@app.route('/delete_account', methods=['POST'])
def delete_account():
    if session.get('logged_in'):
        user_id = session.get('user_id')

        # Benutzer aus der Datenbank löschen
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

        # Benutzer ausloggen
        session.clear()
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if session.get('logged_in') and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('admin'))


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if session.get('logged_in') and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()

        if request.method == 'POST':
            new_username = request.form['username']
            new_password = request.form['password']
            role = request.form['role']

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
    initialize_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
