from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Battery, db

batteries = Blueprint("batteries", __name__, url_prefix="/api/v1/batteries")


@batteries.route('/update')
def post_route():
    user = request.args.get('user', default = 1, type = int)
    field1 = request.args.get('field1', default = 0, type = str)
    field2 = request.args.get('field2', default = 0, type = str)
    field3 = request.args.get('field3', default = 0, type = str)
    field4 = request.args.get('field4', default = 0, type = str)
    batteries = Battery(user_id=user,
                voltage=field1, 
                current=field2, 
                SOC= field3, 
                SOH= field4,
                )
    db.session.add(batteries)
    db.session.commit()
    
    return jsonify({'user': user, 
                    "field1": field1,
                    "field2": field2})



@batteries.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_batteries():
    current_user = get_jwt_identity()

    if request.method == 'POST':

        voltage = request.get_json().get('voltage', '')
        current = request.get_json().get('current', '')
        SOC = request.get_json().get('SOC', '')
        SOH = request.get_json().get('SOH', '')
        RUL_EOL = request.get_json().get('RUL_EOL', '')
        DOD = request.get_json().get('DOD', '')
        brand = request.get_json().get('brand', '')
        capacity = request.get_json().get('capacity', '')
        no_load_v = request.get_json().get('no_load_v', '')
        internal_resistance = request.get_json().get('internal_resistance', '')
        number_of_cycle = request.get_json().get('number_of_cycle', '')


        batteries = Battery(user_id=current_user,
                            voltage=voltage, 
                            current=current, 
                            SOC= SOC, 
                            SOH= SOH,
                            RUL_EOL = RUL_EOL, 
                            DOD=DOD,
                            brand=brand, 
                            capacity=capacity,
                            no_load_v=no_load_v,
                            internal_resistance=internal_resistance,
                            number_of_cycle=number_of_cycle,
                            )
        db.session.add(batteries)
        db.session.commit()

        return jsonify({
            'user_id': batteries.id,
            'voltage': batteries.voltage,
            'current': batteries.current,
            'SOC': batteries.SOC,
            'SOH': batteries.SOH,
            'RUL_EOL': batteries.RUL_EOL,
            'DOD': batteries.DOD,
            'brand': batteries.brand,
            'capacity':batteries.capacity,
            'no_load_v':batteries.no_load_v,
            'internal_resistance':batteries.internal_resistance,
            'number_of_cycle': batteries.number_of_cycle,
        }), HTTP_201_CREATED

    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        battery = Battery.query.filter_by(user_id=current_user).first()

        data = []


        data.append({
        'user_id': battery.id,
        'voltage': battery.voltage,
        'current': battery.current,
        'SOC': battery.SOC,
        'SOH': battery.SOH,
        'RUL_EOL': battery.RUL_EOL,
        'DOD': battery.DOD,
        'brand': battery.brand,
        'capacity':battery.capacity,
        'no_load_v':battery.no_load_v,
        'internal_resistance':battery.internal_resistance,
        'number_of_cycle': battery.number_of_cycle,
        })


        return jsonify({'data': data}), HTTP_200_OK
    
    
@batteries.get("/<int:id>")
@jwt_required()
def get_battery(id):
    current_user = get_jwt_identity()

    battery = Battery.query.filter_by(user_id=current_user, id=id).first()

    if not battery:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    return jsonify({
            'user_id': batteries.id,
            'voltage': batteries.voltage,
            'current': batteries.current,
            'SOC': batteries.SOC,
            'SOH': batteries.SOH,
            'RUL_EOL': batteries.RUL_EOL,
            'DOD': batteries.DOD,
            'brand': batteries.brand,
            'capacity':batteries.capacity,
            'no_load_v':batteries.no_load_v,
            'internal_resistance':batteries.internal_resistance,
            'number_of_cycle': batteries.number_of_cycle,

    }), HTTP_200_OK
    
    
@batteries.put('/<int:id>')
@batteries.patch('/<int:id>')
@jwt_required()
def editbattery(id):
    current_user = get_jwt_identity()

    battery = Battery.query.filter_by(user_id=current_user, id=id).first()

    if not battery:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    voltage = request.get_json().get('voltage', '')
    current = request.get_json().get('current', '')
    SOC = request.get_json().get('SOC', '')
    SOH = request.get_json().get('SOH', '')
    RUL_EOL = request.get_json().get('RUL_EOL', '')
    DOD = request.get_json().get('DOD', '')
    brand = request.get_json().get('brand', '')
    capacity = request.get_json().get('capacity', '')
    no_load_v = request.get_json().get('no_load_v', '')
    internal_resistance = request.get_json().get('internal_resistance', '')
    number_of_cycle = request.get_json().get('number_of_cycle', '')

    
    batteries.voltage = voltage
    batteries.current = current
    batteries.SOC = SOC
    batteries.SOH = SOH
    batteries.RUL_EOL = RUL_EOL
    batteries.DOD = DOD
    batteries.brand = brand
    batteries.capacity = capacity
    batteries.no_load_v = no_load_v
    batteries.internal_resistance,
    batteries.number_of_cycle,

    db.session.commit()

    return jsonify({
        'user_id': batteries.id,
        'voltage': batteries.voltage,
        'current': batteries.current,
        'SOC': batteries.SOC,
        'SOH': batteries.SOH,
        'RUL_EOL': batteries.RUL_EOL,
        'DOD': batteries.DOD,
        'brand': batteries.brand,
        'capacity':batteries.capacity,
        'no_load_v':batteries.no_load_v,
        'internal_resistance':batteries.internal_resistance,
        'number_of_cycle': batteries.number_of_cycle,
    }), HTTP_200_OK


@batteries.delete("/<int:id>")
@jwt_required()
def delete_battery(id):
    current_user = get_jwt_identity()

    battery = Battery.query.filter_by(user_id=current_user, id=id).first()


    if not battery:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(battery)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT

# @batteries.get("/stats")
# @jwt_required()
# def get_stats():
#     current_user = get_jwt_identity()

#     data = []

#     items = Battery.query.filter_by(user_id=current_user).all()

#     for item in items:
#         new_link = {
#             'visits': item.visits,
#             'url': item.url,
#             'id': item.id,
#             'short_url': item.short_url,
#         }

#         data.append(new_link)

#     return jsonify({'data': data}), HTTP_200_OK