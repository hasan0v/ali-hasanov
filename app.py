from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key in production
app.config['APP_NAME'] = 'Ali Hasanov'

@app.route('/')
def home():
    return f"<h1>Welcome to {app.config['APP_NAME']}'s Portfolio</h1>"

if __name__ == '__main__':
    app.run(debug=True)
