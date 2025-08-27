#===========================================================
# Maintenance Tracker
# Dylan Collins
#-----------------------------------------------------------
# Maintenance tracker used for tracking vehicle maintenance throughout life of vehicles 
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
init_session(app)
init_logging(app)
init_error(app)
init_datetime(app)


#-----------------------------------------------------------
# Home page
#-----------------------------------------------------------
@app.get("/")
def index():
    return render_template("pages/home.jinja")


#-----------------------------------------------------------
# About page
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")


#-----------------------------------------------------------
# Vehicle list page
#-----------------------------------------------------------
@app.get("/vehicle.list/")
def vehicle_list():
    return render_template("pages/vehicle.list.jinja")


#-----------------------------------------------------------
# Add/Edit a vehicle
#-----------------------------------------------------------
@app.get("/add.edit.a.vehicle")
def add_edit_a_vehicle():
    return render_template("pages/add.edit.a.vehicle.jinja")


#-----------------------------------------------------------
# Maintenance info page
#-----------------------------------------------------------
@app.get("/maintenance.info")
def maintenance_info():
    return render_template("pages/maintenance info.jinja")


#-----------------------------------------------------------
# Show all maintenance logs
#-----------------------------------------------------------
@app.get("/details/")
def show_all_details():
    with connect_db() as client:
        sql = "SELECT details FROM INFO"
        result = client.execute(sql)
        logs = result.fetchall()
    return render_template("pages/details.jinja", details=logs)


#-----------------------------------------------------------
# Add a maintenance log
#-----------------------------------------------------------
@app.post("/add")
@login_required
def add_a_log():
    vehicle_id  = html.escape(request.form.get("vehicle_id") or "")
    action_taken = html.escape(request.form.get("action_taken") or "")
    details   = html.escape(request.form.get("details") or "")
    odometer_kms = request.form.get("odometer_kms") or 0

    with connect_db() as client:
        sql = """
        INSERT INTO INFO (vehicle_id, action_taken, details, odometer_kms, date)
        VALUES (?, ?, ?, ?, ?)
        """
        params = [vehicle_id, action_taken, details, odometer_kms, init_datetime]
        client.execute(sql, params)

    flash(f"Maintenance log for vehicle {vehicle_id} added", "success")
    return redirect("/") 


#-----------------------------------------------------------
# Delete a maintenance log
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
@login_required
def delete_a_log(id):
    user_id = session["user_id"]
    with connect_db() as client:
        sql = """
        DELETE FROM INFO
        WHERE id = ? AND vehicle_id IN (SELECT id FROM VEHICLES WHERE user_id = ?)
        """
        client.execute(sql, [id, user_id])

    flash("Maintenance log deleted", "success")
    return redirect("/")


#-----------------------------------------------------------
# Registration page
#-----------------------------------------------------------
@app.get("/register")
def register_form():
    return render_template("pages/register.jinja")


#-----------------------------------------------------------
# User registration
#-----------------------------------------------------------
@app.post("/add-user")
def add_user():
    name     = html.escape(request.form.get("name") or "")
    username = html.escape(request.form.get("username") or "")
    password = request.form.get("password")  

    if not username or not password:
        flash("Username and password are required", "error")
        return redirect("/register")

    with connect_db() as client:
        sql = "SELECT 1 FROM USERS WHERE username = ?"
        result = client.execute(sql, [username])
        rows = result.fetchall()
        if rows:
            flash("Username already exists", "error")
            return redirect("/register")

        password_hash = generate_password_hash(password)
        sql = "INSERT INTO USERS (name, username, password_hash) VALUES (?, ?, ?)"
        client.execute(sql, [name, username, password_hash])

    flash("Registration successful. Please login.", "success")
    return redirect("/login")


#-----------------------------------------------------------
# Login page
#-----------------------------------------------------------
@app.get("/login")
def login_form():
    return render_template("pages/login.jinja")


#-----------------------------------------------------------
# User login
#-----------------------------------------------------------
@app.post("/login-user")
def login_user():
    username = html.escape(request.form.get("username") or "")
    password = request.form.get("password")  

    if not username or not password:
        flash("Username and password are required", "error")
        return redirect("/login")

    with connect_db() as client:
        sql = "SELECT * FROM USERS WHERE username = ?"
        result = client.execute(sql, [username])
        rows = result.fetchall()

        if rows:
            user = rows[0]
            if check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["name"] if "name" in user.keys() else ""
                session["logged_in"] = True
                flash("Login successful", "success")
                return redirect("/")
            else:
                flash("Invalid username or password", "error")
        else:
            flash("Invalid username or password", "error")
    return redirect("/login")


#-----------------------------------------------------------
# Logout
#-----------------------------------------------------------
@app.get("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/")
