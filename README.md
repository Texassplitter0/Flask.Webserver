# Flask Webserver mit MySQL

Dieses Projekt ist ein einfacher Webserver mit Flask, der eine Benutzerverwaltung beinhaltet. Es unterstützt Login, Admin-Funktionalität, Rollenverwaltung und wird über Docker bereitgestellt.

## Installation & Setup (Lokal)

### 1. Abhängigkeiten installieren
Falls du die Anwendung **ohne Docker** betreiben möchtest, installiere die benötigten Abhängigkeiten:
```bash
pip install -r requirements.txt
```

### 2. Datenbank einrichten
Falls du MySQL **manuell** aufgesetzt hast, führe das `init.sql`-Skript aus, um die Tabellen und Benutzer zu erstellen:
```bash
mysql -u root -p -h localhost flask_app < init.sql
```
Falls du Docker verwendest, kannst du die MySQL-Datenbank mit Docker starten (siehe unten).

### 3. Anwendung starten
```bash
python app.py
```
Die Anwendung läuft standardmäßig auf **http://127.0.0.1:5000/**.

---

## Docker verwenden
Um die gesamte Anwendung in Docker auszuführen:
```bash
docker-compose up --build
```
**Wichtige Ports:**
- Flask läuft auf **Port 10100** (`http://<SERVER-IP>:10100`)
- MySQL ist auf **Port 3306** erreichbar (nur intern für Flask)

---

## Standard Admin-Login
- **Benutzername:** `Admin`
- **Passwort:** `Lappen01` *(Passwort ist gehasht gespeichert, wird beim ersten Start automatisch generiert)*

Falls das Passwort nicht funktioniert, kann ein neuer Hash in der MySQL-Datenbank generiert werden:
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("Lappen01"))
```
Füge dann den neuen Hash manuell in MySQL ein:
```sql
UPDATE users SET password = 'NEUER_HASH' WHERE username = 'Admin';
```

---

## Verzeichnisstruktur
```plaintext
/flask_app
│── /Webserver-main        # Enthält alle relevanten HTML-Templates
│── /static                # Statische Dateien (CSS, JS, Bilder)
│── app.py                 # Haupt-Flask-Anwendung
│── requirements.txt        # Python-Abhängigkeiten
│── Dockerfile              # Dockerfile für Flask-App
│── docker-compose.yml      # Docker-Setup für Flask & MySQL
│── init.sql                # Datenbank-Initialisierung
│── README.md               # Projektbeschreibung
```

---

## Wichtige Endpunkte
| Route            | Methode | Beschreibung |
|-----------------|---------|-------------|
| `/`             | GET     | Startseite |
| `/login`        | POST    | Login mit Benutzername & Passwort |
| `/logout`       | GET     | Benutzer ausloggen |
| `/welcome`      | GET     | Begrüßungsseite nach Login |
| `/admin`        | GET/POST| Admin-Dashboard zur Benutzerverwaltung |
| `/delete_user/<user_id>` | GET | Löscht einen Benutzer (Admin-Only) |
| `/edit_user/<user_id>` | GET/POST | Bearbeitet einen Benutzer (Admin-Only) |

---

## Fehlerbehebung
Falls die Anwendung nicht funktioniert:
1. **Überprüfe die Docker-Logs**
   ```bash
   docker logs webserver2-web-1
   docker logs webserver2-db-1
   ```
2. **Datenbankverbindung testen**
   ```bash
   docker exec -it webserver2-db-1 mysql -u flask_user -pflask_password -h db flask_app
   ```
3. **Falls MySQL-Probleme auftreten:**
   ```bash
   docker-compose down
   docker volume rm webserver2_mysql_data
   docker-compose up --build
   ```

---

🚀 **Jetzt sollte der Webserver mit MySQL voll funktionsfähig sein!** 🎉

