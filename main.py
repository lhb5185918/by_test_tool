import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import requests
from config import ENVIRONMENTS
from main_window import MainWindow  # 导入新窗口类
import time  # 添加到文件顶部的导入语句中


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_host = None
        self.company_info = {}  # 存储公司信息
        self.warehouse_info = {}  # 存储仓库信息
        self.initUI()

    def generate_receipt(self):
        """生成小票的方法"""
        pass  # 这里可以根据需要实现具体的小票生成逻辑
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('百洋一体化测试工具')
        self.resize(500, 600)  # 扩大窗口尺寸

        # 设置窗口背景色
        self.setStyleSheet('background-color: #f5f5f5;')

        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)  # 增加间距
        main_layout.setContentsMargins(50, 40, 50, 40)  # 设置边距

        # 创建标题标签
        title_label = QLabel('用户登录')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Microsoft YaHei', 32, QFont.Bold))  # 增大字体到32
        title_label.setStyleSheet('''
            color: #333333; 
            margin: 30px 0;
            letter-spacing: 5px;  /* 增加字间距 */
            font-family: "Microsoft YaHei";
        ''')
        main_layout.addWidget(title_label)

        # 统一的输入框样式
        input_style = '''
            QLineEdit, QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #4a90e2;
            }
            QLabel {
                font-size: 15px;  /* 略微增大标签字体 */
                color: #333333;
                font-family: 'Microsoft YaHei';
                font-weight: bold;  /* 加粗标签文字 */
            }
        '''
        self.setStyleSheet(input_style)

        # 在用户名输入框之前添加环境选择
        env_layout = QHBoxLayout()
        env_label = QLabel('环境:')
        self.env_combo = QComboBox()
        self.env_combo.addItems(list(ENVIRONMENTS.keys()))
        self.env_combo.currentTextChanged.connect(self.on_environment_changed)
        env_layout.addWidget(env_label)
        env_layout.addWidget(self.env_combo)
        main_layout.addLayout(env_layout)

        # 设置默认环境
        self.on_environment_changed(self.env_combo.currentText())

        # 创建用户名输入框
        username_layout = QHBoxLayout()
        username_label = QLabel('用户名:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')
        # 添加用户名输入完成事件
        self.username_input.editingFinished.connect(self.on_username_complete)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        main_layout.addLayout(username_layout)

        # 创建密码输入框
        password_layout = QHBoxLayout()
        password_label = QLabel('密码:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)

        # 创建公司选择框
        company_layout = QHBoxLayout()
        company_label = QLabel('公司:')
        self.company_combo = QComboBox()
        self.company_combo.setEnabled(False)
        # 移除原有的信号连接
        # self.company_combo.currentTextChanged.connect(self.on_company_changed)
        # 改用currentIndexChanged信号
        self.company_combo.currentIndexChanged.connect(self.on_company_index_changed)
        company_layout.addWidget(company_label)
        company_layout.addWidget(self.company_combo)
        main_layout.addLayout(company_layout)

        # 创建仓库选择框
        warehouse_layout = QHBoxLayout()
        warehouse_label = QLabel('仓库:')
        self.warehouse_combo = QComboBox()
        self.warehouse_combo.setEnabled(False)
        self.warehouse_combo.setMaxVisibleItems(10)
        self.warehouse_combo.setStyleSheet('''
            QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                padding: 0px 3px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                image: none;  /* 移除自定义图片 */
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #666;  /* 使用 CSS 三角形 */
            }
            QComboBox:disabled {
                background-color: #f5f5f5;
                color: #888888;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #dcdcdc;
                selection-background-color: #e6e6e6;
                selection-color: #000000;
                background-color: white;
            }
        ''')
        warehouse_layout.addWidget(warehouse_label)
        warehouse_layout.addWidget(self.warehouse_combo)
        main_layout.addLayout(warehouse_layout)

        # 添加一些空白间距
        main_layout.addSpacing(20)

        # 创建登录按钮
        login_button = QPushButton('登录')
        login_button.setFixedHeight(40)
        login_button.setStyleSheet('''
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Microsoft YaHei';
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2e6da4;
            }
        ''')
        login_button.clicked.connect(self.login)
        main_layout.addWidget(login_button)

        # 设置所有标签的固定宽度
        for label in [env_label, username_label, password_label, company_label, warehouse_label]:
            label.setFixedWidth(80)

        # 统一的下拉框样式
        combobox_style = '''
            QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: white;
                min-height: 25px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 8px;
            }
            QComboBox:disabled {
                background-color: #f5f5f5;
                color: #888888;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #dcdcdc;
                selection-background-color: #e6e6e6;
                selection-color: #000000;
                background-color: white;
            }
        '''

        # 应用统一样式到所有下拉框
        self.env_combo.setStyleSheet(combobox_style)
        self.company_combo.setStyleSheet(combobox_style)
        self.warehouse_combo.setStyleSheet(combobox_style)

        # 设置最大可见项数
        self.env_combo.setMaxVisibleItems(10)
        self.company_combo.setMaxVisibleItems(10)
        self.warehouse_combo.setMaxVisibleItems(10)

        # 设置布局
        self.setLayout(main_layout)

    def on_environment_changed(self, env_name):
        """当选择的环境改变时调用"""
        self.current_host = ENVIRONMENTS[env_name]['host']
        print(f"当前环境: {env_name}, Host: {self.current_host}")

    def on_username_complete(self):
        """当用户名输入完成时调用"""
        username = self.username_input.text().strip()
        if username:
            try:
                # 调用接口获取用户信息
                user_info = self.get_user_info(username)
                if user_info:
                    # 暂时断开信号连接
                    self.company_combo.blockSignals(True)

                    # 更新公司下拉框
                    self.company_combo.clear()
                    self.company_combo.addItems(user_info['companies'])
                    self.company_combo.setEnabled(True)

                    # 恢复信号连接
                    self.company_combo.blockSignals(False)

                    # 无论有几个公司，都选中第一个
                    if user_info['companies']:
                        self.company_combo.setCurrentIndex(0)
                        self.on_company_changed(self.company_combo.currentText())
                else:
                    self.show_error_message("未找到用户信息")
            except Exception as e:
                self.show_error_message(f"获取用户信息失败: {str(e)}")

    def get_user_info(self, username):
        """调用接口获取用户信息"""
        try:
            data = {
                "userNo": username,
                "platForm": "Web",
                "clientId": "iowtb"
            }
            url = f"{self.current_host}/oauth/loadCompanyList"
            response = requests.post(url, json=data)

            if response.status_code == 200:
                result = response.json()
                if result['code'] == 200 and result['obj']:
                    # 存储公司信息，用于后续获取companyCode
                    self.company_info = {
                        company['companyShortName']: company['companyCode']
                        for company in result['obj']
                    }
                    # 从返回数据中提取公司名称列表
                    companies = list(self.company_info.keys())
                    return {
                        'companies': companies,
                        'warehouses': []  # 仓库列表将在选择公司后加载
                    }
                else:
                    raise Exception(f"获取公司列表失败: {result['msg']}")
            else:
                raise Exception(f"API请求失败: {response.status_code}")

        except Exception as e:
            print(f"API调用错误: {str(e)}")
            raise

    def show_error_message(self, message):
        """显示错误消息"""
        QMessageBox.warning(self, '错误', message, QMessageBox.Ok)

    def login(self):
        """登录处理"""
        try:
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()
            company = self.company_combo.currentText()
            warehouse = self.warehouse_combo.currentText()

            if not all([username, password, company, warehouse]):
                self.show_error_message("请填写所有必填项")
                return

            # 获取公司代码和仓库ID
            company_code = self.company_info.get(company)
            warehouse_id = self.warehouse_info.get(warehouse)
            warehouse_name = self.warehouse_info.get(warehouse)

            if not company_code or not warehouse_id:
                self.show_error_message("获取公司或仓库信息失败")
                return

            # 构造登录请求数据
            login_data = {
                "userNo": username,
                "pwd": password,
                "platForm": "app",
                "companyCode": company_code,
                "whId": warehouse_id,
                "warehouseId": warehouse_id,
                "haveWarehouse": 1,
                "clientId": "iowtb",
                "userLanguage": "zh-CN"
            }

            # 发送登录请求
            login_url = f"{self.current_host}/oauth/password/unencrypted"
            response = requests.post(login_url, json=login_data)
            print("登录请求数据:", login_data)
            print("登录响应数据:", response.json())

            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    # 存储token
                    token = result.get('obj', {}).get('token')
                    username = result['obj']['user']['userName']
                    user_no = result['obj']['user']['userNo']
                    if token:
                        # 构造headers
                        headers = {
                            'Authorization': f'{token}',
                            'Content-Type': 'application/json'
                        }
                        self.show_success_message("登录成功")
                        self.open_main_window(headers, username, user_no)  # 传递headers给主窗口
                    else:
                        self.show_error_message("登录成功但未获取到token")
                else:
                    self.show_error_message(f"登录失败: {result.get('msg', '未知错误')}")
            else:
                self.show_error_message(f"登录请求失败: {response.status_code}")

        except Exception as e:
            self.show_error_message(f"登录失败: {str(e)}")

    def save_token(self, token):
        """保存token"""
        # 这里可以根据需要选择保存token的方式
        # 例如保存到文件、环境变量或全局变量
        self.token = token  # 暂时保存在实例变量中
        print(f"Token已保存: {token}")

    def open_main_window(self, headers, username, user_no):
        """打开主窗口"""
        # 获取当前选中的仓库名称和对应的仓库ID
        warehouse_name = self.warehouse_combo.currentText()
        warehouse_id = self.warehouse_info.get(warehouse_name)

        print(f"打开主窗口时的仓库ID: {warehouse_id}")  # 调试信息

        # 创建主窗口实例时传入仓库ID
        self.main_window = MainWindow(
            base_url=self.current_host,  # 传递当前环境的base_url
            headers=headers,  # 传递headers
            username=username,
            user_no=user_no,
        )

        # 设置仓库ID
        self.main_window.set_warehouse_id(warehouse_id)
        # 设置仓库名称
        self.main_window.set_warehouse_name(warehouse_name)

        # 显示主窗口
        self.main_window.show()
        self.close()  # 关闭登录窗口

    def show_success_message(self, message):
        """显示成功消息"""
        QMessageBox.information(self, '成功', message, QMessageBox.Ok)

    def on_company_changed(self, company_name):
        """当公司选择改变时调用"""
        if company_name:
            try:
                # 获取选中公司的companyCode
                company_code = self.company_info.get(company_name)
                if not company_code:
                    raise Exception("未找到公司代码")

                print(f"选择的公司: {company_name}, 公司代码: {company_code}")

                # 先启用下拉框，避免界面卡死
                self.warehouse_combo.setEnabled(True)
                self.warehouse_combo.clear()
                self.warehouse_combo.addItem("加载中...")

                # 添加0.5秒延迟
                time.sleep(0.5)

                # 调用接口获取仓库信息
                warehouses = self.get_warehouse_info(company_code)
                print(f"获取到的仓库列表: {warehouses}")

                # 更新仓库下拉框
                self.warehouse_combo.clear()

                if warehouses and len(warehouses) > 0:
                    print(f"正在添加仓库到下拉框: {warehouses}")
                    # 添加仓库选项
                    self.warehouse_combo.addItems(warehouses)
                    self.warehouse_combo.setEnabled(True)

                    # 无论有几个仓库，都选中第一个
                    self.warehouse_combo.setCurrentIndex(0)

                    print(f"仓库下拉框当前项目数: {self.warehouse_combo.count()}")

                    # 强制更新界面
                    self.warehouse_combo.update()
                else:
                    print("没有找到仓库数据")
                    self.warehouse_combo.setEnabled(False)
                    self.show_error_message("该公司没有可用的仓库")

            except Exception as e:
                print(f"处理仓库数据时出错: {str(e)}")
                self.warehouse_combo.clear()
                self.warehouse_combo.setEnabled(False)
                self.show_error_message(f"获取仓库信息失败: {str(e)}")

    def get_warehouse_info(self, company_code):
        """调用接口获取仓库信息"""
        try:
            data = {
                "userNo": self.username_input.text().strip(),
                "platForm": "Web",
                "companyCode": company_code,
                "clientId": "iowtb"
            }
            url = f"{self.current_host}/oauth/loadWarehouseList"
            response = requests.post(url, json=data)
            print("仓库接口请求数据:", data)
            print("仓库接口返回数据:", response.json())

            if response.status_code == 200:
                result = response.json()
                if result['code'] == 200 and result['obj']:
                    # 存储仓库信息，用于后续获取whId
                    self.warehouse_info = {
                        warehouse['whName']: warehouse['whId']
                        for warehouse in result['obj']
                    }
                    # 直接返回仓库名称列表
                    warehouses = list(self.warehouse_info.keys())
                    print("处理后的仓库列表:", warehouses)  # 添加调试信息
                    return warehouses
                elif result['code'] == 200 and not result['obj']:
                    print("API返回成功但没有仓库数据")
                    return []
                else:
                    raise Exception(f"获取仓库列表失败: {result.get('msg', '未知错误')}")
            else:
                raise Exception(f"API请求失败: {response.status_code}")

        except Exception as e:
            print(f"API调用错误: {str(e)}")
            raise

    def on_company_index_changed(self, index):
        """当公司选择索引改变时调用"""
        if index >= 0:  # 确保有有效选择
            company_name = self.company_combo.currentText()
            self.on_company_changed(company_name)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        login_window = LoginWindow()
        login_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        # 显示错误对话框
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("错误")
        error_dialog.setText(f"程序启动失败: {str(e)}")
        error_dialog.setDetailedText(f"详细错误信息:\n{str(e)}")
        error_dialog.exec_()
