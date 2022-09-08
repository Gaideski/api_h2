from flask import Blueprint, render_template
from repositories.persistance import get_all

main = Blueprint('main', __name__, template_folder='blueprints/main')

@main.route("/")
def index():
    return get_all()