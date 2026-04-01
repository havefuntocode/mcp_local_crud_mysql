import os
import mysql.connector
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MySQL CRUD Server")

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )


@mcp.tool()
def get_employees() -> str:
    """Alle Mitarbeiter aus der employees-Tabelle abrufen."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees ORDER BY id")
        rows = cursor.fetchall()
        if not rows:
            return "Keine Mitarbeiter gefunden."
        result = []
        for row in rows:
            result.append(
                f"ID: {row['id']} | Name: {row['first_name']} {row['last_name']} "
                f"| Abteilung: {row['department']} | Gehalt: {row['salary']}"
            )
        return "\n".join(result)
    finally:
        cursor.close()
        conn.close()


@mcp.tool()
def add_employee(first_name: str, last_name: str, department: str, salary: float) -> str:
    """Einen neuen Mitarbeiter hinzufügen."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (first_name, last_name, department, salary) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, department, salary),
        )
        conn.commit()
        return f"Mitarbeiter '{first_name} {last_name}' erfolgreich hinzugefügt (ID: {cursor.lastrowid})."
    finally:
        cursor.close()
        conn.close()


@mcp.tool()
def update_employee(employee_id: int, first_name: str, last_name: str, department: str, salary: float) -> str:
    """Einen bestehenden Mitarbeiter aktualisieren."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE employees
               SET first_name = %s, last_name = %s, department = %s, salary = %s
               WHERE id = %s""",
            (first_name, last_name, department, salary, employee_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return f"Kein Mitarbeiter mit ID {employee_id} gefunden."
        return f"Mitarbeiter mit ID {employee_id} erfolgreich aktualisiert."
    finally:
        cursor.close()
        conn.close()


@mcp.tool()
def delete_employee(employee_id: int) -> str:
    """Einen Mitarbeiter anhand der ID löschen."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return f"Kein Mitarbeiter mit ID {employee_id} gefunden."
        return f"Mitarbeiter mit ID {employee_id} erfolgreich gelöscht."
    finally:
        cursor.close()
        conn.close()


@mcp.tool()
def get_departments() -> str:
    """Alle vorhandenen Abteilungen zurückgeben."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT department FROM employees ORDER BY department")
        rows = cursor.fetchall()
        if not rows:
            return "Keine Abteilungen gefunden."
        return "\n".join(row[0] for row in rows)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    mcp.run(transport="stdio")