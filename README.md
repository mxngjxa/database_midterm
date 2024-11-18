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

An example of how this code works is as follows:

```
Library Database Management System
1. Setup database (setup)
2. View unreturned books (unreturned)
3. Fuzzy search (search)
4. View borrowing frequency (frequency)
5. View recent transactions (recent)
6. View statistics by major (stats)
7. Exit (exit)
0. Reset database (reset)

What would you like to do? reset
Resetting the database...
Dropping table: books
Dropping table: fine
Dropping table: loan
Dropping table: students
All tables dropped successfully.
Database reset complete.

Library Database Management System
1. Setup database (setup)
2. View unreturned books (unreturned)
3. Fuzzy search (search)
4. View borrowing frequency (frequency)
5. View recent transactions (recent)
6. View statistics by major (stats)
7. Exit (exit)
0. Reset database (reset)

What would you like to do? setup 
Setting up the database...
Database setup complete.

Library Database Management System
1. Setup database (setup)
2. View unreturned books (unreturned)
3. Fuzzy search (search)
4. View borrowing frequency (frequency)
5. View recent transactions (recent)
6. View statistics by major (stats)
7. Exit (exit)
0. Reset database (reset)

What would you like to do? unreturned
Fetching unreturned books...
('The Hobbit', 'William Turner', datetime.date(2024, 3, 10))
('Chemistry Fundamentals', 'Emily Taylor', datetime.date(2024, 2, 25))
('Lord of the Rings', 'Rachel Cohen', datetime.date(2024, 3, 25))
('Economics 101', 'Brian Johnson', datetime.date(2024, 5, 1))
('Philosophy Basics', 'Christopher Lee', datetime.date(2024, 4, 10))
('Environmental Science', 'Ryan Wilson', datetime.date(2024, 5, 10))
('Music Theory', 'Kevin Chang', datetime.date(2024, 4, 20))
('Creative Writing', 'Matthew Brown', datetime.date(2024, 5, 20))

Library Database Management System
1. Setup database (setup)
2. View unreturned books (unreturned)
3. Fuzzy search (search)
4. View borrowing frequency (frequency)
5. View recent transactions (recent)
6. View statistics by major (stats)
7. Exit (exit)
0. Reset database (reset)

What would you like to do? search
Enter the table name: fine
Enter the column name: reason 
Enter the keyword to search: Overdue Return
('F001', 'S008', Decimal('5.50'), 'Overdue Return', datetime.date(2024, 3, 10))
('F002', 'S011', Decimal('7.00'), 'Overdue Return', datetime.date(2024, 3, 25))
('F003', 'S014', Decimal('4.50'), 'Overdue Return', datetime.date(2024, 4, 10))
('F004', 'S017', Decimal('6.00'), 'Overdue Return', datetime.date(2024, 4, 25))
('F005', 'S019', Decimal('8.50'), 'Overdue Return', datetime.date(2024, 5, 5))
('F006', 'S021', Decimal('5.00'), 'Overdue Return', datetime.date(2024, 5, 15))
('F007', 'S023', Decimal('7.50'), 'Overdue Return', datetime.date(2024, 5, 25))

Library Database Management System
1. Setup database (setup)
2. View unreturned books (unreturned)
3. Fuzzy search (search)
4. View borrowing frequency (frequency)
5. View recent transactions (recent)
6. View statistics by major (stats)
7. Exit (exit)
0. Reset database (reset)

What would you like to do? frequency
Order by descending frequency? (yes/no): yes
('Fiction', 'Biology', 1)
('Fiction', 'Mathematics', 1)
('Technology', 'Biology', 1)
('Technology', 'Mathematics', 1)
('Arts', 'Theater Arts', 2)
('Fiction', 'Computer Science', 2)
('Business', 'Marketing', 2)
('Technology', 'Journalism', 2)
('Arts', 'Law', 2)
('Science', 'Environmental Science', 2)
('Business', 'Medicine', 2)
('Mathematics', 'Anthropology', 2)
('Philosophy', 'Architecture', 2)
('Economics', 'Film Studies', 2)
('History', 'Sociology', 2)
('Arts', 'Art History', 2)
('Science', 'Political Science', 2)
('Fantasy', 'Philosophy', 2)
('Mathematics', 'Economics', 2)
('Fiction', 'Music', 2)
('Science', 'Psychology', 2)
('Fiction', 'Business', 2)
('Technology', 'Chemistry', 2)
('Fantasy', 'Engineering', 2)
('Technology', 'English', 2)
('Fiction', 'History', 2)
('Technology', 'Physics', 2)

Library Database Management System
1. Setup database (setup)
2. View unreturned books (unreturned)
3. Fuzzy search (search)
4. View borrowing frequency (frequency)
5. View recent transactions (recent)
6. View statistics by major (stats)
7. Exit (exit)
0. Reset database (reset)

What would you like to do? recent
Enter the number of recent transactions to display: 5
('Creative Writing', 'Paul Taylor', datetime.date(2024, 9, 25))
('Artificial Intelligence', 'Alice Davis', datetime.date(2024, 9, 20))
('Environmental Science', 'David Moore', datetime.date(2024, 9, 15))
('Statistical Methods', 'Emily Robinson', datetime.date(2024, 9, 10))
('Economics 101', 'Jack Wilson', datetime.date(2024, 9, 5))

Library Database Management System
1. Setup database (setup)
2. View unreturned books (unreturned)
3. Fuzzy search (search)
4. View borrowing frequency (frequency)
5. View recent transactions (recent)
6. View statistics by major (stats)
7. Exit (exit)
0. Reset database (reset)

What would you like to do? stats
Order by descending average borrows? (yes/no): no
('History', 2, 2, Decimal('1.00'))
('Theater Arts', 2, 2, Decimal('1.00'))
('Sociology', 2, 2, Decimal('1.00'))
('Psychology', 2, 2, Decimal('1.00'))
('Political Science', 2, 2, Decimal('1.00'))
('Physics', 2, 2, Decimal('1.00'))
('Philosophy', 2, 2, Decimal('1.00'))
('Music', 2, 2, Decimal('1.00'))
('Medicine', 2, 2, Decimal('1.00'))
('Mathematics', 2, 2, Decimal('1.00'))
('Marketing', 2, 2, Decimal('1.00'))
('Law', 2, 2, Decimal('1.00'))
('Journalism', 2, 2, Decimal('1.00'))
('Anthropology', 2, 2, Decimal('1.00'))
('Film Studies', 2, 2, Decimal('1.00'))
('Environmental Science', 2, 2, Decimal('1.00'))
('English', 2, 2, Decimal('1.00'))
('Engineering', 2, 2, Decimal('1.00'))
('Economics', 2, 2, Decimal('1.00'))
('Computer Science', 2, 2, Decimal('1.00'))
('Chemistry', 2, 2, Decimal('1.00'))
('Business', 2, 2, Decimal('1.00'))
('Biology', 2, 2, Decimal('1.00'))
('Art History', 2, 2, Decimal('1.00'))
('Architecture', 2, 2, Decimal('1.00'))

Library Database Management System
1. Setup database (setup)
2. View unreturned books (unreturned)
3. Fuzzy search (search)
4. View borrowing frequency (frequency)
5. View recent transactions (recent)
6. View statistics by major (stats)
7. Exit (exit)
0. Reset database (reset)

What would you like to do? exit
Exiting the system. Goodbye!
```
