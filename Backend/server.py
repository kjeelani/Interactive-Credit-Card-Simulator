from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os, json
from firebase_admin import credentials, firestore, initialize_app
from credit_card import CreditSummarizer

app = Flask(__name__)

CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate("key.json")
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')


@app.route('/user/<userId>', methods=['POST'])
def add_user(userId):
    '''
        Creates new user for credit card simulation. Recieves JSON in the following format:
        {
            userId: <str>
            creditLimit: <number>
        }
    '''
    try:
        init_data = {
            "userId": userId, 
            "balance": 0,
            "creditLimit": request.json['creditLimit'], 
            "events": []
        }
        user_ref.document(userId).set(init_data)
        return jsonify({"success": True, "data": init_data}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/user/<userId>', methods=['GET'])
def get_user(userId):
    '''
        Takes in input of the userID
        
        Gets Credit Card data for following user in this format
        {
            userId: <str>
            creditLimit: <number>
            balance: <number>
            event: <EventType>
        }
        
        Returns a display message string to print in front end:
        "Available Credit: X, Balance: Y, Pending Transactions...Settled Transactions..."
    '''
    try:
        user = user_ref.document(userId).get()
        credit_summarizer = CreditSummarizer(user.to_dict())
        summarized_text = credit_summarizer.summarize()
        
        return jsonify({"success": True, "data": summarized_text}), 200
    except Exception as e:
        response = requests.post(f"http://127.0.0.1:8080/user/{userId}", json={"userId": userId, "creditLimit": 1000})
        credit_summarizer = CreditSummarizer(response.json()["data"])
        summarized_text = credit_summarizer.summarize()
        return jsonify({"success": True, "data": summarized_text}), 200
            

@app.route('/user/<userId>', methods=['PUT'])
def update_user(userId):
    '''
        Takes in input of the userID AND updated event as a JSON:
        {
            "event": <EventType>
        }

        Gets Credit Card data for following user in this format
        {
            userId: <str>
            creditLimit: <number>
            balance: <number>
            event: <EventType>
        }
        
        Returns a display message string to print in front end:
        "Available Credit: X, Balance: Y, Pending Transactions...Settled Transactions..."
    '''
    # print(request.json["event"])
    try:
        user = user_ref.document(userId).get()
        user_dict = user.to_dict()
        user_dict["events"].append(request.json["event"])
        # Push Updated Data to Firebase and resummarize
        user_ref.document(userId).set(user_dict)
        credit_summarizer = CreditSummarizer(user_dict)
        summarized_text = credit_summarizer.summarize()
        
        return jsonify({"success": True, "data": summarized_text}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

if __name__ == '__main__':
    app.run(debug=True, port="8080")
