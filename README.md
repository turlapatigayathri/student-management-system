# Student Management System

## Project Overview

The Student Management System is a web-based application developed using Python, Flask, and SQLite. It helps users manage student records and academic marks through a simple and user-friendly interface.

The application allows users to add, view, search, edit, and delete student records. It also calculates the total marks, average percentage, and grade based on the student's marks in three subjects.

## Objectives

- Manage student information efficiently.
- Store student records in an SQLite database.
- Calculate total marks, average, and grades automatically.
- Validate student details and marks before saving.
- Provide search functionality to find student records easily.

## Technologies Used

- **Python:** Application logic and calculations.
- **Flask:** Web application framework.
- **SQLite:** Database for storing student records.
- **HTML:** Structure of the web pages.
- **CSS:** Styling and layout.
- **Visual Studio Code:** Code editor.
- **GitHub:** Project hosting and version control.

## Features

### 1. Add Student
Add a new student by entering the student number, name, course or stream, and marks in three subjects.

### 2. View Student Records
Display saved student information and academic results on the dashboard.

### 3. Search Students
Search student records using the available search functionality.

### 4. Edit Student Details
Update existing student information and marks.

### 5. Delete Student Records
Remove student records when they are no longer required.

### 6. Automatic Result Calculation
The application calculates total marks, average marks, and grades automatically.

### 7. Input Validation
Validate required fields, student numbers, and marks to help prevent invalid records.

### 8. Database Storage
Store student information in an SQLite database so records remain available after restarting the application.

## Grade Calculation

The application calculates the average from three subject marks and assigns a grade using the following rules:

| Average Marks | Grade |
|---|---|
| 90–100 | A+ |
| 80–89.99 | A |
| 70–79.99 | B |
| 60–69.99 | C |
| 50–59.99 | D |
| Below 50 | F |

**Formula:**

Total Marks = Subject 1 + Subject 2 + Subject 3

Average Marks = Total Marks / 3

## Project Structure

```text
student-management-system/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── students.db
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── student_form.html
│
├── static/
│   └── style.css
│
└── tests/
    └── test_result.py
```

## Installation and Setup

### Prerequisites

Install the following software:

- Python
- Visual Studio Code
- A web browser

SQLite is included with Python, so a separate database server is not required.

### Step 1: Clone the Repository

```bash
git clone https://github.com/turlapatigayathri/student-management-system.git
```

### Step 2: Open the Project Folder

```bash
cd student-management-system
```

### Step 3: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python app.py
```

### Step 6: Open the Application

Open your browser and visit:

http://127.0.0.1:5000

You can now add and manage student records.

## Database

The application uses SQLite to store student information, including:

- Student ID
- Student number
- Student name
- Course 
- Marks in three subjects
- Average

The database table is created automatically by the application when it starts, if it does not already exist.

## Learning Outcomes

Through this project, I practised:

- Python programming and functions.
- Developing web applications using Flask.
- Designing and querying an SQLite database.
- Performing CRUD operations (Create, Read, Update, and Delete).
- Validating user input.
- Using HTML templates and CSS.
- Organising a Python project into separate files.
- Hosting project source code on GitHub.

## Future Enhancements

- User authentication and role-based access.
- Export student results to CSV or PDF.
- Add charts to analyse student performance.
- Improve dashboard reporting.
- Add automated tests for application routes and database operations.

## Author

**Gayathri**

GitHub Repository:  
https://github.com/turlapatigayathri/student-management-system

## Disclaimer

This project was developed for educational and learning purposes. The application is intended to demonstrate basic student record management, web development, database operations, and academic result calculations.
