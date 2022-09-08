import os
from flask import Flask
from config import load_dotenv
from blueprints.main.view import main
from etl.data_initializer import initialize_data
from repositories.persistance_insertion import insert_database_data
def create_app():
    app = Flask(__name__)
    app.config.from_object(load_dotenv())    
    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    dataframes = initialize_data()
    if dataframes is not None:
        insert_database_data(dataframes)
    create_app().run()