from flask import Flask
from blueprints.b_user import user_blueprint


app = Flask(__name__)
# Tells flask what URL should trigger the function
@app.route("/")

def main():
    return "<p>This is the main route for the api. If you're reading this, then its running.<p>"

app.register_blueprint(user_blueprint)