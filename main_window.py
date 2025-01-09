from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QHBoxLayout, QComboBox, QPushButton, QCheckBox,
                             QGroupBox, QGridLayout, QScrollArea, QFrame, QMessageBox,
                             QListWidget, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPainter, QPen
from common import select_sku, get_owner_list, get_sku_detail, create_in_order  # 导入商品列表查询方法


class LoadingButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.original_text = text
        self.loading = False
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rotation)

        # 设置基础样式
        self.setStyleSheet('''
            LoadingButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 6px;
                font-size: 15px;
                font-weight: bold;
                padding: 10px 20px;
                min-width: 150px;
                min-height: 40px;
            }
            LoadingButton:hover {
                background-color: #357abd;
            }
            LoadingButton:disabled {
                background-color: #cccccc;
            }
        ''')

    def start_loading(self):
        """开始加载动画"""
        self.loading = True
        self.setEnabled(False)
        self.setText("处理中...")
        self.timer.start(50)  # 每50毫秒更新一次旋转角度

    def stop_loading(self):
        """停止加载动画"""
        self.loading = False
        self.setEnabled(True)
        self.setText(self.original_text)
        self.timer.stop()
        self.update()

    def update_rotation(self):
        """更新旋转角度"""
        self.angle = (self.angle + 10) % 360
        self.update()

    def paintEvent(self, event):
        """绘制按钮和加载动画"""
        super().paintEvent(event)
        if self.loading:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # 设置画笔
            pen = QPen()
            pen.setWidth(2)
            pen.setColor(QColor('white'))
            painter.setPen(pen)

            # 计算圆的位置和大小
            size = min(self.width(), self.height()) * 0.3
            x = self.width() - size - 10
            y = (self.height() - size) / 2

            # 绘制加载动画
            painter.translate(x + size / 2, y + size / 2)
            painter.rotate(self.angle)
            for i in range(8):
                painter.rotate(45)
                painter.setOpacity(0.125 * (i + 1))
                painter.drawLine(0, size / 4, 0, size / 2)


