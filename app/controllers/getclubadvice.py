from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime, date
from flask_login import login_required, current_user
from models.users import User
from models.golfsetData import GolfSet, Swing

clubadvice = Blueprint('getclubadvice', __name__)

@clubadvice.route('/getclubadvice')
@login_required
def getclubadvice():
    return render_template('getclubadvice.html', name=current_user.name, email_id=current_user.email, panel="Get Club Advice")   

@clubadvice.route("/process", methods=["POST"])
def process():
    swing_speed = float(request.form['swing_speed'])
    distance = float(request.form['distance'])
    
    try:

        user_golfset = GolfSet.getGolfSetByEmail(current_user.email) #Get golfset of user

        arr=[]
        delta = 50  # Default delta value
        if user_golfset:
            for club_label, club in user_golfset.clubs.items():
                #print(club_label)
                length = format(Swing.getClubLength(club), ".1f") #format the length to one decimal place
                #print(length)
                loft = club.getClubHeadloft()
                #print(loft)
                estimated_distance = Swing.computeDistance(club, swing_speed)
                #print(estimated_distance)
                difference = abs(estimated_distance - distance)
                #print(difference)
                if difference <= delta:
                    arr.append([club_label, length, loft])
                print(arr)
            
        else:
            # if No Golfset
            return jsonify({'clubs': None})
    
    except Exception as e:
        print(f"{e}")
        return jsonify({})

    return jsonify({'clubs': arr})


    
    
    

