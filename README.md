# Overview
This small application is meant to simulate credit card transactions. As a user, you can make transactions through the credit card, and resolve payments to your credit provider. Right now, the app isn't deployed anywhere, so you would need to run the Flask backend via localhost w/ Port 8080. A demo video can be seen [here](https://youtu.be/9Ti98LRNm-4).

# Tech Stack
For the frontend, I used Next.js + ChakraUI for easy component-building and formatting
For the backend, I used Flask w/ Firebase for an easy proof-of-concept. Given more time, I'd have integrated the API directly within Next.js

# Database Testing
If you want to test the credit card algorithm through unit testing, make your way to test_client.py, where you can easily write bulk unit tests. credit_card.py is the main algorithm powering the backend.

# Future Changes
Currently, users can utilize the tool in any manner they want to, and thus settle payments before they even initialize a payment. More form control needs to be in place
