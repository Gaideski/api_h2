from flask import Blueprint, render_template

cake = Blueprint('cake', __name__,template_folder='templates')


@cake.route("/cake")
def index():
    return render_template('cake/cake.html')
