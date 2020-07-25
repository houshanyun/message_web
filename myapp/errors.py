
from flask import render_template
from myapp import app

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
