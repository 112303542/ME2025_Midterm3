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

    def get_product_names_by_category(self, category):
        # 根據 category 篩選出所有商品名稱
        sql = "SELECT product FROM commodity WHERE category = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (category,))
                # 將查詢結果 [(name1,), (name2,)] 轉為列表 [name1, name2]
                return [row['product'] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []

    def get_product_price(self, product):
        # 根據 product 名稱查詢單價
        sql = "SELECT price FROM commodity WHERE product = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (product,))
                result = cursor.fetchone()
                # 若有查到結果回傳 price，否則回傳 None
                return result['price'] if result else None
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None

    def add_order(self, order_data):
        # 將訂單資料字典 (Dictionary) 寫入 order_list 資料表
        
        # 1. 產生 ID
        order_id = self.generate_order_id()
        
        # 2. 準備 SQL (對應資料庫欄位: order_id, date, customer_name, product, amount, total, status, note)
        sql = """
        INSERT INTO order_list 
        (order_id, date, customer_name, product, amount, total, status, note) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # 3. 準備變數 (從 order_data 字典中取出對應的值)
        # 注意: 字典的 Key 必須與 app.py 傳入的一致
        values = (
            order_id,
            order_data['product_date'],      # 對應 date
            order_data['customer_name'],     # 對應 customer_name
            order_data['product_name'],      # 對應 product (注意名稱差異)
            order_data['product_amount'],    # 對應 amount
            order_data['product_total'],     # 對應 total
            order_data['product_status'],    # 對應 status
            order_data['product_note']       # 對應 note
        )

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, values)
                conn.commit() # 新增資料必須 commit
        except Exception as e:
            print(f"Error adding order: {e}")

    def get_all_orders(self):
        # 取得所有訂單，並需額外查詢該商品的 price 欄位合併回傳
        # 使用 LEFT JOIN 連接 commodity 資料表
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
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return []

    def delete_order(self, order_id):
        # 根據 order_id 刪除特定訂單
        sql = "DELETE FROM order_list WHERE order_id = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (order_id,))
                conn.commit() # 刪除資料必須 commit
        except Exception as e:
            print(f"Error deleting order: {e}")