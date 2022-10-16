--Query for creating a new gym
INSERT INTO gyms(location, numOfUser, numOfTrainer)
VALUES (:location_Input, :numOfUser_Input, :numOfTrainer_Input);

--Query for creating a new trainer
INSERT INTO trainers(gymID, firstName, lastName, numTrainee)
VALUES (:gymID_Input, :firstName_Input, :lastName_Input, numTrainee_Input);

--Query for creating a new user
INSERT INTO users(firstName, lastName, gymID, email, birthday, trainerID)
VALUES (:firstName_Input, :lastName_Input, :gym_Input, :email_Input, :birthday_Input, :trainerID_Input);

--Query for creating a new workout entry
INSERT INTO workout_entries(userID, date, workout1Name, workout1Set, workout1Rep, workout1Weight)
VALUES (:userID_Input, :date_Input, :workout1Name_Input, :workout1Set_Input, :workout1Rep_Input, :workout1Weight_Input);

--Query for creating a new class
INSERT INTO classes(className, description)
VALUES (:className, :description_Input);

--Query for creating a new gym_class
INSERT INTO gym_classes(classID, gymID, meetingTime, startDate, endDate, numEnrolled, numRemaining)
VALUES (:classID_Input, :gymID_Input, :meetingTime_Input, :startDate_Input, :endDate_Input, :numEnrolled_Input, :numRemaining_Input);

--Qyery got retrieving all gyms
SELECT * 
FROM gyms;

--Query for retrieving all users
SELECT *
FROM users
ORDER BY lastName;

--Query for retrieving all workout entries 
SELECT *
FROM workout_entries;

--Query for retrieving all workout entries by a user
SELECT * 
FROM workout_entries
WHERE userID = :userID_Input;

--Query for retrieving all classes
SELECT *
FROM classes;

--Query for retrieving all gym_classes
SELECT * 
FROM gym_classes;

--Query for updating a gym
UPDATE gyms
SET location = :location_Input, numOfUser = :numOfUser_Input, numOfTrainer = :numOfTrainer_Input
WHERE gymID = gymID_from_update_form;

--Query for updating a trainer
UPDATE trainers
SET gymID = :gymID_Input, firstName = :firstName_Input, lastName = :lastName_Input, numTrainee = :numTrainee_Input
WHERE trainerID = trainerID_from_update_form;

--Query for updating a user
UPDATE users
SET firstName = :firstName_Input, lastName = :lastName_Input, gymID = :gymID_Input, email = :email_Input, birthday = :birthday_Input, trainerID = :trainerID_Input
WHERE userID = userID_from_update_form;

--Query for updating a workout entry
UPDATE workout_entries
SET userID = :userID_Input, date = :date_input, workout1Name = :workout1Name_Input, workout1Set = :workout1Set_Input, workout1Rep = :workout1Rep_Input, workout1Weight = :workout1Weight_Input
WHERE entryID = entryID_from_update_form;

--Query for updating a class
UPDATE classes
SET className = :className_Input, description = :description_Input
WHERE classID = classID_from_update_form;

--Query for updating a gym_class
UPDATE gym_classes
SET classID = :classID_Input, gymID = :gymID_Input, meetingTime = :meetingTime_Input, startDate = :startDate_Input, endDate = :endDate_Input, numEnrolled = :numEnrolled_Input, numRemaining = :numRemaining_Input
WHERE classID = classID_from_update_form

--Query for deleting a gym
DELETE FROM gyms
WHERE gymID = :gymID_Input;

--Query for deleting a trainer
DELETE FROM trainer
WHERE trainerID = :trainerID_Input;

--Query for deleting a user
DELETE FROM users
WHERE userID = :userID_Input;

--Query for deleting a workout entry
DELETE FROM workout_entries
WHERE entryID = :entryID_Input;

--Query for deleting a class
DELETE FROM classes
WHERE classID = :classID_Input;

--Query for deleting a gym_class
DELETE FROM gym_classes
WHERE classID = :classID_Input;

--Query for retrieving gymID, location for dropdowns
SELECT gymID, location
FROM gyms;

--Query for retrieving trainerID, firstName, lastName for dropdowns
SELECT trainerID, firstName, lastName
FROM trainers;

--Query for retrieving userID, firstName, lastName for dropdowns
SELECT userID, firstName, lastName
FROM users;

--Query for retrieving classID, className for dropdowns
SELECT classID, className
FROM classes;

