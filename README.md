# Library Database Management System

## Overview
This project implements a Python-based Library Database Management System using MySQL. It provides functionalities to manage and interact with a library database, including importing data, searching, and generating statistical insights.

## Key Features
- **Database Setup**: Create and populate tables with sample data from CSV files.
- **Fuzzy Search**: Perform keyword-based searches in specific table columns.
- **Borrowing Insights**: Analyze borrowing statistics grouped by book category and student major.
- **Transaction History**: View the most recent borrowing transactions.
- **Unreturned Books**: Retrieve a list of books not returned by students.
- **Statistics by Major**: Calculate borrowing statistics (e.g., average borrows per student) grouped by major.
- **Reset Database**: Reset the database schema and data to its initial state.

## Project Structure
- **`connection.py`**: Handles MySQL connection logic.
- **`insert.py`**: Contains the function to import data into tables.
- **`tables.py`**: Includes logic to create database tables.
- **`reset.py`**: Defines logic to reset the database schema.
- **`LibraryDatabase` Class**: Implements various methods to interact with the database.

The ER diagram for the project is as follows:

![midterm_er drawio](https://github.com/user-attachments/assets/44b9ca1f-6f4f-4258-aaf3-f0a72df9508c)
