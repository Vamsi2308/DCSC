--------------------

-- 1. How many animals of each type have outcomes?

SELECT animal_type, COUNT(DISTINCT animal_id) as num_animals
FROM dim_animal
GROUP BY animal_type;


-- 2. How many animals are there with more than 1 outcome?
SELECT COUNT(animal_id) as num_animals_with_multiple_outcomes
FROM (
    SELECT animal_id, COUNT(DISTINCT outcome_id) as num_outcomes
    FROM fct_animal
    GROUP BY animal_id
) subquery
WHERE num_outcomes > 1;


-- 3. What are the top 5 months for outcomes? 

SELECT month, COUNT(*) as num_outcomes
FROM dim_time
GROUP BY month
ORDER BY num_outcomes DESC
LIMIT 5;

-- Calculating the ages, A "Kitten" is a "Cat" who is less than 1 year old. 
-- A "Senior cat" is a "Cat" who is over 10 years old. An "Adult" is a cat who is between 1 and 10 years old.
-- Kittens (less than 1 year old)
SELECT 'Kitten' as age_group, COUNT(animal_id) as count
FROM dim_animal
WHERE animal_type = 'Cat' AND age_upon_outcome < '1 year'
GROUP BY age_group;

-- Adults (1 to 10 years old)
SELECT 'Adult' as age_group, COUNT(animal_id) as count
FROM dim_animal
WHERE animal_type = 'Cat' AND age_upon_outcome >= '1 year' AND age_upon_outcome <= '10 years'
GROUP BY age_group;

-- Seniors (over 10 years old)
SELECT 'Senior' as age_group, COUNT(animal_id) as count
FROM dim_animal
WHERE animal_type = 'Cat' AND age_upon_outcome > '10 years'
GROUP BY age_group;

-- 4.1 What is the total number percentage of kittens, adults, and seniors, whose outcome is "Adopted"?
WITH CatAgeCategories AS (
    SELECT animal_id, 
           CASE
               WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) < 1 THEN 'Kitten'
               WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) >= 10 THEN 'Senior'
               ELSE 'Adult'
           END AS age_category
    FROM dim_animal
    WHERE animal_type = 'Cat')

SELECT age_category, 
       (COUNT(DISTINCT animal_id) * 100.0 / SUM(COUNT(DISTINCT animal_id)) OVER()) as percentage
FROM CatAgeCategories
WHERE animal_id IN (
    SELECT animal_id
    FROM fct_animal
    WHERE outcome_type = 'Adopted'
)
GROUP BY age_category;


-- 4.2 Conversely, among all the cats who were "Adopted," 
-- what is the total number percentage of kittens, adults, and seniors?
WITH AdoptedCats AS (
    SELECT animal_id
    FROM fct_animal
    WHERE outcome_type = 'Adopted'
)

SELECT age_category, 
       (COUNT(DISTINCT animal_id) * 100.0 / SUM(COUNT(DISTINCT animal_id)) OVER()) as percentage
FROM CatAgeCategories
WHERE animal_id IN (
    SELECT animal_id
    FROM AdoptedCats
)
GROUP BY age_category;

-- For each date, what is the cumulative total of outcomes up to and including this date?

SELECT datetime, 
       (SELECT COUNT(*) 
        FROM fct_animal AS f
        WHERE f.date_id <= t.date_id) as cumulative_total
FROM dim_time AS t
ORDER BY datetime;

