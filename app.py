from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Print out MongoDB URI for debugging
mongodb_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
print(f"Connecting to MongoDB at {mongodb_uri}")

# Set up MongoDB client
try:
    client = MongoClient(mongodb_uri)
    db = client.flask_db
    collection = db.data
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data = request.get_json()
        try:
            collection.insert_one(data)
            return jsonify({"status": "Data inserted"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == 'GET':
        try:
            data = list(collection.find({}, {"_id": 0}))
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
