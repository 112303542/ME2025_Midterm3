import datetime
import os
import random
import sqlite3

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)
    
    def get_connection(self):
        """輔助函式：使用 self.db_path 建立連線"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    #@staticmethod
    def generate_order_id(self) -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    def get_product_names_by_category(self,category):
        # TODO: Execute SQL to select product names by category
        # 根據 category 篩選出所有商品名稱
        sql = "SELECT product FROM commodity WHERE category = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (category,))
            return [row['product'] for row in cursor.fetchall()]

    def get_product_price(self,product):
        # TODO: Execute SQL to select price by product name
        # 根據 product 名稱查詢單價
        sql = "SELECT price FROM commodity WHERE product = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (product,))
            result = cursor.fetchone()
            return result['price'] if result else None

    def add_order(self, order_data):
        # TODO: Execute SQL to insert a new order into order_list
        order_id = self.generate_order_id()
        
        sql = """
        INSERT INTO order_list 
        (order_id, date, customer_name, product, amount, total, status, note) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            order_id,
            order_data['product_date'],
            order_data['customer_name'],
            order_data['product_name'],
            order_data['product_amount'],
            order_data['product_total'],
            order_data['product_status'],
            order_data['product_note']
        )

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()

    def get_all_orders(self):
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
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

    def delete_order(self, order_id):
        # TODO: Execute SQL to delete order by order_id
        # 根據 order_id 刪除特定訂單
        sql = "DELETE FROM order_list WHERE order_id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (order_id,))
            conn.commit()