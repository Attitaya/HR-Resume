#app.py
from flask import Flask
from flask_cors import CORS
from routes.extract_routes import extract_route
from flask import render_template

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(extract_route)

if __name__ == "__main__":
    app.run(debug=True, port=8899)