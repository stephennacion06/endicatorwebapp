from flask import Blueprint,render_template, flash, request, jsonify
from src.database import User, db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
import random
import time
from src.database import Battery, db



dashboard_page = Blueprint("dashboard_page", __name__)

@dashboard_page.route('/_stuff', methods = ['GET'])
def stuff():
    global user_id
    try: 
        battery = Battery.query.filter_by(user_id=user_id).order_by(Battery.id.desc()).first()
        print(battery.voltage)
    except:
        print("need to fix this 2")
    
    
    return jsonify(result=battery.voltage, result2=battery.current, result3=battery.SOH, result4=battery.SOC)


@dashboard_page.route('/<username>')
def user_dashboard(username):
    global user_id
    # FILTERHERE USERNAME
    #
    # battery = Battery.query.filter_by(username=username).first()
    # print(battery)
    try:
        user = User.query.filter_by(username=username).first()
        
        user_id = user.id
    except:
        print("need to fix this")
   
    return render_template('dashboard.html')