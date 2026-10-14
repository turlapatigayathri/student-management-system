# Advanced Student Management System

A beginner-friendly student-record web application built with Python, Flask, SQLite, HTML and CSS.

# Project Overview

The Student Management System is a web-based application developed using Python, Flask, SQLite, HTML, and CSS. It helps users manage student records through a simple and user-friendly interface.

The application allows users to add, view, search, update, and delete student information. It demonstrates the practical use of Python programming, web development, database management, and CRUD operations.

# Objectives

Develop a simple web application for managing student records.

Implement CRUD operations using Python and SQLite.

Use Flask to connect the frontend with the backend.

Store student information in a database.

Practise input validation, problem-solving, and application testing.

## Technologies Used

- Python: Application logic and backend programming.

- Flask: Web application framework.

- SQLite: Database for storing student records.

- HTML: Structure of web pages.

- CSS: Styling and layout of the website.

- Visual Studio Code: Code editor and development environment.


## Features
- Add, view, search, edit and delete student records
- SQLite database keeps records after the app restarts
- Validates required fields and marks (0–100)
- Prevents duplicate roll numbers
- Calculates totals, averages and grades
- Dashboard displays total students and overall average
- Responsive layout for desktop and mobile browsers

## Project Folder Structure

StudentManagement/
│
├── app.py
├── students.db
├── requirements.txt
├── README.md
├
│
├── templates/
│   ├── index.html
│   └── other HTML files
│
└── static/
    └── style.css

## Requirements
- Python 3.9 or newer
- Internet connection for the initial Flask installation

## Run on Windows
1. Open this folder in VS Code.
2. Open Terminal → New Terminal.
3. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
4. Activate it:
   ```powershell
   .venv\Scripts\activate
   ```
5. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   python app.py
   ```
7. Open http://127.0.0.1:5000 in your browser.
8. Press Ctrl+C in the terminal to stop the server.

## Database
On first run, the application creates `students.db` automatically in the project folder. It is excluded from Git by `.gitignore`, so real or test records are not uploaded. The database can be recreated by running the app again.

## Grade scale
- 90 and above: A+
- 80–89.99: A
- 70–79.99: B
- 60–69.99: C
- 50–59.99: D
- Below 50: F

# Testing

- The following tests can be performed:

- Add a student with valid details.

- Verify that the student appears in the list.

- Search for an existing student.

- Update a student's marks or other details.

- Delete a test record and verify its removal.

- Try submitting invalid or incomplete information.

- Restart the application and verify that saved records remain available.

# Learning Outcomes

- Through this project, I am developing practical knowledge of:

- Python programming and functions.

- Web application development using Flask.

- HTML forms and CSS styling.

- Database operations using SQLite.

- CRUD operations and data persistence.

- Input validation and error handling.

- Debugging and testing a software application.

- Organizing code into files and folders.

# Future Enhancements

- Possible future improvements include:

- User authentication and secure login.

- Student performance analytics and visual charts.

- Exporting student records to CSV.

- Improved form validation and error messages.

- Pagination for large student lists.

- Unit tests for database and application functions.

- Responsive design for mobile devices.

- Deployment to a hosting platform.

# Conclusion

The Student Management System is a practical beginner-level web development project that demonstrates how Python, Flask, and SQLite can work together to manage structured data.

It provides hands-on experience with backend programming, database operations, user interfaces, and software testing. The project can be extended with additional features as programming and computer science knowledge improves.

# Author: T.Gayathri

Project Name: Student Management System
Programming Language: Python
Framework: Flask
Database: SQLite
Development Environment: Visual Studio Code

This project is intended for educational purposes and continued improvement.
