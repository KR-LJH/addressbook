import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QListView, QWidget, QListWidgetItem, QMessageBox, QAction, QFileDialog, QMenu, QActionGroup, QDialog, QFormLayout
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from addBookMySQL import *

class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 파일 로드
        loadUi("./res/myWin01.ui", self)
        # DB 객체 생성
        self.db = mysqlDB()

        # 버튼 클릭 시그널에 슬롯 연결
        self.Button.clicked.connect(self.register_photo)
        self.loadButton.clicked.connect(self.load_address_book)
        self.saveButton.clicked.connect(self.save_address_book)
        self.addButton.clicked.connect(self.add_contact)

        # QStandardItemModel 생성
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)   

        # 리스트뷰의 더블 클릭 시그널에 슬롯 연결
        self.listView.doubleClicked.connect(self.show_item_info)

    def setupUi(self):
        self.setGeometry(0, 0, 387, 556)
        self.setWindowTitle("주소록")
        self.addButton.clicked.connect(self.add_contact)

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(30, 100, 231, 161)
        self.label_3.setFont(("Agency FB", 14))
        self.label_3.setText("")
        self.label_3.setPixmap(QPixmap("./res/men.jpg"))
        self.label_3.setScaledContents(True)
        self.label_3.setMargin(0)

        self.Button = QPushButton(self)
        self.Button.setGeometry(270, 210, 91, 23)
        self.Button.setText("사진등록")
        self.Button.setIcon(QIcon("add icon.png"))

        self.listView = QListView(self)
        self.listView.setGeometry(20, 290, 351, 192)

        self.label = QLabel(self)
        self.label.setGeometry(60, 20, 41, 36)
        self.label.setFont(("Agency FB", 14))
        self.label.setText("이름")

        self.numEdit = QLineEdit(self)
        self.numEdit.setGeometry(137, 60, 221, 20)

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(40, 60, 89, 21)
        self.label_2.setFont(("Agency FB", 14))
        self.label_2.setText("전화번호")

        self.nameEdit = QLineEdit(self)
        self.nameEdit.setGeometry(137, 30, 221, 20)

        self.loadButton = QPushButton(self)
        self.loadButton.setGeometry(20, 490, 172, 23)
        self.loadButton.setText("주소록 불러오기")

        self.saveButton = QPushButton(self)
        self.saveButton.setGeometry(200, 490, 171, 23)
        self.saveButton.setText("주소록 저장")

        self.addButton = QPushButton(self)
        self.addButton.setGeometry(270, 240, 91, 23)
        self.addButton.setText("추가")

    def register_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "사진 등록", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            pixmap = QPixmap(file_name)
            if not pixmap.isNull():
                self.label_3.setPixmap(pixmap.scaled(self.label_3.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            else:
                QMessageBox.critical(self, "오류", "선택한 파일은 이미지 파일이 아닙니다.")

    def load_address_book(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "주소록 불러오기", "", "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, "r") as file:
                    for line in file:
                        item = QStandardItem(line.strip())
                        self.model.appendRow(item)
                QMessageBox.information(self, "불러오기", "주소록을 성공적으로 불러왔습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"주소록을 불러오는 중 오류가 발생했습니다:\n{e}")

    def save_address_book(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "주소록 저장", "", "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, "w") as file:
                    for row in range(self.model.rowCount()):
                        item = self.model.item(row)
                        if item is not None:
                            file.write(item.text() + "\n")
                QMessageBox.information(self, "저장 완료", "주소록이 성공적으로 저장되었습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"주소록을 저장하는 중 오류가 발생했습니다:\n{e}")

    def add_contact(self):
        # 이름과 전화번호를 가져와서 리스트뷰에 추가
        name = self.nameEdit.text()
        phone_number = self.numEdit.text()
        if name and phone_number:  # 이름과 전화번호가 비어있지 않은 경우에만 추가
            item_text = f'이름: {name}, 전화번호: {phone_number}'
            item = QStandardItem(item_text)
            # 선택된 이미지의 파일 경로를 아이템 데이터로 저장
            image_path = self.label_3.pixmap().cacheKey() if self.label_3.pixmap() else None
            item.setData((phone_number, image_path), Qt.UserRole)
            self.model.appendRow(item)
            self.label_3.setPixmap(QPixmap("./res/men.jpg"))  # 먼저 label_3의 이미지를 men.jpg로 설정
            self.nameEdit.clear()
            self.numEdit.clear()
            
            #DB에 추가 하는 곳 
            # result = db.insert("홍길동fromPython","010,0987,6543")
            # print("Insert test: ", result)  
            result = self.db.insert(name, phone_number)
            print("Insert test: ", result)  
    
    def show_item_info(self, index):
        # 유효한 인덱스인지 확인
        if index.isValid():
            # 선택된 아이템 가져오기
            item = self.model.itemFromIndex(index)
            if item is not None:
                # 아이템 정보 가져오기
                item_text = item.text()
                name = item_text.split(':')[1].strip()
                number = item.data(Qt.UserRole)[0]
                image_path = item.data(Qt.UserRole)[1]

                # 이미지 경로 확인
                if image_path and isinstance(image_path, str):
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        # 아이템 정보 다이얼로그 표시
                        dialog = QDialog(self)
                        layout = QVBoxLayout(dialog)

                        # 이름과 번호를 표시하는 레이블 생성
                        name_label = QLabel(f"이름: {name}")
                        number_label = QLabel(f"전화번호: {number}")
                        layout.addWidget(name_label)
                        layout.addWidget(number_label)

                        # 이미지 표시를 위한 레이블 생성
                        image_label = QLabel()
                        # 이미지를 300x300으로 조정하여 표시
                        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
                        image_label.setPixmap(pixmap)
                        image_label.setAlignment(Qt.AlignCenter)  # 이미지를 가운데 정렬
                        layout.addWidget(image_label)

                        dialog.setWindowTitle("아이템 정보")
                        # 다이얼로그가 닫힐 때까지 종료하지 않고 실행을 계속합니다.
                        if dialog.exec_() == QDialog.Accepted:
                            pass
                    else:
                        QMessageBox.warning(self, "경고", "선택된 아이템의 이미지를 표시할 수 없습니다.")
                else:
                    QMessageBox.warning(self, "경고", "선택된 아이템의 이미지 경로가 유효하지 않습니다.")
            else:
                QMessageBox.warning(self, "경고", "선택된 아이템이 없습니다.")


    
    def contextMenuEvent(self, event):
        # 컨텍스트 메뉴 생성
        menu = QMenu(self)
        
        # 수정 액션 추가
        edit_action = QAction("수정", self)
        edit_action.triggered.connect(self.edit_contact)
        menu.addAction(edit_action)

        # 삭제 액션 추가
        delete_action = QAction("삭제", self)
        delete_action.triggered.connect(self.delete_contact)
        menu.addAction(delete_action)

        # 컨텍스트 메뉴 표시
        menu.exec_(event.globalPos())

    def edit_contact(self):
        # 선택된 아이템 가져오기
        selected_indexes = self.listView.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            item = self.model.itemFromIndex(selected_index)
            if item:
                # 대화 상자 열기
                dialog = QDialog(self)
                layout = QFormLayout(dialog)

                # 이름과 전화번호 입력 필드 추가
                name_edit = QLineEdit(self)
                name_edit.setText(item.text().split(',')[0].split(':')[1].strip())
                phone_edit = QLineEdit(self)
                phone_edit.setText(item.text().split(',')[1].split(':')[1].strip())

                layout.addRow("이름:", name_edit)
                layout.addRow("전화번호:", phone_edit)

                # 수정 확인 버튼 추가
                confirm_button = QPushButton("확인", self)
                confirm_button.clicked.connect(lambda: self.confirm_edit(dialog, item, name_edit.text(), phone_edit.text()))
                layout.addWidget(confirm_button)

                dialog.exec_()

    def confirm_edit(self, dialog, item, name, phone):
        # 아이템 수정 및 대화 상자 닫기
        new_item_text = f'이름: {name}, 전화번호: {phone}'
        item.setText(new_item_text)
        # 수정 후에는 이미지 경로를 갱신하지 않음
        dialog.accept()

    def delete_contact(self):
        # 선택된 아이템 삭제
        selected_indexes = self.listView.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            self.model.removeRow(selected_index.row())
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec_())

