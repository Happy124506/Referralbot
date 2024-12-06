from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Sample database (In reality, you would use a database like SQLite or MongoDB)
users = {}
referrals = {}
balance = {}
bonus = 0

# API for User Registration and Referral Link
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    referred_by = request.json.get('referred_by', None)
    referral_code = random.randint(1000, 9999)

    if username in users:
        return jsonify({"message": "User already exists!"})

    users[username] = {"referral_code": referral_code, "referred_by": referred_by}
    referrals[referral_code] = referrals.get(referral_code, 0)  # Initialize referral count
    balance[username] = 0  # Initial balance
    return jsonify({"message": "User registered successfully!", "referral_code": referral_code})

# API for Refer a Friend
@app.route('/refer', methods=['POST'])
def refer():
    referrer = request.json.get('referrer')
    referral_code = request.json.get('referral_code')

    if referrer not in users:
        return jsonify({"message": "Referrer not registered!"})

    if referral_code not in referrals:
        return jsonify({"message": "Invalid referral code!"})

    referrals[referral_code] += 1
    # Reward logic: bonus after every 5 successful referrals
    if referrals[referral_code] % 5 == 0:
        balance[referrer] += 500  # 500 points for 5 successful referrals
        return jsonify({"message": "Referral successful! You've earned ₹500!"})
    
    return jsonify({"message": "Referral successful!"})

# API to Check Balance
@app.route('/balance/<username>', methods=['GET'])
def check_balance(username):
    if username not in balance:
        return jsonify({"message": "User not found!"})

    return jsonify({"balance": balance[username]})

# API for Withdrawal (Bonus withdrawal logic)
@app.route('/withdraw', methods=['POST'])
def withdraw():
    username = request.json.get('username')
    amount = request.json.get('amount')

    if username not in balance:
        return jsonify({"message": "User not found!"})

    if balance[username] >= amount:
        balance[username] -= amount
        return jsonify({"message": f"₹{amount} withdrawn successfully!"})
    else:
        return jsonify({"message": "Insufficient balance!"})

if __name__ == '__main__':
    app.run(debug=True)
