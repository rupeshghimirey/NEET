from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.appointment import Appointment
from flask_app.models.appointmentAll import AppointmentAll
from flask_app.models.time import Time
from flask_app.models.user import User


# ==============================================
#Appointments Page
# ==============================================
@app.route("/appointments")
def create_appointment_page():
    list_of_all_times = Time.get_all_times();
    return render_template("create_appointment.html",list_of_all_times = list_of_all_times)

# ==============================================
#Separate Appointment where no login required
# ==============================================
@app.route("/appointments/all")
def create_all_appointment_page():
    list_of_all_times = Time.get_all_times();
    return render_template("appointment_for_all.html", list_of_all_times = list_of_all_times)

# ==============================================
# Add Appointment
# ==============================================
@app.route('/book/appointment', methods=["POST"])
def add_appointment():
    if not Appointment.validate_appointment(request.form):
        return redirect('/appointments')
        
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "phone_number": request.form["phone_number"],
        "date": request.form["date"],
        "time": request.form["time"],
        "user_id": session['user_id'],
        
        
    }
    Appointment.save_appointment(data)
    flash("New Appointment successfully added!")
    return redirect("/show/appointments")

# ==============================================
#Add Appointment Where where no login required
# ==============================================
@app.route('/book/appointment/all', methods=["POST"])
def add_appointment_all():
    if not Appointment.validate_appointment(request.form):
        return redirect('/appointments/all')
        
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "phone_number": request.form["phone_number"],
        "date": request.form["date"],
        "time": request.form["time"],
    }
    AppointmentAll.save_appointment_all(data)
    flash("New Appointment successfully added!")
    return redirect("/")
# ==============================================
# Show Appointments Page
# ==============================================
@app.route("/show/appointments")
def show_appointment_page():
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/login_register")
    
    data = {
        "user_id" : session["user_id"]
    }
    all_appointments_with_user = Appointment.get_all_appointments_with_user(data)
    user = User.get_user_info(data)


    return render_template("show_appointments.html", user = user, all_appointments_with_user=all_appointments_with_user)
# ==============================================
#Edit Appointments Page
# ==============================================
@app.route("/edit/<int:appointment_id>/")
def edit_painting(appointment_id):
    list_of_all_times = Time.get_all_times();
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/appointments")
    data = {
        "appointment_id" : appointment_id,
        "user_id" : session["user_id"]

    }

    appointment_one = Appointment.get_one_appointment_with_user(data)
    return render_template("edit_appointment.html", appointment_one = appointment_one,list_of_all_times=list_of_all_times)

# ==============================================
# Update Appointments 
# ==============================================
@app.route('/edit/appointment/<int:appointment_id>', methods=["POST"])
def update_painting(appointment_id):

    if not Appointment.validate_appointment(request.form):
        return redirect('/edit/' + str(appointment_id))
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/appointments")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "phone_number": request.form["phone_number"],
        "date": request.form["date"],
        "time": request.form["time"],
        "user_id": session['user_id'],
        "appointment_id" : appointment_id,
    }
    Appointment.update_appointment(data)
    flash("Appointment successfully updated")
    return redirect('/show/appointments')

@app.route("/delete/<int:appointment_id>")
def delete_appointment(appointment_id):
    if "user_id" not in session:
        flash("Please register/login before continuing!")
        return redirect("/appointments")
    data = {
        "appointment_id" : appointment_id
    }
    Appointment.delete_appointment(data)
    flash("Appointment successfully deleted")
    return redirect("/show/appointments")
