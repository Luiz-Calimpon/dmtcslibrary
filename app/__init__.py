from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config

db = SQLAlchemy()
scheduler = BackgroundScheduler()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app import routes, models
    
    with app.app_context():
        db.create_all()
        
    from app.utils import retrain_model
    scheduler.add_job(func=retrain_model, trigger="interval", hours=24, args=[app])
    scheduler.start()

    return app