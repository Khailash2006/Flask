from flask import Flask
from route import auth_user,library,db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "khailash"

db.init_app(app)

app.register_blueprint(auth_user,url_prefix='/auth')
app.register_blueprint(library,url_prefix="/library")

@app.route('/')
def home():
    return "<h1> Welcome to Home</h1>"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8000)