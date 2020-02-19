from flask import render_template, request
from . import home
from ..models.Hurricane import *


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html')

@home.route('/result', methods=['GET', 'POST'])
def search_result():
    """
    Render the homepage template on the /result route
    """
    lat = request.form.get('latitude')
    lon = request.form.get('longitude')
    result = find_hurricanes_hitting_location(lat, lon)
    return render_template('home/result.html', matched_hurricane=result)
