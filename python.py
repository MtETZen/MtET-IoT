import sys
import urllib.request
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QPushButton, QLineEdit, QFrame, QLabel, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class AnimeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anime Style Calculator")
        self.setFixedSize(400, 650)
        self.setup_ui()

    def setup_ui(self):
        # 1. ตั้งค่าภาพพื้นหลัง
        self.bg_label = QLabel(self)
        self.bg_label.resize(self.width(), self.height())
        self.bg_label.setScaledContents(True)
        self.load_background_image('https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=800&auto=format&fit=crop')

        # เลย์เอาต์หลัก จัดให้อยู่ตรงกลาง
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # 2. สร้างกล่องเครื่องคิดเลข (Glassmorphism Effect)
        self.calc_container = QFrame()
        self.calc_container.setObjectName("CalcContainer")
        self.calc_container.setFixedSize(340, 480)
        
        # เพิ่มเงาให้กล่องดูลอยขึ้นมา
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 5)
        self.calc_container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(self.calc_container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)

        # 3. หน้าจอแสดงผล
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(70)
        font = QFont("Arial", 24, QFont.Bold)
        self.display.setFont(font)
        container_layout.addWidget(self.display)

        # 4. ปุ่มกด
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        buttons = [
            ('AC', 'Clear'), ('DEL', 'Clear'), ('%', 'Operator'), ('÷', 'Operator'),
            ('7', 'Num'), ('8', 'Num'), ('9', 'Num'), ('×', 'Operator'),
            ('4', 'Num'), ('5', 'Num'), ('6', 'Num'), ('-', 'Operator'),
            ('1', 'Num'), ('2', 'Num'), ('3', 'Num'), ('+', 'Operator'),
            ('0', 'Num'), ('.', 'Num'), ('=', 'Equal')
        ]

        row, col = 0, 0
        for text, btn_type in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(60)
            btn.setFont(QFont("Arial", 16, QFont.Bold))
            btn.setObjectName(btn_type) # กำหนดชื่อ Object สำหรับโยงกับ CSS
            btn.clicked.connect(self.on_button_clicked)
            
            if text == '=':
                # ปุ่มเท่ากับกินพื้นที่ 2 คอลัมน์
                grid_layout.addWidget(btn, row, col, 1, 2)
                col += 1
            else:
                grid_layout.addWidget(btn, row, col)

            col += 1
            if col > 3:
                col = 0
                row += 1

        container_layout.addLayout(grid_layout)
        main_layout.addWidget(self.calc_container)

        # 5. ตกแต่งด้วย QSS (Qt Style Sheets คล้าย CSS ในเว็บ)
        self.setStyleSheet("""
            QFrame#CalcContainer {
                background-color: rgba(255, 255, 255, 100);
                border-radius: 20px;
                border: 2px solid rgba(255, 255, 255, 180);
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 12px;
                color: #4a4a4a;
                padding: 10px;
                border: 1px solid rgba(255, 255, 255, 200);
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 160);
                border-radius: 12px;
                color: #555;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 230);
                color: #ff758c;
            }
            QPushButton:pressed {
                background-color: rgba(200, 200, 200, 200);
            }
            QPushButton#Operator {
                background-color: rgba(255, 182, 193, 200);
                color: white;
            }
            QPushButton#Operator:hover {
                background-color: rgba(255, 150, 168, 255);
            }
            QPushButton#Clear {
                background-color: rgba(173, 216, 230, 200);
                color: white;
            }
            QPushButton#Clear:hover {
                background-color: rgba(135, 206, 235, 255);
            }
            QPushButton#Equal {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff758c, stop:1 #ff7eb3);
                color: white;
            }
            QPushButton#Equal:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff7eb3, stop:1 #ff758c);
            }
        """)

    def load_background_image(self, url):
        try:
            data = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.bg_label.setPixmap(pixmap)
        except Exception as e:
            print("โหลดภาพพื้นหลังไม่สำเร็จ:", e)
            self.bg_label.setStyleSheet("background-color: #fce4ec;") # สีชมพูอ่อนหากโหลดภาพไม่ได้

    def on_button_clicked(self):
        btn = self.sender()
        text = btn.text()
        current_text = self.display.text()

        if text == 'AC':
            self.display.setText("0")
        elif text == 'DEL':
            if len(current_text) == 1 or current_text == "Error":
                self.display.setText("0")
            else:
                self.display.setText(current_text[:-1])
        elif text == '=':
            try:
                # แปลงเครื่องหมายให้ python เข้าใจ
                expr = current_text.replace('×', '*').replace('÷', '/')
                result = eval(expr)
                
                # จัดการทศนิยมให้ดูสวยงาม
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                elif isinstance(result, float):
                    result = round(result, 5)
                    
                self.display.setText(str(result))
            except Exception:
                self.display.setText("Error")
        else:
            if current_text == "0" and text not in ['.', '%', '÷', '×', '-', '+']:
                self.display.setText(text)
            else:
                self.display.setText(current_text + text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = AnimeCalculator()
    calc.show()
    sys.exit(app.exec_())