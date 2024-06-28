from flask import Flask
from iadoc.src.app import iadoc_app

app = Flask(__name__)

# Registrar os blueprints
app.register_blueprint(iadoc_app, url_prefix='/iadoc')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
