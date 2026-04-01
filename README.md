# CRUD MySQL MCP Server Erfahrungsbericht
Ziel war es hier einen MCP-Server als Brücke zwischen dem Claude-Client und einer MySQL-Datenbank zu entwickeln, um CRUD Answeisungen auszuführen. 
Hierbei handelt es sich um einen kleinen Erfahrungsbericht. Hier ging es mir also in erster Linie darum Erkenntnisse zu gewinnen und zu lernen.
Der Quellkode für den MCP-Server wurde von Claude erstellt. 


## Voraussetzungen

- Python 3.11+
- MySQL
- Claude Desktop (Windows)
- Bibliotheken: mcp, mysql-connector-python

## Bibliotheken in Python bereit stellen

```bash
pip install fastmcp mysql-connector-python
```

## Datenbankstruktur
Die Datenbank die für den Erhfahrungsbericht verwendet wurde, habe ich mit folgenden drei Anweisungen eingerichtet.
```sql

-- Datenbank erstellen und auswählen
CREATE DATABASE IF NOT EXISTS mitarbeiter_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE employees_db;

-- Tabelle erstellen
CREATE TABLE IF NOT EXISTS employees (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100) NOT NULL,
    department  VARCHAR(100) NOT NULL,
    salary      DECIMAL(10, 2) NOT NULL
);

-- Beispieldaten
INSERT INTO employees (first_name, last_name, department, salary) VALUES
    ('Anna',      'Müller',   'IT',         4500.00),
    ('Thomas',    'Schmidt',  'HR',         3800.00),
    ('Sabine',    'Weber',    'Finanzen',   5200.00),
    ('Siegfried', 'Meier',    'IT',         4200.00);

```

## Claude Desktop Konfiguration

Die Datei `claude_desktop_config.json` `(C:\Users\user\AppData\Roaming\Claude\claude_desktop_config.json)` wurde um folgenden Eintrag ergänzt:

```json

"mysql-crud": {
      "command": "c:/Users/<user>/AppData/Local/Programs/Python/Python311/python.exe",
      "args": ["c:/<your path>/mcp_crud_local_mysql/server.py"],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "root",
        "MYSQL_PASSWORD": "dein_passwort",
        "MYSQL_DATABASE": "mitarbeiter_db"
      }
    }

```

## Verfuegbare Tools

| Tool | Beschreibung |
|------|-------------|
| `get_employees` | Alle Mitarbeiter abrufen, optional nach Abteilung filtern |
| `get_departments` | Alle Abteilungen abrufen |
| `add_employee` | Neuen Mitarbeiter hinzufuegen |
| `update_employee` | Mitarbeiter aktualisieren (nur geaenderte Felder) |
| `delete_employee` | Mitarbeiter loeschen |

