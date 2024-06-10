#파이썬으로 sql사용하기 feat mySQL
import sys
import pymysql
from PyQt5.QtWidgets import QApplication
class mysqlDB():
    def __init__(self)->None:
        pymysql.version_info = (1, 4, 2, "final", 0)
        pymysql.install_as_MySQLdb()
        super().__init__()
        self.connection = pymysql.connect(
            host = 'localhost',
            user = 'ljh',
            passwd = '1234',
            db = 'ljh',
            charset = 'utf8',
            port = 3308,
            cursorclass = pymysql.cursors.DictCursor)
    def insert(self, new_name, new_phone):        
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO addbook (name, phone) VALUES (%s, %s)"
            result = cursor.execute(sql, (new_name, new_phone))
            self.connection.commit()
            return result
    
    def update(self, name_key, new_phone):
        with self.connection.cursor() as cursor:
            sql = "UPDATE addbook SET phone = %s WHERE name = %s"
            result = cursor.execute(sql, (new_phone, name_key))
            self.connection.commit()
            return result
    
    def delete(self, name_key):                
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM addbook WHERE name = %s"
            relust = cursor.execute(sql, name_key)
            self.connection.commit()
            return result
        
    def search(self, any_key):                
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM addbook WHERE name LIKE %s OR phone LIKE %s"
            key = '%' + any_key + '%'
            cursor.execute(sql, (key, key))
            result = cursor.fetchall() # result = cursor.fetchone() 1개의 레코드
            return result
    def pause(self):
        input("다음 테스트를 진행하려면 Enter를 누르세요...")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = mysqlDB()
    # 추가 테스트
    result = db.insert("홍길동fromPython","010,0987,6543")
    print("Insert test: ", result)   
    result = db.insert("홍길동2","011-1234-6543")
    print("Insert test: ", result)   
    db.pause()

    # 수정 테스트
    result = db.update("홍길동fromPython","010-4333-1212")
    print("Update Test : ", result)
    db.pause()

    # 찾기 테스트
    result = db.search("홍")
    print("Search Test : ", result)
    db.pause()

    # 삭제 테스트
    result = db.delete("홍길동fromPython")
    print("Delete Test : ", result)

    exit(app.exec_())
