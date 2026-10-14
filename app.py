
from pathlib import Path
from contextlib import contextmanager
import os
import secrets
import sqlite3
import math

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
)


# --------------------------------------------------
# 1. APPLICATION CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"

app = Flask(__name__)

# Use an environment variable for a stable secret key.
# A random fallback is provided for local development.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)


# --------------------------------------------------
# 2. DATABASE CONNECTION
# --------------------------------------------------

def get_db_connection():
    """Create and return a SQLite database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_connection():
    """Commit successful transactions and always close connections."""
    conn = get_db_connection()

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# --------------------------------------------------
# 3. CREATE DATABASE TABLE
# --------------------------------------------------

def init_db():
    """Create the students table if it does not exist."""
    with db_connection() as conn:
        conn.execute("""
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


# --------------------------------------------------
# 4. CALCULATE TOTAL, AVERAGE AND GRADE
# --------------------------------------------------

def calculate_results(mark1, mark2, mark3):
    """Calculate results for three subject marks."""
    total = mark1 + mark2 + mark3
    average = round(total / 3, 2)

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

    return total, average, grade


# --------------------------------------------------
# 5. VALIDATE STUDENT DETAILS
# --------------------------------------------------

def validate_student_form(form):
    """Validate student details before inserting or updating."""
    roll_number = form.get("roll_number", "").strip()
    name = form.get("name", "").strip()
    course = form.get("course", "").strip()

    if not roll_number or not name or not course:
        return None, (
            "Student number, student name and course are required."
        )

    if not roll_number.isascii() or not roll_number.isdigit():
        return None, (
            "Student number must contain digits only, for example 101."
        )

    if int(roll_number) < 1:
        return None, "Student number must be greater than zero."

    if len(name) > 100:
        return None, "Student name must be 100 characters or fewer."

    if not any(char.isalpha() for char in name):
        return None, "Please enter a valid student name."

    if not all(
        char.isalpha() or char.isspace() or char in " .'-"
        for char in name
    ):
        return None, (
            "Name can contain letters, spaces, periods, "
            "apostrophes and hyphens only."
        )

    if len(course) > 100:
        return None, "Course must be 100 characters or fewer."

    try:
        marks = [
            float(form.get("mark1", "")),
            float(form.get("mark2", "")),
            float(form.get("mark3", "")),
        ]
    except (TypeError, ValueError):
        return None, "Please enter valid marks for all three subjects."

    if any(not math.isfinite(mark) for mark in marks):
        return None, "Marks must be valid finite numbers."

    if any(mark < 0 or mark > 100 for mark in marks):
        return None, "Each subject mark must be between 0 and 100."

    student = {
        "roll_number": roll_number,
        "name": name,
        "course": course,
        "mark1": marks[0],
        "mark2": marks[1],
        "mark3": marks[2],
    }

    return student, None


# --------------------------------------------------
# 6. DASHBOARD AND SEARCH
# --------------------------------------------------

@app.route("/")
def dashboard():
    """Display student records and overall dashboard statistics."""
    search_query = request.args.get("q", "").strip()

    with db_connection() as conn:
        # Calculate statistics across all student records.
        stats = conn.execute("""
            SELECT
                COUNT(*) AS total_students,
                AVG((mark1 + mark2 + mark3) / 3.0)
                    AS overall_average
            FROM students
        """).fetchone()

        # Retrieve all students or matching search results.
        if search_query:
            students = conn.execute("""
                SELECT * FROM students
                WHERE roll_number LIKE ?
                   OR name LIKE ?
                   OR course LIKE ?
                ORDER BY id DESC
            """, (
                f"%{search_query}%",
                f"%{search_query}%",
                f"%{search_query}%",
            )).fetchall()
        else:
            students = conn.execute("""
                SELECT * FROM students
                ORDER BY id DESC
            """).fetchall()

    student_list = []

    for student in students:
        total, average, grade = calculate_results(
            student["mark1"],
            student["mark2"],
            student["mark3"],
        )

        item = dict(student)
        item["total"] = total
        item["average"] = average
        item["grade"] = grade

        student_list.append(item)

    overall_average = stats["overall_average"]

    if overall_average is not None:
        overall_average = round(overall_average, 2)

    return render_template(
        "index.html",
        students=student_list,
        total_students=stats["total_students"],
        overall_average=overall_average,
        search=search_query,
        q=search_query,
    )


# --------------------------------------------------
# 7. ADD STUDENT
# --------------------------------------------------

@app.route("/add", methods=["GET", "POST"])
def add_student():
    """Display the form and add a new student."""
    student = {
        "roll_number": "",
        "name": "",
        "course": "",
        "mark1": "",
        "mark2": "",
        "mark3": "",
    }

    if request.method == "POST":
        student, error = validate_student_form(request.form)

        if error:
            flash(error, "error")
            return render_template(
                "student_form.html",
                page_title="Add Student",
                student=student or request.form,
            )

        try:
            with db_connection() as conn:
                conn.execute("""
                    INSERT INTO students (
                        roll_number, name, course,
                        mark1, mark2, mark3
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    student["roll_number"],
                    student["name"],
                    student["course"],
                    student["mark1"],
                    student["mark2"],
                    student["mark3"],
                ))

        except sqlite3.IntegrityError:
            flash("That student number already exists.", "error")
            return render_template(
                "student_form.html",
                page_title="Add Student",
                student=student,
            )

        flash("Student added successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "student_form.html",
        page_title="Add Student",
        student=student,
    )


# --------------------------------------------------
# 8. EDIT STUDENT
# --------------------------------------------------

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    """Display the form and update an existing student."""

    # Correct indentation: this block belongs inside the function.
    with db_connection() as conn:
        record = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

    if record is None:
        abort(404)

    student = dict(record)

    if request.method == "POST":
        updated_student, error = validate_student_form(request.form)

        if error:
            flash(error, "error")
            return render_template(
                "student_form.html",
                page_title="Edit Student",
                student=updated_student or request.form,
            )

        try:
            with db_connection() as conn:
                conn.execute("""
                    UPDATE students
                    SET roll_number = ?,
                        name = ?,
                        course = ?,
                        mark1 = ?,
                        mark2 = ?,
                        mark3 = ?
                    WHERE id = ?
                """, (
                    updated_student["roll_number"],
                    updated_student["name"],
                    updated_student["course"],
                    updated_student["mark1"],
                    updated_student["mark2"],
                    updated_student["mark3"],
                    student_id,
                ))

        except sqlite3.IntegrityError:
            flash("That student number already exists.", "error")
            return render_template(
                "student_form.html",
                page_title="Edit Student",
                student=updated_student,
            )

        flash("Student updated successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "student_form.html",
        page_title="Edit Student",
        student=student,
    )


# --------------------------------------------------
# 9. DELETE STUDENT
# --------------------------------------------------

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    """Delete a student record."""
    with db_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,),
        )

        deleted = cursor.rowcount

    if deleted == 0:
        abort(404)

    flash("Student deleted successfully.", "success")
    return redirect(url_for("dashboard"))


# --------------------------------------------------
# 10. START APPLICATION
# --------------------------------------------------

init_db()


if __name__ == "__main__":
    # Debug mode is disabled by default.
    # Enable it only for local development when needed.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
