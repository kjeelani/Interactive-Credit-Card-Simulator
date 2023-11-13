from flask import Flask, request, jsonify
import requests, os, json

# Basic Testing Database for get, post, and put functionalities
USER_ID = "kj"
HEADER = "PUT"

api_url = "http://127.0.0.1:8080/user/" + USER_ID

if HEADER == "POST":
    response = requests.post(api_url, json={"userId": USER_ID, "creditLimit": 2000})
    print(response.json())
elif HEADER == "GET":
    response = requests.get(api_url)
    print(response.json())
else:
    new_event = {
        "eventType": "TXN_AUTHED",
        "eventTime": 139183982,
        "txnId": "221",
        "amount": 300
    }
    response = requests.put(api_url, json={"event": new_event})
    print(response.json())

