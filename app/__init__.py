#===========================================================
# Maintenance Tracker
# Dylan collins
#-----------------------------------------------------------
# maintenance tracker used for tracking vehicle maintenance throughout life of vehicles 
#===========================================================


from flask import Flask, render_template, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.auth    import login_required
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)
app.secret_key = "random_secret_key"
# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    return render_template("pages/home.jinja")


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")


#-----------------------------------------------------------
# Vehicle list route
#-----------------------------------------------------------
@app.get("/vehicle.list/")
def vehicle_list():
    return render_template("pages/vehicle.list.jinja")

#-----------------------------------------------------------
#add/edit a vehicle route
#-----------------------------------------------------------
@app.get("/add.edit.a.vehicle")
def add_edit_a_vehicle():
    return render_template("pages/add.edit.a.vehicle.jinja")

#-----------------------------------------------------------
#maintenance info route 
#-----------------------------------------------------------
@app.get("/maintenance.info")
def maintenance_info():
    return render_template("pages/maintenance info.jinja")



#-----------------------------------------------------------
# details page route - Show all the details, and new details form
#-----------------------------------------------------------
@app.get("/details/")
def show_all_details():
    with connect_db() as client:
        # Get all info logs for vehicles, including the owner
        sql = "SELECT * FROM INFO"
        result = client.execute(sql)
        logs = result.rows

        return render_template("pages/details.jinja", details=logs)



#-----------------------------------------------------------
# Route for adding a log.
#-----------------------------------------------------------
@app.post("/add")
@login_required
def add_a_log():
    vehicle_id  = html.escape(request.form.get("vehicle_id"))
    action_taken = html.escape(request.form.get("action_taken", ""))
    details      = html.escape(request.form.get("details", ""))
    odometer_kms = request.form.get("odometer_kms")
  

    with connect_db() as client:
        sql = """
        INSERT INTO INFO (vehicle_id, action_taken, details, odometer_kms)
        VALUES (?, ?, ?, ?)
        """
        params = [vehicle_id, action_taken, details, odometer_kms]
        client.execute(sql, params)

    flash(f"Maintenance log for vehicle {vehicle_id} added", "success")
    return redirect("/")


#-----------------------------------------------------------
# Route for deleting a log.
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
@login_required
def delete_a_log(id):
    user_id = session["user_id"]

    with connect_db() as client:
        # Only allow deleting if the user owns the vehicle
        sql = """
        DELETE FROM INFO
        WHERE id = ? AND vehicle_id IN (SELECT id FROM VEHICLES WHERE user_id = ?)
        """
        client.execute(sql, [id, user_id])

    flash("Maintenance log deleted", "success")
    return redirect("/")






#-----------------------------------------------------------
# User registration form route
#-----------------------------------------------------------
@app.get("/register")
def register_form():
    return render_template("pages/register.jinja")


#-----------------------------------------------------------
# User login form route
#-----------------------------------------------------------
@app.get("/login")
def login_form():
    return render_template("pages/login.jinja")


#-----------------------------------------------------------
# Registration route
#-----------------------------------------------------------
@app.post("/add-user")
def add_user():
    name     = html.escape(request.form.get("name") or "")
    username = html.escape(request.form.get("username") or "")
    password = request.form.get("password")  # raw, do NOT escape

    if not username or not password:
        flash("Username and password are required", "error")
        return redirect("/register")

    with connect_db() as client:
        # Check if username exists
        sql = "SELECT 1 FROM USERS WHERE username = ?"
        result = client.execute(sql, [username])
        print("Check existing username:", result.rows)

        if result.rows:
            flash("Username already exists", "error")
            return redirect("/register")

        # Hash password
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO USERS (name, username, password_hash) VALUES (?, ?, ?)"
        client.execute(sql, [name, username, password_hash])
        print(f"User {username} inserted with hash {password_hash}")

    flash("Registration successful. Please login.", "success")
    return redirect("/login")

#-----------------------------------------------------------
# Login route
#-----------------------------------------------------------
@app.post("/login-user")
def login_user():
    username = html.escape(request.form.get("username") or "")
    password = request.form.get("password")  # raw!

    if not username or not password:
        flash("Username and password are required", "error")
        return redirect("/login")

    with connect_db() as client:
        sql = "SELECT * FROM USERS WHERE username = ?"
        result = client.execute(sql, [username])
        print("DB result rows:", result.rows)

        if result.rows:
            user = result.rows[0]
            print("Stored hash:", user["password_hash"])
            if check_password_hash(user["password_hash"], password):
                # Save user info in session
                session["user_id"] = user["id"]
                session["user_name"] = user.get("name", "")
                session["logged_in"] = True

                flash("Login successful", "success")
                return redirect("/")
            else:
                print("Password mismatch!")
        else:
            print("Username not found in DB")

    flash("Invalid username or password", "error")
    return redirect("/login")

#-----------------------------------------------------------
# Logout route
#-----------------------------------------------------------
@app.get("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/")
