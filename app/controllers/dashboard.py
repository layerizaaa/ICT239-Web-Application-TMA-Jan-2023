from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io
from statistics import mean
import json

from models.golfsetData import Swing
# from models.chart import CHART

dashboard = Blueprint('dashboard', __name__)

def getChartDim(user_email=None):

    # meta = {'collection': 'swings'}
    # golfer = db.ReferenceField(User)
    # swing_datetime = db.DateTimeField(['%Y-%m-%d %h:%M'])
    # club = db.ReferenceField(Club)
    # swingSpeed = db.FloatField()
    # distance = db.FloatField()
    print(user_email)
    chartDim = {} 
    labels = []
    
    # New Output 
    # var chartDim = data.chartDim; 
    # {'golfer_1': [[datetime1, 23], [datetime2, 21.5], ...], 'golfer_2': [[],[], ... ],  ...}
    # var xLabels = data.labels;
    # [] 

    try:
        swings = Swing.objects()
        chartDim = {}

        if user_email == None:
            for swing_object in swings:
                print(swing_object)
                if not user_email or (swing_object.golfer.email == user_email): 
                    swing = chartDim.get(swing_object.golfer.name)
                    if not swing:
                        chartDim[swing_object.golfer.name]=[[swing_object.swing_datetime, swing_object.distance]]
                                        
                    else:
                        swing.append([swing_object.swing_datetime, swing_object.distance])
                        
            # make sure the datetime line is sorted    
            for value in chartDim.values():
                value.sort(key=lambda x: x[0])

            return chartDim, labels

        else:
            for swing_object in swings:
                if not user_email or (swing_object.golfer.email == user_email):
                    club_label = swing_object.club.label
                    swing_data = chartDim.get(club_label)
                    if not swing_data:
                        chartDim[club_label] = [[swing_object.swing_datetime, swing_object.distance]]
                    else:
                        swing_data.append([swing_object.swing_datetime, swing_object.distance])

            return chartDim, []

    except:
        return None

# swingchart GET and POST act in tandum, POST done via swingchart.js

@dashboard.route('/swingchart', methods=['GET', 'POST'])
@login_required
def chart():
    if request.method == 'GET':
        #I want to get some data from the service
        return render_template('swingchart.html', name=current_user.name, email_id=current_user.email, panel="Swing Chart")    
    elif request.method == 'POST':
        
        # Retrieve data from AJAX POST
        res = request.get_data("data")
        d_token = json.loads(res)
        email_id = d_token['email_id'] 
                
        # if it is admin, all swing records are to be charted
        if email_id == "admin@abc.com":
            email_id = None
        
        chartDim, labels = getChartDim(user_email=email_id)
        
        return jsonify({'chartDim': chartDim, 'labels': labels})

# Only GET, /dashboard only produces the dashboard view 
   
@dashboard.route('/dashboard')
@login_required
def render_dashboard():
    return render_template('dashboard.html', name=current_user.name, panel="")




