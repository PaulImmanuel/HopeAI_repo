
-- NETFLIX DATABASE ASSIGNMENT

-- Q1
-- Display the names and emails of all users subscribed to the Premium plan.

SELECT name, email
FROM Users
WHERE subscription_plan = 'Premium';


-- Q2
-- Retrieve all Drama movies released after 2015 having a rating greater than 8.0.

SELECT title, release_year, rating
FROM Movies
WHERE genre = 'Drama'
AND release_year > 2015
AND rating > 8.0;


-- Q3
-- Calculate the average movie rating for films released from 2018 onwards.

SELECT AVG(rating) AS avg_rating
FROM Movies
WHERE release_year >= 2018;


-- Q4
-- Show users who watched Stranger Things along with the watch date and completion percentage.

SELECT U.name,
       W.watch_date,
       W.completion_percentage
FROM Users U
JOIN WatchHistory W
ON U.user_id = W.user_id
JOIN Movies M
ON W.movie_id = M.movie_id
WHERE M.title = 'Stranger Things';


-- Q5
-- Find users who have given a review rating of 5.

SELECT DISTINCT U.name
FROM Users U
JOIN Reviews R
ON U.user_id = R.user_id
WHERE R.review_rating = 5;


-- Q6
-- Display the total watch history entries for each user.

SELECT U.name,
       COUNT(W.watch_id) AS total_watched
FROM Users U
LEFT JOIN WatchHistory W
ON U.user_id = W.user_id
GROUP BY U.user_id, U.name;


-- Q7
-- Retrieve all movies watched by John Doe along with genre and rating.

SELECT M.title,
       M.genre,
       M.rating
FROM Users U
JOIN WatchHistory W
ON U.user_id = W.user_id
JOIN Movies M
ON W.movie_id = M.movie_id
WHERE U.name = 'John Doe';


-- Q8
-- Increase the rating of Stranger Things by 0.1.

UPDATE Movies
SET rating = rating + 0.1
WHERE title = 'Stranger Things';


-- Q9
-- Remove reviews associated with movies having rating less than 5.

DELETE R
FROM Reviews R
JOIN Movies M
ON R.movie_id = M.movie_id
WHERE M.rating < 5;


-- Q10
-- Find users whose completion percentage is below 100 but have submitted a review.

SELECT DISTINCT U.name
FROM Users U
JOIN WatchHistory W
ON U.user_id = W.user_id
JOIN Reviews R
ON U.user_id = R.user_id
WHERE W.completion_percentage < 100;


-- Q11
-- Display user reviews and ratings for Stranger Things.

SELECT U.name,
       R.review_text,
       R.review_rating
FROM Users U
JOIN Reviews R
ON U.user_id = R.user_id
JOIN Movies M
ON R.movie_id = M.movie_id
WHERE M.title = 'Stranger Things';


-- Q12
-- Generate a detailed Netflix viewing report including user and movie information.

SELECT U.name,
       U.email,
       M.title,
       M.genre,
       W.watch_date,
       W.completion_percentage
FROM Users U
JOIN WatchHistory W
ON U.user_id = W.user_id
JOIN Movies M
ON W.movie_id = M.movie_id;


-- Q13
-- Display each movie with the total number of reviews and average review rating.

SELECT M.title,
       COUNT(R.review_id) AS total_reviews,
       AVG(R.review_rating) AS average_rating
FROM Movies M
LEFT JOIN Reviews R
ON M.movie_id = R.movie_id
GROUP BY M.movie_id, M.title;


-- Q14
-- Find the most watched movie on Netflix.

SELECT M.title,
       COUNT(W.watch_id) AS watch_count
FROM Movies M
JOIN WatchHistory W
ON M.movie_id = W.movie_id
GROUP BY M.movie_id, M.title
ORDER BY watch_count DESC
LIMIT 1;


-- Q15
-- Find the average completion percentage for each movie.

SELECT M.title,
       AVG(W.completion_percentage) AS avg_completion
FROM Movies M
JOIN WatchHistory W
ON M.movie_id = W.movie_id
GROUP BY M.movie_id, M.title;