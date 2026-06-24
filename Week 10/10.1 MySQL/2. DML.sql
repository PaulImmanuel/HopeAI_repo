CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID, auto-increment
    first_name VARCHAR(50) NOT NULL,            -- Cannot be NULL
    last_name VARCHAR(50),                      -- Optional
    email VARCHAR(100) UNIQUE,                  -- Must be unique
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- Default to today's date
);
select * from students;
-- 1) Insert 
-- Insert a single row into the 'students' table
INSERT INTO students (first_name, last_name, email, enrollment_date) 
VALUES ('John', 'Doe', 'john.doe@example.com', '2024-11-21');

-- Insert multiple rows
INSERT INTO students (first_name, last_name, email, enrollment_date) 
VALUES 
('Jane', 'Smith', 'jane.smith@example.com', '2024-11-20'),
('Alice', 'Johnson', 'alice.johnson@example.com', '2024-11-19');

-- 2) Update Data

-- Update the email for a specific student
UPDATE students 
SET email = 'john.newemail@example.com' 
WHERE student_id = 1;

-- Disable safe update mode for this session
SET SQL_SAFE_UPDATES = 0;

-- Update multiple columns
UPDATE students 
SET last_name = 'Brown', email = 'jane.brown@example.com' 
WHERE first_name = 'Jane';

-- Update all rows
UPDATE students 
SET enrollment_date = '2024-11-20';

CREATE TABLE archived_students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID, auto-increment
    first_name VARCHAR(50) NOT NULL,            -- Cannot be NULL
    last_name VARCHAR(50),                      -- Optional
    email VARCHAR(100) UNIQUE,                  -- Must be unique
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- Default to today's date
);

-- Insert data into 'archived_students' by selecting from 'students'
INSERT INTO archived_students (student_id, first_name, last_name, email, enrollment_date)
SELECT student_id, first_name, last_name, email, enrollment_date
FROM students
WHERE enrollment_date = '2024-11-22';



select * from students;

select * from archived_students











