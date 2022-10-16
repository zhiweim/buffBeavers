SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-----------------------
---   DROP TABLES   ---
-----------------------

DROP TABLES IF EXISTS gyms;
DROP TABLES IF EXISTS trainers;
DROP TABLES IF EXISTS users;
DROP TABLES IF EXISTS workout_entries;
DROP TABLES IF EXISTS classes;
DROP TABLES IF EXISTS gym_classes;

-----------------------
---  CREATE TABLES  ---
-----------------------

CREATE TABLE gyms (
    gymID int NOT NULL AUTO_INCREMENT,
    location varchar(255), 
    numUser int,
    numTrainer int,
    PRIMARY KEY (gymID)
);

CREATE TABLE trainers (
    trainerID int NOT NULL AUTO_INCREMENT,
    gymID int NOT NULL,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
    numTrainee int NOT NULL,
    PRIMARY KEY (trainerID),
    FOREIGN KEY (gymID) REFERENCES gyms(gymID) ON DELETE CASCADE
);

CREATE TABLE users (
    userID int NOT NULL AUTO_INCREMENT,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
    gymID int NOT NULL,
    email varchar(255) NOT NULL,
    birthday date NOT NULL,
    trainerID int NOT NULL,
    PRIMARY KEY (userID),
    FOREIGN KEY (gymID) REFERENCES gyms(gymID) ON DELETE CASCADE,
    FOREIGN KEY (trainerID) REFERENCES trainers(trainerID) ON DELETE CASCADE
);


CREATE TABLE workout_entries (
    entryID int NOT NULL AUTO_INCREMENT,
    userID int NOT NULL,
    date date,
    workoutName varchar(255),
    workoutSet int,
    workoutRep int,
    workoutWeight int,
    PRIMARY KEY (entryID),
    FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE
);

CREATE TABLE classes (
    classID int NOT NULL AUTO_INCREMENT,
    className varchar(255) NOT NULL,
    description varchar(255),
    PRIMARY KEY (classID)
);

CREATE TABLE gym_classes (
    classID int NOT NULL,
    gymID int NOT NULL,
    meetingTime time,
    startDate date,
    endDate date,
    numEnrolled int,
    numRemaining int,
    FOREIGN KEY (gymID) REFERENCES gyms(gymID) ON DELETE CASCADE,
    FOREIGN KEY (classID) REFERENCES classes(classID) ON DELETE CASCADE
    );

-----------------------
---  INSERT VALUES  ---
-----------------------
INSERT INTO gyms (location, numUser, numTrainer)
VALUES 
    ("Portland", 1000, 25),
    ("Corvallis", 700, 10),
    ("Salem", 300, 5)
;

INSERT INTO trainers (gymID,firstName, lastName, numTrainee)
VALUES 
    (1, "Justin", "Chang", 3),
    (3, "John", "Doe", 2),
    (2, "Steven", "Smith", 2)
;

INSERT INTO users (firstName, lastName, gymID, email, birthday, trainerID)
VALUES 
    ("Benny", "Beaver", 2, "BennyBeaver@oregonstate.edu", "1942-06-05", 3),
    ("Miguel", "Cabrera", 3, "CabreraM@hello.com", "2001-08-23", 2),
    ("Ananya", "Jaiswal", 1, "JaiswalA@hotmail.com", "1992-06-10", 1)
;

INSERT INTO classes (className, description)
VALUES 
    ("Aquatic Exercise", "includes variety of swimming styles and basic swimming techniques."),
    ("Beginner Weight Lifting", "Introduces newcomers to lifting and how to safely and properly workout with weights."),
    ("Badminton", "Learn how to play badminton, can be in pairs or solo.") 
;

INSERT INTO gym_classes (classID, gymID, meetingTime, startDate, endDate, numEnrolled, numRemaining)
VALUES
    (3, 1, "13:00 PM", "2022-06-10", "2022-08-10", 22, 8),
    (1, 3, "17:30 PM", "2022-04-25", "2022-05-25", 5, 25),
    (2, 2, "18:00 PM", "2022-05-01", "2022-09-01", 30, 0)
;

INSERT INTO workout_entries (date, userID, workoutName, workoutSet, workoutRep, workoutWeight)
VALUES 
    ("2021-01-10", 1, "bench", 3, 10, 135),
    ("2021-01-12", 1, "deadlift", 5, 8, 155),
    ("2021-01-13", 2, "bicep curls", 4, 12, 25)
;

-----------------
--  OPTIONAL  --
-----------------
-- SELECT * FROM gyms;
-- SELECT * FROM trainers;
-- SELECT * FROM users;
-- SELECT * FROM workout_entries;
-- SELECT * FROM classes;
-- SELECT * FROM gyms_classes;

SET FOREIGN_KEY_CHECKS=1;
COMMIT;