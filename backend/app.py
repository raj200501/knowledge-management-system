from flask import Flask
from routes import init_routes
from database import init_db

app = Flask(__name__)
init_db(app)
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