class MainWindow(QMainWindow):
    def __init__(self, base_url=None, headers=None):
        super().__init__()
        self.base_url = base_url
        self.headers = headers
        if not self.headers:
            self.headers = {
                'Content-Type': 'application/json'
            }
        self.warehouse_id = None  # 添加仓库ID属性
        self.warehouse_name = None  # 添加仓库名称属性
        self.sku_list = []  # 存储商品列表
        self.owner_dict = {}  # 存储货主信息 {display_text: owner_code}
        self.selected_sku_details = []  # 存储商品详细信息的列表
        self.current_owner = {  # 存储当前选中的货主信息
            'origCompanyCode': '',
            'ownerCode': '',
            'ownerName': '',
            'id': ''
        }

        # 初始化UI
        self.initUI()

        # 加载数据
        self.load_owner_list()  # 先加载货主列表
        self.load_sku_list()  # 再加载商品列表

        # 添加商品列表选择变化的信号连接
        if hasattr(self, 'product_list'):
            self.product_list.itemSelectionChanged.connect(self.on_product_selected)

        # 添加货主选择变化的信号连接
        if hasattr(self, 'storage_owner_combo'):
            self.storage_owner_combo.currentIndexChanged.connect(self.on_owner_selected)
        if hasattr(self, 'outbound_owner_combo'):
            self.outbound_owner_combo.currentIndexChanged.connect(self.on_outbound_owner_selected)

        # 添加出库商品选择变化的信号连接
        if hasattr(self, 'outbound_product_combo'):
            self.outbound_product_combo.currentIndexChanged.connect(self.on_outbound_product_selected)

    def load_sku_list(self):
        """加载商品列表"""
        try:
            if not self.base_url or not self.headers:
                QMessageBox.warning(self, '警告', '缺少必要的配置信息')
                return

            # 根据追溯码复选框状态决定是否查询药品
            is_drug = 1 if hasattr(self, 'trace_checkbox') and self.trace_checkbox.isChecked() else 0

            # 调用接口获取商品列表
            result = select_sku(
                is_drug=is_drug,
                base_url=self.base_url,
                headers=self.headers
            )

            # 检查返回结果格式
            if isinstance(result, dict) and result.get('code') == 200:
                self.sku_list = result.get('obj', [])
                self.update_product_lists()
            else:
                QMessageBox.warning(self, '警告', f'获取商品列表失败：{result.get("msg", "未知错误")}')

        except Exception as e:
            QMessageBox.warning(self, '警告', f'获取商品列表失败：{str(e)}')

    def update_product_lists(self):
        """更新商品列表"""
        try:
            # 清空现有选项
            self.product_list.clear()
            self.outbound_product_combo.clear()

            # 获取当前选择的货主
            storage_owner = self.storage_owner_combo.currentText() if hasattr(self, 'storage_owner_combo') else None
            outbound_owner = self.outbound_owner_combo.currentText() if hasattr(self, 'outbound_owner_combo') else None

            # 添加商品选项
            for sku in self.sku_list:
                sku_name = sku.get('skuName', '')
                spec = sku.get('spec', '')
                sku_code = sku.get('skuCode', '')
                owner_name = sku.get('ownerName', '')
                owner_code = sku.get('ownerCode', '')
                current_owner = f"{owner_name} ({owner_code})"

                display_text = f"{sku_name} - {spec} - {sku_code}"

                # 根据货主过滤商品
                if sku_name:
                    if not storage_owner or current_owner == storage_owner:
                        self.product_list.addItem(display_text)
                    if not outbound_owner or current_owner == outbound_owner:
                        self.outbound_product_combo.addItem(display_text)

        except Exception as e:
            QMessageBox.warning(self, '警告', f'更新商品列表失败：{str(e)}')

    def get_selected_sku_info(self, combo_box):
        """获取选中商品的完整信息"""
        try:
            current_text = combo_box.currentText()
            for sku in self.sku_list:
                if sku.get('skuName') == current_text:
                    return sku
            return None
        except Exception:
            return None

    def initUI(self):
        self.setWindowTitle('白羊一体化测试工具 - 操作页面')
        self.setGeometry(100, 100, 1600, 1000)

        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # 创建水平布局来容纳入库和出库区域
        operations_layout = QHBoxLayout()
        operations_layout.setSpacing(20)

        # 创建左右两个容器
        left_container = QWidget()
        right_container = QWidget()
        left_container.setMinimumWidth(750)
        right_container.setMinimumWidth(750)

        left_layout = QVBoxLayout(left_container)
        right_layout = QVBoxLayout(right_container)
        left_layout.setContentsMargins(0, 0, 0, 0)  # 移除内边距
        right_layout.setContentsMargins(0, 0, 0, 0)  # 移除内边距

        # 创建操作区域
        self.create_storage_area(left_layout)
        self.create_outbound_area(right_layout)

        # 添加到水平布局
        operations_layout.addWidget(left_container)

        # 添加垂直分割线
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet('QFrame { color: #dcdcdc; }')
        operations_layout.addWidget(line)

        operations_layout.addWidget(right_container)

        # 将水平布局添加到主布局
        main_layout.addLayout(operations_layout)

        # 添加状态显示区域
        status_group = QGroupBox("操作状态")
        status_group.setStyleSheet('''
            QGroupBox {
                font-size: 15px;
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #ffffff, stop:1 #f8f9fa);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px 15px;
                color: #2c3e50;
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                min-width: 100px;
            }
        ''')

        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(15, 25, 15, 15)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet('''
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #4a90e2, stop:1 #357abd);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #357abd, stop:1 #2868b0);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        ''')

        # 创建一个容器widget来包含状态标签
        status_container = QWidget()
        status_container_layout = QVBoxLayout(status_container)
        status_container_layout.setContentsMargins(0, 0, 0, 0)
        status_container_layout.setSpacing(10)

        self.status_label = QLabel()
        self.status_label.setStyleSheet('''
            QLabel {
                font-size: 13px;
                color: #2c3e50;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #f8f9fa, stop:1 #ffffff);
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                min-height: 80px;
            }
        ''')
        self.status_label.setWordWrap(True)  # 允许文本自动换行

        # 创建一个半透明的阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.status_label.setGraphicsEffect(shadow)

        status_container_layout.addWidget(self.status_label)
        status_container_layout.addStretch()

        # 将容器widget设置为滚动区域的widget
        scroll_area.setWidget(status_container)

        # 设置滚动区域的固定高度
        scroll_area.setFixedHeight(250)  # 增加了高度以显示更多内容

        status_layout.addWidget(scroll_area)
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

    def create_storage_area(self, layout):
        """创建入库操作区域"""
        # 创建入库操作管理标题
        storage_title = QLabel("入库操作管理")
        storage_title.setStyleSheet('''
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #333;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dcdcdc;
            }
        ''')
        storage_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(storage_title)

        # 创建主要内容区域
        content_widget = QWidget()
        content_layout = QGridLayout()
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_widget.setLayout(content_layout)

        # 入库订单类型
        order_type_label = QLabel("入库订单类型:")
        order_type_label.setStyleSheet('font-size: 15px; font-weight: bold;')
        self.storage_type_combo = QComboBox()
        self.storage_type_combo.setStyleSheet('''
            QComboBox {
                padding: 8px;
                font-size: 14px;
                min-width: 300px;
                min-height: 35px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
            }
        ''')

        # 写死入库订单类型
        self.inbound_types = [
            {"key": "采购订单", "value": "CGDD"},
            {"key": "赠品采购订单", "value": "ZPCGDD"},
            {"key": "退仓申请单", "value": "TCSQD"},
            {"key": "退仓申请单(直配)", "value": "TCSQDZP"},
            {"key": "网店退款退货单", "value": "WDTKSQD"},
            {"key": "批发销售退货单", "value": "PFXSTHD"},
            {"key": "采购订单(直配)", "value": "CGDDZP"},
            {"key": "移仓入库单", "value": "YCRKD"},
            {"key": "调拨入库单", "value": "DBRKD"},
            {"key": "调拨退仓单", "value": "DBTCD"},
            {"key": "领样退货单", "value": "LYTHD"}
        ]

        # 添加订单类型到下拉框
        for type_info in self.inbound_types:
            self.storage_type_combo.addItem(type_info["key"])

        content_layout.addWidget(order_type_label, 0, 0)
        content_layout.addWidget(self.storage_type_combo, 0, 1, 1, 2)

        # 货主选择区域
        owner_label = QLabel("选择货主:")
        owner_label.setStyleSheet('font-size: 15px; font-weight: bold;')
        self.storage_owner_combo = QComboBox()
        self.storage_owner_combo.setStyleSheet('''
            QComboBox {
                padding: 8px;
                font-size: 14px;
                min-width: 300px;
                min-height: 35px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
            }
        ''')

        refresh_owner_button = QPushButton("获取货主")
        refresh_owner_button.setStyleSheet('''
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                min-height: 35px;
            }
        ''')
        refresh_owner_button.clicked.connect(self.load_owner_list)

        content_layout.addWidget(owner_label, 1, 0)
        content_layout.addWidget(self.storage_owner_combo, 1, 1)
        content_layout.addWidget(refresh_owner_button, 1, 2)

        # 复选框区域
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(20)

        self.trace_checkbox = QCheckBox("是否需要采集追溯码")
        self.whole_piece_checkbox = QCheckBox("是否整件")
        self.mixed_checkbox = QCheckBox("整零混合")

        checkbox_style = '''
            QCheckBox {
                font-size: 15px;
                padding: 8px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        '''
        self.trace_checkbox.setStyleSheet(checkbox_style)
        self.whole_piece_checkbox.setStyleSheet(checkbox_style)
        self.mixed_checkbox.setStyleSheet(checkbox_style)

        checkbox_layout.addWidget(self.trace_checkbox)
        checkbox_layout.addWidget(self.whole_piece_checkbox)
        checkbox_layout.addWidget(self.mixed_checkbox)
        checkbox_layout.addStretch()

        checkbox_widget.setLayout(checkbox_layout)
        content_layout.addWidget(checkbox_widget, 2, 0, 1, 3)

        # 商品选择区域
        product_label = QLabel("选择商品:")
        product_label.setStyleSheet('font-size: 15px; font-weight: bold;')

        self.product_list = QListWidget()
        self.product_list.setStyleSheet('''
            QListWidget {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 5px;
                min-height: 200px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e6f3ff;
                color: #000;
            }
        ''')
        self.product_list.setSelectionMode(QListWidget.MultiSelection)

        refresh_button = QPushButton("获取商品")
        refresh_button.setStyleSheet('''
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                min-height: 35px;
            }
        ''')
        refresh_button.clicked.connect(self.load_sku_list)

        content_layout.addWidget(product_label, 3, 0)
        content_layout.addWidget(self.product_list, 4, 0, 1, 2)
        content_layout.addWidget(refresh_button, 4, 2)

        # 按钮区域
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # 创建自定义按钮
        self.receipt_button = LoadingButton("生成验收单")
        self.shelf_button = LoadingButton("生成上架单")
        self.quick_storage_button = LoadingButton("一键入库")

        # 连接按钮点击事件
        self.receipt_button.clicked.connect(self.generate_receipt)
        self.shelf_button.clicked.connect(self.generate_shelf)
        self.quick_storage_button.clicked.connect(self.quick_storage)

        button_layout.addWidget(self.receipt_button)
        button_layout.addWidget(self.shelf_button)
        button_layout.addWidget(self.quick_storage_button)

        button_widget.setLayout(button_layout)
        content_layout.addWidget(button_widget, 5, 0, 1, 3)

        # 将内容区域添加到主布局
        layout.addWidget(content_widget)

    def create_outbound_area(self, layout):
        """创建出库操作区域"""
        # 创建出库操作管理标题
        outbound_title = QLabel("出库操作管理")
        outbound_title.setStyleSheet('''
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #333;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dcdcdc;
            }
        ''')
        outbound_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(outbound_title)

        # 创建主要内容区域
        content_widget = QWidget()
        content_layout = QGridLayout()
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_widget.setLayout(content_layout)

        # 出库订单类型
        outbound_type_label = QLabel("出库订单类型:")
        outbound_type_label.setStyleSheet('font-size: 15px; font-weight: bold;')
        self.outbound_type_combo = QComboBox()
        self.outbound_type_combo.setStyleSheet('''
            QComboBox {
                padding: 8px;
                font-size: 14px;
                min-width: 300px;
                min-height: 35px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
            }
        ''')
        self.outbound_type_combo.addItems([
            "销售出库",
            "调拨出库",
            "退货出库",
            "生产领料",
            "其他出库"
        ])

        content_layout.addWidget(outbound_type_label, 0, 0)
        content_layout.addWidget(self.outbound_type_combo, 0, 1, 1, 2)

        # 货主选择区域
        owner_label = QLabel("选择货主:")
        owner_label.setStyleSheet('font-size: 15px; font-weight: bold;')
        self.outbound_owner_combo = QComboBox()
        self.outbound_owner_combo.setStyleSheet('''
            QComboBox {
                padding: 8px;
                font-size: 14px;
                min-width: 300px;
                min-height: 35px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
            }
        ''')

        refresh_owner_button = QPushButton("获取货主")
        refresh_owner_button.setStyleSheet('''
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                min-height: 35px;
            }
        ''')
        refresh_owner_button.clicked.connect(self.load_owner_list)

        content_layout.addWidget(owner_label, 1, 0)
        content_layout.addWidget(self.outbound_owner_combo, 1, 1)
        content_layout.addWidget(refresh_owner_button, 1, 2)

        # 复选框区域
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(20)

        self.outbound_trace_checkbox = QCheckBox("是否需要采集追溯码")
        self.outbound_whole_piece_checkbox = QCheckBox("是否整件")
        self.outbound_mixed_checkbox = QCheckBox("整零混合")

        checkbox_style = '''
            QCheckBox {
                font-size: 15px;
                padding: 8px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        '''
        self.outbound_trace_checkbox.setStyleSheet(checkbox_style)
        self.outbound_whole_piece_checkbox.setStyleSheet(checkbox_style)
        self.outbound_mixed_checkbox.setStyleSheet(checkbox_style)

        checkbox_layout.addWidget(self.outbound_trace_checkbox)
        checkbox_layout.addWidget(self.outbound_whole_piece_checkbox)
        checkbox_layout.addWidget(self.outbound_mixed_checkbox)
        checkbox_layout.addStretch()

        checkbox_widget.setLayout(checkbox_layout)
        content_layout.addWidget(checkbox_widget, 2, 0, 1, 3)

        # 商品选择区域
        product_label = QLabel("选择出库商品:")
        product_label.setStyleSheet('font-size: 15px; font-weight: bold;')

        self.outbound_product_combo = QComboBox()
        self.outbound_product_combo.setStyleSheet('''
            QComboBox {
                padding: 8px;
                font-size: 14px;
                min-width: 300px;
                min-height: 35px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
            }
        ''')

        refresh_button = QPushButton("获取商品")
        refresh_button.setStyleSheet('''
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                min-height: 35px;
            }
        ''')
        refresh_button.clicked.connect(self.load_sku_list)

        content_layout.addWidget(product_label, 3, 0)
        content_layout.addWidget(self.outbound_product_combo, 3, 1)
        content_layout.addWidget(refresh_button, 3, 2)

        # 按钮区域
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        buttons = [
            ("生成出库单", self.generate_outbound_order),
            ("一键出库", self.quick_outbound)
        ]

        button_style = '''
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 6px;
                font-size: 15px;
                font-weight: bold;
                padding: 10px 20px;
                min-width: 150px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        '''

        for text, slot in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(slot)
            button_layout.addWidget(btn)

        button_widget.setLayout(button_layout)
        content_layout.addWidget(button_widget, 4, 0, 1, 3)

        # 将内容区域添加到主布局
        layout.addWidget(content_widget)

    def generate_receipt(self):
        """生成验收单"""
        try:
            self.receipt_button.start_loading()

            # 检查是否选择了商品
            if not self.selected_sku_details:
                QMessageBox.warning(self, "警告", "请先选择商品")
                return

            # 检查是否选择了货主
            if not self.current_owner['ownerCode']:
                QMessageBox.warning(self, "警告", "请先选择货主")
                return

            # 获取选中的入库单类型值
            selected_type_value = self.get_selected_storage_type_value()
            if not selected_type_value:
                QMessageBox.warning(self, "警告", "请选择入库单类型")
                return

            # 获取当前选中的货主名称
            current_text = self.storage_owner_combo.currentText()
            owner_info = self.owner_dict.get(current_text)
            owner_name = owner_info.get('ownerName') if owner_info else None  # 获取货主名称

            # 检查仓库信息
            if not self.warehouse_id or not owner_name:  # 修改这里,使用货主名称
                QMessageBox.warning(self, "警告", "缺少仓库信息或货主名称，请确保已正确登录并选择货主")
                return

            # 调用创建入库单接口
            result = create_in_order(
                base_url=self.base_url,
                headers=self.headers,
                order_type=selected_type_value,
                owner_info=self.current_owner,
                sku_details=self.selected_sku_details,
                is_whole_piece=1 if self.whole_piece_checkbox.isChecked() else 0,
                is_mixed=1 if self.mixed_checkbox.isChecked() else 0,
                warehouse_id=self.warehouse_id,
                warehouse_name=owner_name  # 修改这里,传入货主名称而不是仓库名称
            )

            # 处理返回结果
            if isinstance(result, dict):
                if result['result'].get('code') == 200:
                    QMessageBox.information(self, "成功", f"验收单创建成功\n单号: {result['result'].get('obj', '')}")
                else:
                    QMessageBox.warning(self, "错误", f"创建验收单失败: {result['result'].get('msg', '未知错误')}")
            else:
                QMessageBox.warning(self, "错误", "创建验收单失败: 返回数据格式错误")

        except Exception as e:
            print(f"生成验收单异常: {str(e)}")
            QMessageBox.warning(self, "错误", f"创建验收单时发生异常: {str(e)}")
        finally:
            self.receipt_button.stop_loading()

    def generate_shelf(self):
        """生成上架单"""
        try:
            self.shelf_button.start_loading()
            # ... 处理逻辑 ...
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成上架单时发生异常: {str(e)}")
        finally:
            self.shelf_button.stop_loading()

    def quick_storage(self):
        """一键入库"""
        try:
            self.quick_storage_button.start_loading()
            # ... 处理逻辑 ...
        except Exception as e:
            QMessageBox.warning(self, "错误", f"一键入库时发生异常: {str(e)}")
        finally:
            self.quick_storage_button.stop_loading()

    def generate_outbound_order(self):
        """生成出库单"""
        selected_product = self.outbound_product_combo.currentText()
        selected_type = self.outbound_type_combo.currentText()
        need_trace = 1 if self.outbound_trace_checkbox.isChecked() else 0
        is_whole_piece = 1 if self.outbound_whole_piece_checkbox.isChecked() else 0
        is_mixed = 1 if self.outbound_mixed_checkbox.isChecked() else 0
        self.status_label.setText(
            f"正在生成出库单...\n"
            f"订单类型: {selected_type}\n"
            f"商品: {selected_product}\n"
            f"需要追溯码: {need_trace}\n"
            f"是否整件: {is_whole_piece}\n"
            f"整零混合: {is_mixed}"
        )
        # TODO: 实现出库单生成逻辑

    def quick_outbound(self):
        """一键出库"""
        selected_product = self.outbound_product_combo.currentText()
        selected_type = self.outbound_type_combo.currentText()
        need_trace = 1 if self.outbound_trace_checkbox.isChecked() else 0
        is_whole_piece = 1 if self.outbound_whole_piece_checkbox.isChecked() else 0
        is_mixed = 1 if self.outbound_mixed_checkbox.isChecked() else 0
        self.status_label.setText(
            f"正在执行一键出库...\n"
            f"订单类型: {selected_type}\n"
            f"商品: {selected_product}\n"
            f"需要追溯码: {need_trace}\n"
            f"是否整件: {is_whole_piece}\n"
            f"整零混合: {is_mixed}"
        )
        # TODO: 实现一键出库逻辑 

    def load_owner_list(self):
        """加载货主列表"""
        try:
            if not self.base_url or not self.headers:
                QMessageBox.warning(self, '警告', '缺少必要的配置信息')
                return

            result = get_owner_list(self.base_url, self.headers)
            if isinstance(result, dict) and result.get('code') == 200:
                owners = result.get('obj', [])
                self.owner_dict.clear()

                # 更新货主下拉框
                self.storage_owner_combo.clear()
                self.outbound_owner_combo.clear()

                for owner in owners:
                    owner_name = owner.get('ownerName', '')
                    owner_code = owner.get('ownerCode', '')
                    if owner_name and owner_code:
                        display_text = f"{owner_name} ({owner_code})"
                        # 存储完整的货主信息
                        self.owner_dict[display_text] = owner
                        self.storage_owner_combo.addItem(display_text)
                        self.outbound_owner_combo.addItem(display_text)

            else:
                QMessageBox.warning(self, '警告', f'获取货主列表失败：{result.get("msg", "未知错误")}')

        except Exception as e:
            QMessageBox.warning(self, '警告', f'获取货主列表失败：{str(e)}')

    def get_selected_owner_code(self, combo_box):
        """获取选中货主的编码"""
        current_text = combo_box.currentText()
        owner_info = self.owner_dict.get(current_text)
        return owner_info.get('ownerCode') if owner_info else None

    def get_selected_owner_info(self, combo_box):
        """获取选中货主的完整信息"""
        current_text = combo_box.currentText()
        return self.owner_dict.get(current_text)

    def get_selected_storage_type_value(self):
        """获取选中的入库订单类型的value值"""
        current_text = self.storage_type_combo.currentText()
        for type_info in self.inbound_types:
            if type_info["key"] == current_text:
                return type_info["value"]
        return None

    def on_product_selected(self):
        """处理商品选择变化"""
        try:
            # 获取所有选中的商品
            selected_items = self.product_list.selectedItems()
            if not selected_items:
                return

            # 检查是否允许多选
            if not self.mixed_checkbox.isChecked() and len(selected_items) > 1:
                QMessageBox.warning(self, "警告", "未勾选整零混合时只能选择一个商品")
                self.product_list.itemSelectionChanged.disconnect(self.on_product_selected)
                self.product_list.clearSelection()
                self.product_list.item(0).setSelected(True)
                self.product_list.itemSelectionChanged.connect(self.on_product_selected)
                selected_items = [self.product_list.item(0)]

            # 收集所有选中商品的编码
            sku_codes = []
            for item in selected_items:
                try:
                    current_text = item.text()
                    # 从当前文本中提取商品编码
                    sku_code = current_text.split(' - ')[-1]
                    sku_codes.append(sku_code)
                except Exception as e:
                    print(f"处理商品 {current_text} 时出错: {str(e)}")
                    continue

            if not sku_codes:
                return

            # 调用 get_sku_detail 获取商品详细信息
            sku_details = get_sku_detail(self.base_url, self.headers, sku_codes)

            # 处理返回结果
            if isinstance(sku_details, list):
                # 多个商品的情况
                self.selected_sku_details = sku_details
                status_text = "已选择商品:\n"
                for i, sku in enumerate(sku_details, 1):
                    status_text += f"\n商品 {i}:\n"
                    status_text += (
                        f"商品名称: {sku.get('skuName')}\n"
                        f"商品编码: {sku.get('skuCode')}\n"
                        f"规格: {sku.get('spec')}\n"
                        f"单位: {sku.get('mainUnit')}\n"
                        f"生产厂家: {sku.get('mfg')}\n"
                        f"批准文号: {sku.get('approvalNumber')}\n"
                        f"是否批次管理: {'是' if sku.get('isBatchManage') else '否'}\n"
                        f"是否效期管理: {'是' if sku.get('isValidity') else '否'}\n"
                    )
            elif isinstance(sku_details, dict):
                # 单个商品的情况
                if "error" in sku_details:
                    QMessageBox.warning(self, "错误", sku_details["error"])
                    return
                self.selected_sku_details = [sku_details]
                status_text = (
                    f"已选择商品:\n"
                    f"商品名称: {sku_details.get('skuName')}\n"
                    f"商品编码: {sku_details.get('skuCode')}\n"
                    f"规格: {sku_details.get('spec')}\n"
                    f"单位: {sku_details.get('mainUnit')}\n"
                    f"生产厂家: {sku_details.get('mfg')}\n"
                    f"批准文号: {sku_details.get('approvalNumber')}\n"
                    f"是否批次管理: {'是' if sku_details.get('isBatchManage') else '否'}\n"
                    f"是否效期管理: {'是' if sku_details.get('isValidity') else '否'}\n"
                )
            else:
                QMessageBox.warning(self, "错误", "获取商品详情失败")
                return

            # 更新状态显示
            self.status_label.setText(status_text)

        except Exception as e:
            QMessageBox.warning(self, "错误", f"处理商品选择时出错: {str(e)}")

    def on_outbound_product_selected(self):
        """处理出库商品选择变化"""
        try:
            current_text = self.outbound_product_combo.currentText()
            if not current_text:
                return

            # 从当前文本中提取商品编码
            sku_code = current_text.split(' - ')[-1]

            # 调用 get_sku_detail 获取商品详细信息
            sku_detail = get_sku_detail(self.base_url, self.headers, sku_code)

            if "error" in sku_detail:
                QMessageBox.warning(self, "错误", sku_detail["error"])
                return

            # 更新状态显示
            self.status_label.setText(
                f"已选择出库商品:\n"
                f"商品名称: {sku_detail.get('skuName')}\n"
                f"商品编码: {sku_detail.get('skuCode')}\n"
                f"规格: {sku_detail.get('spec')}\n"
                f"单位: {sku_detail.get('mainUnit')}\n"
                f"生产厂家: {sku_detail.get('mfg')}\n"
                f"批准文号: {sku_detail.get('approvalNumber')}\n"
                f"是否批次管理: {'是' if sku_detail.get('isBatchManage') else '否'}\n"
                f"是否效期管理: {'是' if sku_detail.get('isValidity') else '否'}"
            )

            # 存储商品详细信息
            self.selected_sku_details = [sku_detail]

        except Exception as e:
            QMessageBox.warning(self, "错误", f"获取商品详细信息失败: {str(e)}")

    def on_owner_selected(self):
        """处理入库货主选择变化"""
        try:
            current_text = self.storage_owner_combo.currentText()
            owner_info = self.owner_dict.get(current_text)
            if owner_info:
                self.current_owner = {
                    'origCompanyCode': owner_info.get('origCompanyCode', ''),
                    'ownerCode': owner_info.get('ownerCode', '')
                }
                # 更新状态显示
                self.status_label.setText(
                    f"已选择货主:\n"
                    f"货主名称: {owner_info.get('ownerName')}\n"
                    f"货主编码: {owner_info.get('ownerCode')}\n"
                    f"公司编码: {owner_info.get('origCompanyCode')}\n"
                    f"货主类型: {owner_info.get('ownerTypeStr')}"
                )

                # 重新加载商品列表
                self.load_sku_list()

        except Exception as e:
            QMessageBox.warning(self, "错误", f"选择货主失败: {str(e)}")

    def on_outbound_owner_selected(self):
        """处理出库货主选择变化"""
        try:
            current_text = self.outbound_owner_combo.currentText()
            owner_info = self.owner_dict.get(current_text)
            if owner_info:
                self.current_owner = {
                    'origCompanyCode': owner_info.get('origCompanyCode', ''),
                    'ownerCode': owner_info.get('ownerCode', '')
                }
                # 更新状态显示
                self.status_label.setText(
                    f"已选择出库货主:\n"
                    f"货主名称: {owner_info.get('ownerName')}\n"
                    f"货主编码: {owner_info.get('ownerCode')}\n"
                    f"公司编码: {owner_info.get('origCompanyCode')}\n"
                    f"货主类型: {owner_info.get('ownerTypeStr')}"
                )

                # 重新加载商品列表
                self.load_sku_list()

        except Exception as e:
            QMessageBox.warning(self, "错误", f"选择货主失败: {str(e)}")

    def set_warehouse_id(self, warehouse_id):
        """设置仓库ID"""
        print(f"设置仓库ID: {warehouse_id}")  # 添加调试信息
        self.warehouse_id = warehouse_id

    def set_warehouse_name(self, warehouse_name):
        """设置仓库名称"""
        print(f"设置仓库名称: {warehouse_name}")  # 添加调试信息
        self.warehouse_name = warehouse_name
