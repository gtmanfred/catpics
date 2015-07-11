import requests

from flask.views import MethodView
from flask import render_template


class Index(MethodView):
    def get(self):
        resp = requests.get('http://localhost:5000/api/random').json()
        return render_template('index.html', source=resp['image'])
