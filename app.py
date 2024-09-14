import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__, template_folder='templates')
app.secret_key = '555'  # Set a secret key for session management

# Load JSON data
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("data.json file not found.")
    data = {}
except json.JSONDecodeError:
    print("Error decoding JSON from data.json.")
    data = {}

# Serve the HTML file
@app.route('/')
def home():
    if 'username' not in session:
        print("User not logged in, redirecting to login.")
        return redirect(url_for('login'))
    print("User logged in, displaying home page.")
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Dummy check for username and password
        if username == 'testuser' and password == 'password123':  # Replace with your actual user authentication logic
            session['username'] = username
            print(f"User {username} logged in successfully.")
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            print("Login failed.")
    return render_template('login.html', error=error)

# Endpoint to handle user input
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # Process user input based on loaded JSON data
    response_message = process_user_input(user_message)

    response = {'message': response_message}
    return jsonify(response)

def process_user_input(user_message):
    # Check for matching roles
    companies = data.get('companies', [])
    for sector in companies:
        for role in sector['roles']:
            if user_message.lower() in role['role'].lower():
                return (
                    f"Sector: {sector['name']}\n"
                    f"Role: {role['role']}\n"
                    f"Description: {role['description']}\n"
                    f"Permissions: {', '.join(role['permissions'])}"
                )

    # Fallback response if no role matched
    return "Sorry, I didn't understand that. Please ask about a specific role."

if __name__ == '__main__':
    app.run(debug=True)
