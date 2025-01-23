from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

class LoginWindow(QMainWindow):
    # 定义登录成功信号
    login_success = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('重新登录')
        self.setGeometry(300, 300, 300, 200)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加用户名输入框
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('用户名')
        layout.addWidget(self.username_input)
        
        # 添加密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # 添加登录按钮
        login_button = QPushButton('登录')
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        
    def handle_login(self):
        # 在这里实现登录逻辑
        # 登录成功后发出信号
        self.login_success.emit() 