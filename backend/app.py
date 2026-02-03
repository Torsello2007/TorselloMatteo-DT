from flask import Flask, jsonify, request
from flask_cors import CORS
from DatabaseWrapper import DatabaseWrapper

app = Flask(__name__)

# Abilita CORS: fondamentale per permettere ad Angular (frontend) 
# di chiamare le API Flask (backend)
CORS(app)

# Inizializza il wrapper del database
db = DatabaseWrapper()

# Crea le tabelle all'avvio se non esistono (richiesto dal punto 2)
db.create_table()

@app.route('/deliveries', methods=['GET'])
def get_deliveries():
    """Endpoint per recuperare la lista delle consegne in formato JSON"""
    try:
        deliveries = db.get_all_deliveries()
        return jsonify(deliveries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deliveries', methods=['POST'])
def create_delivery():
    """Endpoint per inserire una nuova consegna con validazione base"""
    data = request.json
    
    # Validazione base richiesta dalla traccia
    required_fields = ['tracking_code', 'recipient', 'address', 'time_slot', 'priority']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Dati mancanti o non validi"}), 400
    
    success = db.add_delivery(
        data['tracking_code'],
        data['recipient'],
        data['address'],
        data['time_slot'],
        data['priority']
    )
    
    if success:
        return jsonify({"message": "Consegna inserita con successo"}), 201
    else:
        return jsonify({"error": "Errore durante l'inserimento o tracking già esistente"}), 500

if __name__ == '__main__':
    # Avvia il server sulla porta 5000
    app.run(debug=True, host='0.0.0.0', port=5000)