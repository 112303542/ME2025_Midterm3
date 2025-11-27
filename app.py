from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        orders = db.get_all_orders()
        if request.args.get('warning'):
            warning = request.args.get('warning')
            return render_template('form.html', orders=orders, warning=warning)
        return render_template('form.html', orders=orders)

@app.route('/product', methods=['GET', 'POST', 'DELETE'])
    def product():
        if request.method == 'GET':
          # TODO: Implement GET logic for category list and product price
        elif request.method == 'POST':
          # TODO: Implement POST logic to add new order
        elif request.method == 'DELETE':
          # TODO: Implement DELETE logic using order_id

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
