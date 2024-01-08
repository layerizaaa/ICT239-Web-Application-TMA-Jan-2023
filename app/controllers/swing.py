from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime, date
from flask_login import login_required, current_user
from models.users import User
from models.golfsetData import GolfSet, Swing

swing = Blueprint('swing', __name__)

# This following functions is for GET /log2 and POST /process via log2.html and log2.js

@swing.route('/log2')
@login_required
def log2():
    all_users = User.objects()
    return render_template('log2.html', name=current_user.name, panel="Swing", user_list=all_users)

@swing.route("/getClubs", methods=["POST"])
def getClubs():
    aEmail = request.form.get("aEmail")
    print(f"(Back-end) getClubs: aEmail is{aEmail}") #from ajax call

    golfset = GolfSet.getGolfSetByEmail(aEmail)

    arr=[]
    if not golfset is None:
        a_dict = golfset.getAllClubs()
        for label in a_dict:
            arr.append(label)

    #convert data into xml format
    return jsonify({"myClubs":arr}) 

@swing.route('/process2',methods= ['POST'])
@login_required
def process2():

    # Get the parameters posted by form in log2.html
    user_email = request.form['user_email']
    club_label  = request.form['club']
    swing_speed = float(request.form['swingspeed'])   
    date = request.form['date']

    datetime_object = datetime.strptime(date, '%Y-%m-%dT%M:%S')
    date_object= datetime_object.date()

    golfset = GolfSet.getGolfSetByEmail(user_email)

    try:
        
        existing_user = User.getUser(email=user_email)
        club = golfset.getClub(club_label)
        distance = Swing.computeDistance(club=club, swingSpeed=swing_speed)

        swinglogObject = Swing.createSwing(golfer=existing_user, swing_datetime=date_object, club=club , swingSpeed=swing_speed, distance=distance)
        swinglogObject.save()

    except Exception as e:
        print(f"{e}")
        return jsonify({})

    return redirect(url_for('swing.log2'))