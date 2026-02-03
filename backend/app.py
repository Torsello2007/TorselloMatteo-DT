from flask import Flask, jsonify, request
from flask_cors import CORS
from DatabaseWrapper import DatabaseWrapper

app = Flask(__name__)
CORS(app)

db = DatabaseWrapper()
db.create_table()

@app.route('/deliveries', methods=['GET'])
def get_deliveries():
    consegne = db.get_all_deliveries()
    return jsonify(consegne), 200

@app.route('/deliveries', methods=['POST'])
def create_delivery():
    data = request.json
    success = db.add_delivery(data['tracking_code'], data['recipient'], data['address'], data['time_slot'], data['priority'])
    return jsonify({"message": "OK"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)