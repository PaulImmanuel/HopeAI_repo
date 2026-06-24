-- Data Control Language (DCL)

-- Create a new user
CREATE USER 'student_user'@'localhost'
IDENTIFIED BY 'student123';

-- Show created user
SELECT user, host
FROM mysql.user;

-- Grant permissions
GRANT SELECT, INSERT
ON practice_db.*
TO 'student_user'@'localhost';

-- Apply privilege changes
FLUSH PRIVILEGES;

-- View granted permissions
SHOW GRANTS FOR 'student_user'@'localhost';

-- Grant additional privilege
GRANT UPDATE
ON practice_db.students
TO 'student_user'@'localhost';

SHOW GRANTS FOR 'student_user'@'localhost';

-- Revoke UPDATE privilege
REVOKE UPDATE
ON practice_db.students
FROM 'student_user'@'localhost';

SHOW GRANTS FOR 'student_user'@'localhost';

-- Revoke INSERT privilege
REVOKE INSERT
ON practice_db.*
FROM 'student_user'@'localhost';

SHOW GRANTS FOR 'student_user'@'localhost';

-- Grant all privileges
GRANT ALL PRIVILEGES
ON practice_db.*
TO 'student_user'@'localhost';

SHOW GRANTS FOR 'student_user'@'localhost';

-- Remove all privileges
REVOKE ALL PRIVILEGES
ON practice_db.*
FROM 'student_user'@'localhost';

SHOW GRANTS FOR 'student_user'@'localhost';

-- Delete user
DROP USER 'student_user'@'localhost';