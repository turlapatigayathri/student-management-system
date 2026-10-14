from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, abort

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"

app = Flask(__name__)
# Used only for local development. Change this before any public deployment.
app.config["SECRET_KEY"] = "change-this-development-key"


def get_db_connection():
    """Open a database connection and return rows by column name."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the students table if it does not already exist."""
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_number TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                mark1 REAL NOT NULL CHECK(mark1 BETWEEN 0 AND 100),
                mark2 REAL NOT NULL CHECK(mark2 BETWEEN 0 AND 100),
                mark3 REAL NOT NULL CHECK(mark3 BETWEEN 0 AND 100),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def calculate_results(mark1, mark2, mark3):
    """Return total, average and grade from three marks."""
    total = mark1 + mark2 + mark3
    average = total / 3
    if average >= 90:
        grade = "A+"
    elif average >= 80:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 60:
        grade = "C"
    elif average >= 50:
        grade = "D"
    else:
        grade = "F"
    return total, round(average, 2), grade


def validate_student_form(form):
    """Validate submitted form fields; return cleaned values or an error."""
    roll_number = form.get("roll_number", "").strip()
    name = form.get("name", "").strip()
    course = form.get("course", "").strip()

    if not roll_number or not name or not course:
        return None, "Roll number, name and course are required."

    try:
        marks = [float(form.get(key, "")) for key in ("mark1", "mark2", "mark3")]
    except (TypeError, ValueError):
        return None, "Enter a valid number for each mark."

    if any(mark < 0 or mark > 100 for mark in marks):
        return None, "Each mark must be between 0 and 100."

    return {
        "roll_number": roll_number,
        "name": name,
        "course": course,
        "mark1": marks[0],
        "mark2": marks[1],
        "mark3": marks[2],
    }, None


def add_calculated_fields(student):
    """Add total, average and grade to a database row for display."""
    result = dict(student)
    result["total"], result["average"], result["grade"] = calculate_results(
        result["mark1"], result["mark2"], result["mark3"]
    )
    return result


@app.route("/")
def dashboard():
    search = request.args.get("q", "").strip()
    with get_db_connection() as connection:
        if search:
            rows = connection.execute(
                """SELECT * FROM students
                   WHERE roll_number LIKE ? OR name LIKE ? OR course LIKE ?
                   ORDER BY name COLLATE NOCASE""",
                (f"%{search}%", f"%{search}%", f"%{search}%"),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM students ORDER BY name COLLATE NOCASE"
            ).fetchall()

        total_students = connection.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]
        average_row = connection.execute(
            "SELECT AVG((mark1 + mark2 + mark3) / 3.0) FROM students"
        ).fetchone()[0]

    students = [add_calculated_fields(row) for row in rows]
    return render_template(
        "index.html",
        students=students,
        search=search,
        total_students=total_students,
        overall_average=round(average_row, 2) if average_row is not None else None,
    )


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student, error = validate_student_form(request.form)
        if error:
            flash(error, "error")
            return render_template("student_form.html", page_title="Add Student", student=request.form)

        try:
            with get_db_connection() as connection:
                connection.execute(
                    """INSERT INTO students
                       (roll_number, name, course, mark1, mark2, mark3)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        student["roll_number"], student["name"], student["course"],
                        student["mark1"], student["mark2"], student["mark3"],
                    ),
                )
        except sqlite3.IntegrityError:
            flash("That roll number already exists. Use a unique roll number.", "error")
            return render_template("student_form.html", page_title="Add Student", student=request.form)

        flash("Student added successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("student_form.html", page_title="Add Student", student={})


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with get_db_connection() as connection:
        row = connection.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        ).fetchone()
    if row is None:
        abort(404)

    if request.method == "POST":
        student, error = validate_student_form(request.form)
        if error:
            flash(error, "error")
            return render_template("student_form.html", page_title="Edit Student", student=request.form)

        try:
            with get_db_connection() as connection:
                connection.execute(
                    """UPDATE students
                       SET roll_number = ?, name = ?, course = ?, mark1 = ?, mark2 = ?, mark3 = ?
                       WHERE id = ?""",
                    (
                        student["roll_number"], student["name"], student["course"],
                        student["mark1"], student["mark2"], student["mark3"], student_id,
                    ),
                )
        except sqlite3.IntegrityError:
            flash("That roll number is already assigned to another student.", "error")
            return render_template("student_form.html", page_title="Edit Student", student=request.form)

        flash("Student updated successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("student_form.html", page_title="Edit Student", student=dict(row))


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db_connection() as connection:
        cursor = connection.execute("DELETE FROM students WHERE id = ?", (student_id,))
    if cursor.rowcount == 0:
        abort(404)
    flash("Student deleted successfully.", "success")
    return redirect(url_for("dashboard"))


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


init_db()

if __name__ == "__main__":
    # Local development only; do not expose Flask's debug server to the internet.
    app.run(debug=True)
