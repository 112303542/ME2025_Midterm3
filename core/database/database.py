import datetime
import os
import random

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    def get_product_names_by_category(self, cur, category):
        # TODO: Execute SQL to select product names by category
        sql = "SELECT product FROM commodity WHERE category = ?"
        cur.execute(sql, (category,))
        # fetchall 會回傳 list of tuples, 例如 [('Item1',), ('Item2',)]
        # 我們需要轉換成 ['Item1', 'Item2']
        return [row[0] for row in cur.fetchall()]

    def get_product_price(self, cur, product):
        # TODO: Execute SQL to select price by product name
        sql = "SELECT price FROM commodity WHERE product = ?"
        cur.execute(sql, (product,))
        result = cur.fetchone()
        # 如果有找到回傳價格，沒找到回傳 None
        return result[0] if result else None

    def add_order(self, cur, order_data):
        # TODO: Execute SQL to insert a new order into order_list
        order_id = self.generate_order_id()
        
        # 對應 SQL 欄位與傳入的字典 Key
        sql = """
        INSERT INTO order_list 
        (order_id, date, customer_name, product, amount, total, status, note) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # 注意: 這裡假設 order_data 的 key 與 Part 2 前端傳來的一致
        values = (
            order_id,
            order_data['product_date'],      # 對應 DB: date
            order_data['customer_name'],     # 對應 DB: customer_name
            order_data['product_name'],      # 對應 DB: product (注意名稱差異)
            order_data['product_amount'],    # 對應 DB: amount
            order_data['product_total'],     # 對應 DB: total
            order_data['product_status'],    # 對應 DB: status
            order_data['product_note']       # 對應 DB: note
        )
        
        cur.execute(sql, values)

    def get_all_orders(self, cur):
        # TODO: Execute SQL to get all order information
        sql = """
        SELECT 
            o.order_id, 
            o.date, 
            o.customer_name, 
            o.product, 
            c.price, 
            o.amount, 
            o.total, 
            o.status, 
            o.note
        FROM order_list o
        LEFT JOIN commodity c ON o.product = c.product
        ORDER BY o.date DESC
        """
        cur.execute(sql)
        return cur.fetchall()

    def delete_order(self, cur, order_id):
        # TODO: Execute SQL to delete order by order_id
        sql = "DELETE FROM order_list WHERE order_id = ?"
        cur.execute(sql, (order_id,))
