
 -- Creating tables 


CREATE TABLE IF NOT EXISTS dim_animal (
animal_id VARCHAR PRIMARY KEY,
name VARCHAR,
date_of_birth date,
animal_type VARCHAR,
breed VARCHAR,
color VARCHAR
);

CREATE TABLE IF NOT EXISTS dim_time (
date_id serial PRIMARY KEY,
datetime TIMESTAMP,
month VARCHAR,
year INT
);

CREATE TABLE IF NOT EXISTS dim_outcometype (
outcome_id serial PRIMARY KEY,
outcome_type VARCHAR,
outcome_subtype VARCHAR
);

CREATE TABLE IF NOT EXISTS fct_animal (
breed_id serial PRIMARY KEY,
animal_id VARCHAR,
date_id INT,
outcome_id INT,
month VARCHAR,
year INT,
outcome_type VARCHAR,
FOREIGN KEY (animal_id) REFERENCES dim_animal(animal_id),
FOREIGN KEY (date_id) REFERENCES dim_time(date_id),
FOREIGN KEY (outcome_id) REFERENCES dim_outcometype(outcome_id)
);

-----------------------------------
 -- Inital test create table

/*CREATE TABLE outcomes(
    animal_id VARCHAR,
    animal_name VARCHAR,
    ts TIMESTAMP,
    DOB date,
    outcome_type VARCHAR,
    outcome_subtype VARCHAR,
    animal_type VARCHAR,
    age VARCHAR,
    breed VARCHAR,
    color VARCHAR,
    month  VARCHAR,
    year INT,
    sex VARCHAR
);*/
