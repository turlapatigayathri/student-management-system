
from pathlib import Path
import sqlite3
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
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


def calculate_results(mark1, mark2, mark3):
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


def validate_student_form(form):
    roll_number = form.get("roll_number", "").strip()
    name = form.get("name", "").strip()
    course = form.get("course", "").strip()

    if not roll_number or not name or not course:
        return None, "Student number, student name and course are required."

    if not roll_number.isascii() or not roll_number.isdigit():
        return None, "Student number must contain digits only, for example 101."

    if int(roll_number) < 1:
        return None, "Student number must be greater than zero."

    if not any(char.isalpha() for char in name):
        return None, "Please enter a valid student name."

    if not all(
        char.isalpha() or char.isspace() or char in " .'-"
        for char in name
    ):
        return None, "Name can contain letters, spaces, periods, apostrophes and hyphens only."

    try:
        marks = [
            float(form.get("mark1", "")),
            float(form.get("mark2", "")),
            float(form.get("mark3", "")),
        ]
    except (TypeError, ValueError):
        return None, "Please enter valid marks for all three subjects."

    if any(not 0 <= mark <= 100 for mark in marks):
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



@app.route("/")
def dashboard():
    search_query = request.args.get("q", "").strip()

    with get_db_connection() as conn:
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
    total_marks_all = 0
    overall_average = 0

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
        total_marks_all += total

    if student_list:
        overall_average = round(
            total_marks_all / (len(student_list) * 3), 2
        )

    return render_template(
        "index.html",
        students=student_list,
        q=search_query,
        overall_average=overall_average,
    )



@app.route("/add", methods=["GET", "POST"])
def add_student():
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
            with get_db_connection() as conn:
                conn.execute("""
                    INSERT INTO students
                    (roll_number, name, course, mark1, mark2, mark3)
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


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with get_db_connection() as conn:
        record = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

    if record is None:
        abort(404)

    student = dict(record)

    if request.method == "POST":
        student, error = validate_student_form(request.form)

        if error:
            flash(error, "error")
            return render_template(
                "student_form.html",
                page_title="Edit Student",
                student=student or request.form,
            )

        try:
            with get_db_connection() as conn:
                conn.execute("""
                    UPDATE students
                    SET roll_number = ?, name = ?, course = ?,
                        mark1 = ?, mark2 = ?, mark3 = ?
                    WHERE id = ?
                """, (
                    student["roll_number"],
                    student["name"],
                    student["course"],
                    student["mark1"],
                    student["mark2"],
                    student["mark3"],
                    student_id,
                ))
        except sqlite3.IntegrityError:
            flash("That student number already exists.", "error")
            return render_template(
                "student_form.html",
                page_title="Edit Student",
                student=student,
            )

        flash("Student updated successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "student_form.html",
        page_title="Edit Student",
        student=student,
    )


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db_connection() as conn:
        conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,),
        )

    flash("Student deleted successfully.", "success")
    return redirect(url_for("dashboard"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
