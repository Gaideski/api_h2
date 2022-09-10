import os
from flask import Flask
from config import load_dotenv
from blueprints.main.view import main
from blueprints.movies.view import movies
from blueprints.cake.view import cake

from etl.csv_extractor import initialize_data
from repositories.persistance_insertion import insert_database_data
from repositories.persistance import close_conection
import time

def create_app():
    app = Flask(__name__)
    app.config.from_object(load_dotenv())    
    app.register_blueprint(main)
    app.register_blueprint(movies)
    app.register_blueprint(cake)
    return app

def on_exit(sig, func=None):
    print("exit handler")
    close_conection()
    time.sleep(10)

if __name__ == "__main__":
    dataframes = initialize_data()
    if dataframes is not None:
        insert_database_data(dataframes)
    create_app().run(host='0.0.0.0')