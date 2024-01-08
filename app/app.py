# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe

from flask_login import login_required, current_user
from flask import render_template, request
from app import app, db, login_manager

# Register Blueprint so we can factor routes
from controllers.swing import swing
from controllers.dashboard import dashboard
from controllers.auth import auth
from controllers.getclubadvice import clubadvice
# from auth import auth

# register blueprint from respective module
app.register_blueprint(dashboard)
app.register_blueprint(auth)
app.register_blueprint(swing)
app.register_blueprint(clubadvice)

# from models.chart import CHART
from models.users import User
import csv
import io

# from models.golfsetData import
from models.golfsetData import Club, GolfSet, Swing

from datetime import datetime

# Load the current user if any
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/base')
@login_required
def show_base():
    return render_template('base.html')

@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template("upload.html", name=current_user.name, panel="Upload", Users=User.getAllUsers()) #added Users=User.getAllUsers() for Jinja reference in upload.html
    
    elif request.method == 'POST':      
        type = request.form.get('type')
        file = request.files.get('file')                    
        data = file.read().decode('utf-8')
                
        aDataType = request.form.get("datatype")
        aEmail = request.form.get("users")
        
        #create GolfSet
        golfset = GolfSet.createGolfSet(aEmail)
        
        if type == 'create':
            print("No create Action yet")

        elif type == 'upload':
            #if data type is GolfSet
            if aDataType == "GolfSet":
                #readfile
                dict_reader = csv.reader(io.StringIO(data), delimiter=',', quotechar='"')
                file.close() 
                               
                for item in dict_reader: #returns list of each row in .txt file
                    print(item)
                    #create club in database
                    club = Club.createClub(item)
                    #add club to golf set
                    golfset.addClub(club)

            #if data type is Swings
            elif aDataType == "Swings":
                #readfile
                dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
                file.close()

                for item in list(dict_reader): #returns list of each row in .txt file
                    print(item)
                    golfer = User.getUser(aEmail)
                    date_time = item['swing_time'].replace('"', '')
                    swing_datetime = datetime.strptime(date_time, "%Y-%f-%dT%I:%M")
                    club = golfset.getClub(item['club_label'])
                    swingSpeed = item['swing_speed']
                    distance = Swing.computeDistance(club,swingSpeed)
                    print(distance)

                    swing = Swing.createSwing(golfer, swing_datetime, club, swingSpeed, distance)
                    
                                                                               
        return render_template("upload.html", name=current_user.name, panel="Upload", Users=User.getAllUsers())

