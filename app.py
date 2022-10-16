# Citation for the following code: 
# Date: 06/05/2022
# Adapted from app.py from:
# https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/app.py

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import database.db_connector as db
import os

app = Flask(__name__)
db_connection = db.connect_to_database()

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_xxxx"
app.config["MYSQL_PASSWORD"] = "xxxx"
app.config["MYSQL_DB"] = "cs340_xxxx"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.j2")
    
#---- Gyms Entity ----#
@app.route("/gyms", methods=["POST", "GET"])
def gym():
    # inserts a new gym into database
    if request.method == "POST":
        if request.form.get("Add_Gym"):
            location = request.form["location"]
            numUser = request.form["numUser"]
            numTrainer = request.form["numTrainer"]

            query = "INSERT INTO gyms (location, numUser, numTrainer) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (location, numUser, numTrainer))
            mysql.connection.commit()

            return redirect("/gyms")

    # query for users for templates
    if request.method == "GET":
        query = "SELECT * from gyms"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("gyms.j2", data=data)

@app.route("/edit_gyms/<int:gymID>", methods=["POST", "GET"])
def edit_gym(gymID):    
    if request.method == "GET":
        query = "SELECT * FROM gyms WHERE gymID = %s" % (gymID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
 
        return render_template("edit_gyms.j2", data=data)
 
    if request.method == "POST":
        if request.form.get("Edit_Gym"):
            numUser = request.form["numUser"]
            numTrainer = request.form["numTrainer"]
 
            query = "UPDATE gyms SET gyms.numUser = %s, gyms.numTrainer = %s WHERE gyms.gymID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (numUser, numTrainer, gymID))
            mysql.connection.commit()
 
            return redirect("/gyms")

@app.route("/delete_gyms/<int:gymID>")
def delete_gym(gymID):
    query = "DELETE FROM gyms WHERE gymID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (gymID,))
    mysql.connection.commit()

    return redirect("/gyms")

#---- Users Entity ----#
@app.route("/users", methods=["POST", "GET"])
def user():
    # inserts user into database
    if request.method == "POST":
        if request.form.get("Add_User"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            gymID = request.form["gymID"]
            email = request.form["email"]
            birthday = request.form["birthday"]
            trainer = request.form["trainer"]

        # pulls up info for input user ID
        if request.form.get("search"):
            userID = request.form["userID"]
            query = "SELECT * FROM users WHERE userID = %s" % (userID)
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return render_template("/users.j2", data=data)

        query = "INSERT INTO users (firstName, lastName, gymID, email, birthday, trainerID) VALUES (%s, %s, %s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (firstName, lastName, gymID, email, birthday, trainer))
        mysql.connection.commit()

        return render_template("users.j2")

    # query for users for templates
    if request.method == "GET":
        # query for users
        query = "SELECT * FROM users ORDER BY lastName"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #dropdown for showing locations
        query2 = "SELECT gymID, location FROM gyms" 
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_data = cur.fetchall()

        query3 = "SELECT trainerID, firstName, lastName FROM trainers" 
        cur = mysql.connection.cursor()
        cur.execute(query3)
        trainer_data = cur.fetchall()

        return render_template("users.j2", data = data, gyms=gym_data, trainers=trainer_data)

@app.route("/edit_users/<int:userID>", methods=["POST", "GET"])
def edit_users(userID):    
    if request.method == "GET":
        query = "SELECT * FROM users WHERE userID = %s" % (userID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #query for getting dropdown menu from trainers
        query2 = "SELECT trainerID, firstName, lastName FROM trainers"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        trainer_data = cur.fetchall()

        #query for getting dropdown menu from gyms
        query3 = "SELECT gymID, location FROM gyms"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        gym_data = cur.fetchall()
 
        return render_template("edit_users.j2", data=data, trainers=trainer_data, gyms=gym_data)
 
    if request.method == "POST":
        if request.form.get("Edit_User"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            gymID = request.form["gymID"]
            email = request.form["email"]
            birthday = request.form["birthday"]
            trainerID = request.form["trainerID"]
 
            query = "UPDATE users SET users.firstName = %s, users.lastName = %s, users.gymID = %s, users.email = %s, users.birthday = %s, users.trainerID = %s WHERE users.userID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, gymID, email, birthday, trainerID, userID))
            mysql.connection.commit()
 
            return redirect("/users")


@app.route("/delete_users/<int:userID>")
def delete_user(userID):
    query = "DELETE FROM users WHERE userID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (userID,))
    mysql.connection.commit()

    return redirect("/users")


#---- Trainers Entity ----#
@app.route("/trainers", methods=["POST", "GET"])
def trainer():
    # inserts user into database
    if request.method == "POST":
        if request.form.get("Add_Trainer"):
            gymID = request.form["gymID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            numTrainee = request.form["numTrainee"]

            query = "INSERT INTO trainers (gymID, firstName, lastName, numTrainee) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (gymID, firstName, lastName, numTrainee))
            mysql.connection.commit()

            return redirect("/trainers")

    # query for trainers for templates
    if request.method == "GET":
        # query for users
        query = "SELECT * FROM trainers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #dropdown for showing locations
        query2 = "SELECT gymID, location FROM gyms" 
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_data = cur.fetchall()

        return render_template("trainers.j2", data=data, gyms=gym_data)

@app.route("/edit_trainers/<int:trainerID>", methods=["POST", "GET"])
def edit_trainer(trainerID):    
    if request.method == "GET":
        query = "SELECT * FROM trainers WHERE trainerID = %s" % (trainerID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #query for getting dropdown menu from gyms
        query2 = "SELECT gymID, location FROM gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_data = cur.fetchall()
 
        return render_template("edit_trainers.j2", data=data, gyms=gym_data)
 
    if request.method == "POST":
        if request.form.get("Edit_Trainer"):
            gymID = request.form["gymID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            numTrainee = request.form["numTrainee"]
 
            query = "UPDATE trainers SET trainers.gymID = %s, trainers.firstName = %s, trainers.lastName = %s, trainers.numTrainee = %s WHERE trainers.trainerID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (gymID, firstName, lastName, numTrainee, trainerID))
            mysql.connection.commit()
 
            return redirect("/trainers")

#handles the route for deleting trainers from database
@app.route("/delete_trainers/<int:trainerID>")
def delete_trainer(trainerID):
    query = "DELETE FROM trainers WHERE trainerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (trainerID,))
    mysql.connection.commit()

    return redirect("/trainers")


#---- Workout_Entries Entity ----#
@app.route("/workout_entries", methods=["POST", "GET"])
def workout_entry():
    # inserts user into database
    if request.method == "POST":
        if request.form.get("Add_Workout_Entry"):
            userID = request.form["userID"]
            date = request.form["date"]
            workoutName = request.form["workoutName"]
            workoutSet = request.form["workoutSet"]
            workoutRep = request.form["workoutRep"]
            workoutWeight = request.form["workoutWeight"]

        # search query for getting all workout entries by a user
        if request.form.get("search"):
            userID = request.form["userID"]
            query = "SELECT * FROM workout_entries WHERE userID = %s" % (userID)
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return render_template("/workout_entries.j2", data=data)

        query = "INSERT INTO workout_entries (userID, date, workoutName, workoutSet, workoutRep, workoutWeight) VALUES (%s, %s, %s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (userID, date, workoutName, workoutSet, workoutRep, workoutWeight))
        mysql.connection.commit()

        return redirect("/workout_entries")

    # query for users for templates
    if request.method == "GET":
        # query for getting workout entries
        query = "SELECT * FROM workout_entries"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #query for getting dropdown menu from users
        query2 = "SELECT userID, firstName, lastName FROM users"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        user_data = cur.fetchall()

        return render_template("workout_entries.j2", data=data, users=user_data)

@app.route("/edit_workout_entries/<int:entryID>", methods=["POST", "GET"])
def edit_workout_entries(entryID):    
    if request.method == "GET":
        query = "SELECT * FROM workout_entries WHERE entryID = %s" % (entryID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #query for getting dropdown menu from trainers
        query2 = "SELECT userID, firstName, lastName FROM users"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        user_data = cur.fetchall()
 
        return render_template("edit_workout_entries.j2", data=data, users=user_data)
 
    if request.method == "POST":
        if request.form.get("Edit_Workout_Entries"):
            userID = request.form["userID"]
            date = request.form["date"]
            workoutName = request.form["workoutName"]
            workoutSet = request.form["workoutSet"]
            workoutRep = request.form["workoutRep"]
            workoutWeight = request.form["workoutWeight"]
 
            query = "UPDATE workout_entries SET workout_entries.userID = %s, workout_entries.date = %s, workout_entries.workoutName = %s, workout_entries.workoutSet = %s, workout_entries.workoutRep = %s, workout_entries.workoutWeight = %s WHERE workout_entries.entryID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (userID, date, workoutName, workoutSet, workoutRep, workoutWeight, entryID))
            mysql.connection.commit()
 
            return redirect("/workout_entries")

#handles the route for deleting an entry from database
@app.route("/delete_workout_entries/<int:entryID>")
def delete_entry(entryID):
    query = "DELETE FROM workout_entries WHERE entryID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (entryID,))
    mysql.connection.commit()

    return redirect("/workout_entries")

#---- Classes Entity (Will be called class descriptions for easier understanding on website) ----#
@app.route("/class_descriptions", methods=["POST", "GET"])
def class_description():
    # inserts a class into database
    if request.method == "POST":
        if request.form.get("Add_Class_Description"):
            className = request.form["className"]
            description = request.form["description"]

            query = "INSERT INTO classes (className, description) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (className, description))
            mysql.connection.commit()

            return redirect("/class_descriptions")

    # query for classes for templates
    if request.method == "GET":
        # query for getting classes 
        query = "SELECT * FROM classes"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("class_descriptions.j2", data=data)

@app.route("/edit_class_descriptions/<int:classID>", methods=["POST", "GET"])
def edit_class_descriptions(classID):    
    if request.method == "GET":
        query = "SELECT * FROM classes WHERE classID = %s" % (classID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
 
        return render_template("edit_class_descriptions.j2", data=data)
 
    if request.method == "POST":
        if request.form.get("Edit_Class_Descriptions"):
            className = request.form["className"]
            description = request.form["description"]
 
            query = "UPDATE classes SET classes.className = %s, classes.description = %s WHERE classes.classID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (className, description, classID))
            mysql.connection.commit()
 
            return redirect("/class_descriptions")

#handles the route for deleting an entry from database
@app.route("/delete_class_descriptions/<int:classID>")
def delete_class_description(classID):
    query = "DELETE FROM classes WHERE classID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (classID,))
    mysql.connection.commit()

    return redirect("/class_descriptions")

#---- Gym_Classes Entity (Will be called class schedules in website)----#
@app.route("/class_schedules", methods=["POST", "GET"])
def class_schedule():
    # inserts a gym_classes into database
    if request.method == "POST":
        if request.form.get("Add_Class_Schedule"):
            classID = request.form["classID"]
            gymID = request.form["gymID"]
            meetingTime = request.form["meetingTime"]
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            numEnrolled = request.form["numEnrolled"]
            numRemaining = request.form["numRemaining"]

            query = "INSERT INTO gym_classes (classID, gymID, meetingTime, startDate, endDate, numEnrolled, numRemaining) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (classID, gymID, meetingTime, startDate, endDate, numEnrolled, numRemaining))
            mysql.connection.commit()

            return redirect("/class_schedules")

    # query for classes for templates
    if request.method == "GET":
        # query for getting gym_classes 
        query = "SELECT * FROM gym_classes"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #query for getting dropdown menu from gyms
        query2 = "SELECT gymID, location FROM gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_data = cur.fetchall()

        #query for getting dropdown for classes
        query3 = "SELECT classID, className FROM classes"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        class_data = cur.fetchall()

        return render_template("class_schedules.j2", data=data, gyms=gym_data, classes=class_data)

@app.route("/edit_class_schedules/<int:classID>", methods=["POST", "GET"])
def edit_class_schedules(classID):    
    if request.method == "GET":
        query = "SELECT * FROM gym_classes WHERE classID = %s" % (classID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #query for getting dropdown menu from gyms
        query2 = "SELECT gymID, location FROM gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_data = cur.fetchall()

        #query for getting dropdown for classes
        query3 = "SELECT classID, className FROM classes"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        class_data = cur.fetchall()
 
        return render_template("edit_class_schedules.j2", data=data, gyms=gym_data, classes=class_data)
 
    if request.method == "POST":
        if request.form.get("Edit_Class_Schedules"):
            classID = request.form["classID"]
            gymID = request.form["gymID"]
            meetingTime = request.form["meetingTime"]
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            numEnrolled = request.form["numEnrolled"]
            numRemaining = request.form["numRemaining"]

            query = "UPDATE gym_classes SET gym_classes.classID = %s, gym_classes.gymID = %s, gym_classes.meetingTime = %s, gym_classes.startDate = %s, gym_classes.endDate = %s, gym_classes.numEnrolled = %s, gym_classes.numRemaining = %s WHERE gym_classes.classID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (classID, gymID, meetingTime, startDate, endDate, numEnrolled, numRemaining, classID))
            mysql.connection.commit()
 
            return redirect("/class_schedules")

#handles the route for deleting an entry from database
@app.route("/delete_class_schedules/<int:classID>")
def delete_class_schedule(classID):
    query = "DELETE FROM gym_classes WHERE classID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (classID,))
    mysql.connection.commit()

    return redirect("/class_schedules")

# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":

    app.run(port=57631, debug=True)