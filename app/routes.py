from flask import request, render_template
from app import app
from .query import txnQuery 

####------render default webpage ----####
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template(
        'index.html',
        txnData = txnQuery()
        )