from flask import Blueprint, render_template, jsonify, flash
from App.controllers import initialize

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GaET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'}) 

@index_views.route('/home')
def home():
    flash("Logged in")
    return render_template('home.html')

@index_views.route('/navbar')
def navbar():
    return render_template('navbar.html')