from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ==============================================
# Home Page
# ==============================================
@app.route("/")
def home_page():
    return render_template("dashboard.html")

# ==============================================
# Providers Page
# ==============================================
@app.route("/providers")
def providers_page():
    return render_template("providers.html")

# ==============================================
# Reviews Page
# ==============================================
@app.route("/reviews")
def reviews_page():
    return render_template("reviews.html")



# ==============================================
# Login/Register Page
# ==============================================
@app.route("/login_register")
def login_register_page():
    return render_template("login_register.html")


# ==============================================
# Register Route
# ==============================================

@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect("/login_register")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.register_user(data)
    session['user_id'] = user_id
    return redirect("/show/appointments")

# ==============================================
# Login Route
# ==============================================
@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"] 
    }
    user_in_db = User.get_by_email(data)

    validation_data = {
        "user": user_in_db,
        "password": request.form['password']
    }

    if not User.validate_login(validation_data):
        return redirect("/login_register")
    
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/show/appointments")


# ==============================================
# Dashboard Route
# ==============================================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/")

    data = {
        "user_id" : session["user_id"]
    }
    user = User.get_user_info(data)
    return render_template("dashboard.html", user = user)

# ==============================================
# Logout Route
# ==============================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
