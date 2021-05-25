import os
from flask import Flask
from database.db import db

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


with app.app_context():
    db.init_app(app)
    db.create_all()
    from resources.fanfic import fanfic_bp
    app.register_blueprint(fanfic_bp)


if __name__ == '__main__':
    app.run()