from flask import render_template
from app import app
from .query import txnQuery 

@app.route('/')
def index():
    return render_template(
        'index.html',
        txnData = txnQuery(),
        )
