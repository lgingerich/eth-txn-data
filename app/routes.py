from flask import request, render_template
from app import app
from .query import txnQuery 

####------render default page ----####
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template(
        'index.html')

####------render transaction data ----####
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':
        eth_address = request.form.to_dict()
        eth_address = eth_address["Address"]
        txnData = txnQuery(eth_address)

        return render_template('data.html', txnData=txnData, eth_address=eth_address)