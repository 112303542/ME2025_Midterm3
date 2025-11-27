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
        category = request.args.get('category')
        product_name = request.args.get('product')
        if category:
            # 若請求包含 category 參數，回傳該種類的商品列表
            rows = db.get_product_names_by_category(category)
            products = [row[0] for row in rows]
            return jsonify({"product": products})
    
        if product_name:
            # 若請求包含 product 參數，回傳該商品的價格
            price = db.get_product_price(product_name)
            return jsonify({"price": price})
        
    elif request.method == 'POST':
        # TODO: Implement POST logic to add new order
        # 接收前端 Form Data 並整理成字典
        order_data = {
            'product_date': request.form.get('product-date'),
            'customer_name': request.form.get('customer-name'),
            'product_name': request.form.get('product-name'),
            'product_amount': request.form.get('product-amount'),
            'product_total': request.form.get('product-total'),
            'product_status': request.form.get('product-status'),
            'product_note': request.form.get('product-note')
        }
        
        # 寫入資料庫
        db.add_order(order_data)
        
        # 成功後重導向至首頁，並帶上 warning 訊息
        return redirect(url_for('index', warning="Order placed successfully"))
    
    elif request.method == 'DELETE':
        # TODO: Implement DELETE logic using order_id
        order_id = request.args.get('order_id')
        if order_id:
            db.delete_order(order_id)
            return jsonify({"message": "Order deleted successfully"}), 200
        return jsonify({"message": "Error: Missing order_id"}), 400
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
