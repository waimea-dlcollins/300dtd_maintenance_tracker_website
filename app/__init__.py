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
from app.helpers.dates   import init_datetime, utc_datetime_str, utc_date_str, utc_time_str

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
@app.post("/")
def index():
    user_id = session.get("user_id")

    with connect_db() as client:    
        sql = """
            SELECT id, make, model, year
            FROM VEHICLES
            WHERE owner = ?
            ORDER BY id ASC
        """
        result = client.execute(sql, [user_id])
        vehicles = result.rows

        return render_template("pages/.jinja", vehicles=vehicles)



#-----------------------------------------------------------
# Vehicle page
#-----------------------------------------------------------
@app.get("/vehicle/<int:id>")
def show_vehicle(id):
    user_id = session["user_id"]

    with connect_db() as client:
        sql = """
            SELECT id, make, model, year
            FROM VEHICLES
            WHERE owner = ? AND id = ?
        """
        result = client.execute(sql, [user_id, id])
        
        if result.rows:
            vehicle = result.rows[0]

            sql = """
                SELECT action_taken, details, date, odometer
                FROM LOGS
                WHERE vehicle_id = ?
            """
            result = client.execute(sql, [id])
            logs = result.rows

    return render_template("pages/vehicle.jinja", vehicle=vehicle, logs=logs)


#-----------------------------------------------------------
# Add a log page
#-----------------------------------------------------------
@app.post("/log")
def add_log():
    with connect_db() as client:
        vehicle_id = request.form.get("vehicle_id")
        action_taken = request.form.get("action_taken")
        details = request.form.get("details")
        odometer = request.form.get("odometer")


        sql = "INSERT INTO LOGS (vehicle_id, action_taken, details, odometer) VALUES (?, ?, ?, ?)"
        client.execute(sql, [vehicle_id, action_taken, details, odometer])

        return redirect(f"/vehicle/{vehicle_id}")
    
    























#-----------------------------------------------------------
# About page
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")




#-----------------------------------------------------------
# Add a vehicle
#-----------------------------------------------------------


@app.get("/add-vehicle")
@login_required
def add_vehicle_form():
    return render_template("pages/add.a.vehicle.jinja")



@app.post("/add-vehicle")
@login_required
def add_vehicle():
    make = request.form.get("make") or ""
    model = request.form.get("model") or ""
    year = request.form.get("year") or ""

    if not make or not model:
        flash("Make and model are required", "error")
        return redirect("/add-vehicle")

    with connect_db() as client:
        sql = "INSERT INTO VEHICLES (make, model, year) VALUES (?, ?, ?)"
        params = [make, model, year]
        client.execute(sql, params)

    flash(f"Vehicle {make} {model} added", "success")
    return redirect("/")


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
from datetime import datetime

@app.post("/add")
@login_required
def add_a_log():
    vehicle_id_raw   = request.form.get("vehicle_id") or "0"
    action_taken     = html.escape(request.form.get("action_taken") or "")
    details          = html.escape(request.form.get("details") or "")
    odometer_kms_raw = request.form.get("odometer_kms") or "0"
    date_str         = request.form.get("date") or "" 

   
    try:
        vehicle_id = int(vehicle_id_raw)
    except ValueError:
        vehicle_id = 0

    try:
        odometer_kms = int(odometer_kms_raw)
    except ValueError:
        odometer_kms = 0

   
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")  
        date_ts = int(date_obj.timestamp())
    except ValueError:
        date_ts = int(datetime.now().timestamp())  

   
    with connect_db() as client:
        sql = """
        INSERT INTO INFO (vehicle_id, action_taken, details, odometer_kms, date)
        VALUES (?, ?, ?, ?, ?)
        """
        params = [vehicle_id, action_taken, details, odometer_kms, date_ts]
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
        users = result.rows
        if users:
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
        rows = result.rows

        if rows:
            user = rows[0]
            if check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["name"]
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
