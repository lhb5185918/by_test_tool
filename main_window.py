from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout, 
                           QHBoxLayout, QComboBox, QPushButton, QCheckBox,
                           QGroupBox, QGridLayout, QScrollArea, QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from common import select_sku, get_owner_list, get_sku_detail, create_in_order  # 导入商品列表查询方法

class MainWindow(QMainWindow):
    def __init__(self, base_url=None, headers=None):
        super().__init__()
        self.base_url = base_url
        self.headers = headers
        if not self.headers:
            self.headers = {
                'Content-Type': 'application/json'
            }
        self.warehouse_id = None  # 添加仓库ID属性，供其他方法使用
        self.sku_list = []  # 存储商品列表
        self.owner_dict = {}  # 存储货主信息 {display_text: owner_code}
        self.initUI()
        self.load_owner_list()  # 先加载货主列表
        self.load_sku_list()  # 再加载商品列表
        
        # 添加商品选择变化的信号连接
        self.product_combo.currentIndexChanged.connect(self.on_product_selected)
        self.outbound_product_combo.currentIndexChanged.connect(self.on_outbound_product_selected)
        
        # 存储商品详细信息的列表
        self.selected_sku_details = []
        
        # 添加货主选择变化的信号连接
        self.storage_owner_combo.currentIndexChanged.connect(self.on_owner_selected)
        self.outbound_owner_combo.currentIndexChanged.connect(self.on_outbound_owner_selected)
        
        # 存储当前选中的货主信息
        self.current_owner = {
            'origCompanyCode': '',
            'ownerCode': ''
        }

    def load_sku_list(self):
        """加载商品列表"""
        try:
            if not self.base_url or not self.headers:
                QMessageBox.warning(self, '警告', '缺少必要的配置信息')
                return
            
            # 根据追溯码复选框状态决定是否查询药品
            is_drug = 1 if hasattr(self, 'trace_checkbox') and self.trace_checkbox.isChecked() else 0
            
            # 调用接口获取商品列表
            result = select_sku(is_drug, self.base_url, self.headers)
            
            # 检查返回结果格式
            if isinstance(result, dict) and result.get('code') == 200:
                # 从 obj 字段获取商品列表
                self.sku_list = result.get('obj', [])
                # 更新入库和出库的商品下拉框
                self.update_product_combos()
            else:
                QMessageBox.warning(self, '警告', f'获取商品列表失败：{result.get("msg", "未知错误")}')
            
        except Exception as e:
            QMessageBox.warning(self, '警告', f'获取商品列表失败：{str(e)}')

    def update_product_combos(self):
        """更新商品下拉框"""
        try:
            # 清空现有选项
            self.product_combo.clear()
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
                        self.product_combo.addItem(display_text)
                    if not outbound_owner or current_owner == outbound_owner:
                        self.outbound_product_combo.addItem(display_text)
                        
            # 如果有商品，默认选择第一个
            if self.product_combo.count() > 0:
                self.product_combo.setCurrentIndex(0)
            if self.outbound_product_combo.count() > 0:
                self.outbound_product_combo.setCurrentIndex(0)
                
        except Exception as e:
            QMessageBox.warning(self, '警告', f'更新商品下拉框失败：{str(e)}')

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
        self.setGeometry(100, 100, 1600, 1000)  # 调整为更大的尺寸

        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局，增加边距
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)  # 增加外边距
        main_layout.setSpacing(25)  # 增加组件之间的间距

        # 创建水平布局来容纳入库和出库区域
        operations_layout = QHBoxLayout()
        operations_layout.setSpacing(20)  # 增加左右区域之间的间距

        # 创建左右两个容器，增加最小宽度
        left_container = QWidget()
        right_container = QWidget()
        left_container.setMinimumWidth(750)  # 增加最小宽度
        right_container.setMinimumWidth(750)
        
        left_layout = QVBoxLayout(left_container)
        right_layout = QVBoxLayout(right_container)
        left_layout.setContentsMargins(15, 15, 15, 15)  # 增加内边距
        right_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(20)  # 增加组件间距
        right_layout.setSpacing(20)

        # 设置标题样式，增加字体大小
        title_style = '''
            QLabel {
                font-size: 22px;  /* 增加字体大小 */
                font-weight: bold;
                color: #333;
                padding: 15px;    /* 增加内边距 */
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dcdcdc;
            }
        '''
        
        # 添加标题
        storage_title = QLabel("入库操作管理")
        outbound_title = QLabel("出库操作管理")
        storage_title.setStyleSheet(title_style)
        outbound_title.setStyleSheet(title_style)
        storage_title.setAlignment(Qt.AlignCenter)
        outbound_title.setAlignment(Qt.AlignCenter)
        
        left_layout.addWidget(storage_title)
        right_layout.addWidget(outbound_title)

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

        # 修改状态显示区域的样式
        status_group = QGroupBox("操作状态")
        status_group.setStyleSheet('''
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                margin-top: 10px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: #666;
            }
        ''')
        
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(15, 15, 15, 15)
        self.status_label = QLabel()
        self.status_label.setStyleSheet('''
            QLabel {
                font-size: 13px;
                color: #666;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 4px;
                min-height: 80px;
            }
        ''')
        status_layout.addWidget(self.status_label)
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

    def create_storage_area(self, layout):
        """创建入库操作区域"""
        operation_group = QGroupBox("入库操作管理")
        operation_group.setStyleSheet('''
            QGroupBox {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: #ffffff;
                margin-top: 0px;
            }
        ''')
        operation_layout = QGridLayout()
        operation_layout.setSpacing(15)
        operation_layout.setContentsMargins(20, 20, 20, 20)
        
        # 入库订单类型选择
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
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
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
        
        operation_layout.addWidget(order_type_label, 0, 0)
        operation_layout.addWidget(self.storage_type_combo, 0, 1)
        
        # 货主选择区域使用水平布局
        owner_layout = QHBoxLayout()
        
        # 货主选择标签和下拉框
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
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        ''')
        
        # 添加获取货主按钮
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
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2e6da4;
            }
        ''')
        refresh_owner_button.clicked.connect(self.load_owner_list)
        
        # 将组件添加到水平布局
        owner_layout.addWidget(owner_label)
        owner_layout.addWidget(self.storage_owner_combo)
        owner_layout.addWidget(refresh_owner_button)
        owner_layout.addStretch()  # 添加弹性空间
        
        # 将水平布局添加到主布局
        operation_layout.addLayout(owner_layout, 1, 0, 1, 3)

        # 创建一个水平布局来容纳复选框
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(20)  # 设置复选框之间的间距

        # 添加追溯码选项
        self.trace_checkbox = QCheckBox("是否需要采集追溯码")
        self.trace_checkbox.setStyleSheet('''
            QCheckBox {
                font-size: 15px;
                padding: 8px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        ''')
        # 添加状态改变信号连接
        self.trace_checkbox.stateChanged.connect(self.load_sku_list)
        checkbox_layout.addWidget(self.trace_checkbox)

        # 添加整件选项
        self.whole_piece_checkbox = QCheckBox("是否整件")
        self.whole_piece_checkbox.setStyleSheet('''
            QCheckBox {
                font-size: 15px;
                padding: 8px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        ''')
        checkbox_layout.addWidget(self.whole_piece_checkbox)

        # 添加整零混合选项
        self.mixed_checkbox = QCheckBox("整零混合")
        self.mixed_checkbox.setStyleSheet('''
            QCheckBox {
                font-size: 15px;
                padding: 8px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        ''')
        checkbox_layout.addWidget(self.mixed_checkbox)

        # 添加弹性空间，使复选框靠左对齐
        checkbox_layout.addStretch()

        # 将复选框布局添加到主布局
        operation_layout.addLayout(checkbox_layout, 2, 0, 1, 3)
        
        # 商品选择区域使用水平布局
        product_layout = QHBoxLayout()
        
        # 商品选择标签和下拉框
        product_label = QLabel("选择商品:")
        product_label.setStyleSheet('font-size: 15px; font-weight: bold;')
        self.product_combo = QComboBox()
        self.product_combo.setStyleSheet('''
            QComboBox {
                padding: 8px;
                font-size: 14px;
                min-width: 300px;
                min-height: 35px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
            }
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        ''')
        
        # 添加刷新按钮
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
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2e6da4;
            }
        ''')
        refresh_button.clicked.connect(self.load_sku_list)
        
        # 将组件添加到水平布局
        product_layout.addWidget(product_label)
        product_layout.addWidget(self.product_combo)
        product_layout.addWidget(refresh_button)
        product_layout.addStretch()  # 添加弹性空间
        
        # 将水平布局添加到主布局
        operation_layout.addLayout(product_layout, 3, 0, 1, 3)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)  # 设置按钮之间的间距

        # 添加弹性空间，使按钮均匀分布
        button_layout.addStretch()

        buttons = [
            ("生成验收单", self.generate_receipt),
            ("生成上架单", self.generate_shelf),
            ("一键入库", self.quick_storage)
        ]

        for i, (text, slot) in enumerate(buttons):
            btn = QPushButton(text)
            btn.setStyleSheet('''
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
                QPushButton:pressed {
                    background-color: #2e6da4;
                }
            ''')
            btn.clicked.connect(slot)
            button_layout.addWidget(btn)
            # 在每个按钮后添加弹性空间
            button_layout.addStretch()

        operation_layout.addLayout(button_layout, 4, 0, 1, 3)

        # 最后设置 operation_group 的布局
        operation_group.setLayout(operation_layout)
        layout.addWidget(operation_group)

    def create_outbound_area(self, layout):
        """创建出库操作区域"""
        outbound_group = QGroupBox()
        outbound_group.setStyleSheet('''
            QGroupBox {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: #ffffff;
                margin-top: 0px;
            }
        ''')
        outbound_layout = QGridLayout()
        outbound_layout.setSpacing(15)
        outbound_layout.setContentsMargins(20, 20, 20, 20)
        outbound_group.setLayout(outbound_layout)

        # 添加出库订单类型选择
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
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        ''')
        self.outbound_type_combo.addItems([
            "销售出库",
            "调拨出库",
            "退货出库",
            "生产领料",
            "其他出库"
        ])
        outbound_layout.addWidget(outbound_type_label, 0, 0)
        outbound_layout.addWidget(self.outbound_type_combo, 0, 1)

        # 货主选择区域使用水平布局
        outbound_owner_layout = QHBoxLayout()
        
        # 货主选择标签和下拉框
        outbound_owner_label = QLabel("选择货主:")
        outbound_owner_label.setStyleSheet('font-size: 15px; font-weight: bold;')
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
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        ''')
        
        # 添加获取货主按钮
        outbound_refresh_owner_button = QPushButton("获取货主")
        outbound_refresh_owner_button.setStyleSheet('''
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2e6da4;
            }
        ''')
        outbound_refresh_owner_button.clicked.connect(self.load_owner_list)
        
        # 将组件添加到水平布局
        outbound_owner_layout.addWidget(outbound_owner_label)
        outbound_owner_layout.addWidget(self.outbound_owner_combo)
        outbound_owner_layout.addWidget(outbound_refresh_owner_button)
        outbound_owner_layout.addStretch()  # 添加弹性空间
        
        # 将水平布局添加到主布局
        outbound_layout.addLayout(outbound_owner_layout, 1, 0, 1, 3)

        # 创建一个水平布局来容纳复选框
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(20)  # 设置复选框之间的间距
        
        # 添加追溯码选项
        self.outbound_trace_checkbox = QCheckBox("是否需要采集追溯码")
        self.outbound_trace_checkbox.setStyleSheet('''
            QCheckBox {
                font-size: 15px;
                padding: 8px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        ''')
        checkbox_layout.addWidget(self.outbound_trace_checkbox)
        
        # 添加整件选项
        self.outbound_whole_piece_checkbox = QCheckBox("是否整件")
        self.outbound_whole_piece_checkbox.setStyleSheet('''
            QCheckBox {
                font-size: 15px;
                padding: 8px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        ''')
        checkbox_layout.addWidget(self.outbound_whole_piece_checkbox)
        
        # 添加整零混合选项
        self.outbound_mixed_checkbox = QCheckBox("整零混合")
        self.outbound_mixed_checkbox.setStyleSheet('''
            QCheckBox {
                font-size: 15px;
                padding: 8px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        ''')
        checkbox_layout.addWidget(self.outbound_mixed_checkbox)
        
        # 添加弹性空间，使复选框靠左对齐
        checkbox_layout.addStretch()
        
        # 将复选框布局添加到主布局
        outbound_layout.addLayout(checkbox_layout, 2, 0, 1, 3)

        # 出库商品选择区域使用水平布局
        outbound_product_layout = QHBoxLayout()
        
        # 商品选择标签和下拉框
        outbound_product_label = QLabel("选择出库商品:")
        outbound_product_label.setStyleSheet('font-size: 15px; font-weight: bold;')
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
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        ''')
        
        # 添加刷新按钮
        outbound_refresh_button = QPushButton("获取商品")
        outbound_refresh_button.setStyleSheet('''
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2e6da4;
            }
        ''')
        outbound_refresh_button.clicked.connect(self.load_sku_list)
        
        # 将组件添加到水平布局
        outbound_product_layout.addWidget(outbound_product_label)
        outbound_product_layout.addWidget(self.outbound_product_combo)
        outbound_product_layout.addWidget(outbound_refresh_button)
        outbound_product_layout.addStretch()  # 添加弹性空间
        
        # 将水平布局添加到主布局
        outbound_layout.addLayout(outbound_product_layout, 3, 0, 1, 3)

        # 出库按钮区域
        outbound_button_layout = QHBoxLayout()
        outbound_button_layout.setSpacing(15)
        
        outbound_buttons = [
            ("生成出库单", self.generate_outbound_order),
            ("一键出库", self.quick_outbound)
        ]
        
        for text, slot in outbound_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet('''
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
                QPushButton:pressed {
                    background-color: #2e6da4;
                }
            ''')
            btn.clicked.connect(slot)
            outbound_button_layout.addWidget(btn)

        outbound_layout.addLayout(outbound_button_layout, 4, 0, 1, 3)

        layout.addWidget(outbound_group)

    def generate_receipt(self):
        """生成验收单"""
        try:
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
            
            # 构建入库单数据
            order_data = {
                'orderType': selected_type_value,
                'ownerInfo': self.current_owner,
                'skuDetails': self.selected_sku_details
            }
            
            # 调用创建入库单接口
            result = create_in_order(
                self.base_url,
                self.headers,
                selected_type_value,
                self.current_owner,
                self.selected_sku_details
            )
            
            # 处理返回结果
            if isinstance(result, dict):
                if result.get('code') == 200:
                    QMessageBox.information(self, "成功", f"验收单创建成功\n单号: {result.get('obj', '')}")
                    # 更新状态显示
                    self.status_label.setText(
                        f"验收单创建成功\n"
                        f"单号: {result.get('obj', '')}\n"
                        f"入库类型: {self.storage_type_combo.currentText()}\n"
                        f"商品: {self.product_combo.currentText()}"
                    )
                else:
                    QMessageBox.warning(self, "错误", f"创建验收单失败: {result.get('msg', '未知错误')}")
            else:
                QMessageBox.warning(self, "错误", "创建验收单失败: 返回数据格式错误")
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"创建验收单时发生异常: {str(e)}")

    def generate_shelf(self):
        """生成上架单"""
        selected_product = self.product_combo.currentText()
        need_trace = 1 if self.trace_checkbox.isChecked() else 0
        self.status_label.setText(f"正在生成上架单... 商品: {selected_product}, 需要追溯码: {need_trace}")
        # TODO: 实现上架单生成逻辑

    def quick_storage(self):
        """一键入库"""
        selected_product = self.product_combo.currentText()
        need_trace = 1 if self.trace_checkbox.isChecked() else 0
        self.status_label.setText(f"正在执行一键入库... 商品: {selected_product}, 需要追溯码: {need_trace}")
        # TODO: 实现一键入库逻辑

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
            current_text = self.product_combo.currentText()
            if not current_text:
                return
            
            # 从当前文本中提取商品编码（假设格式为：商品名 - 规格 - 商品编码）
            sku_code = current_text.split(' - ')[-1]
            
            # 调用 get_sku_detail 获取商品详细信息
            sku_detail = get_sku_detail(self.base_url, self.headers, sku_code)
            
            if "error" in sku_detail:
                QMessageBox.warning(self, "错误", sku_detail["error"])
                return
            
            # 更新状态显示
            self.status_label.setText(
                f"已选择商品:\n"
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
        self.warehouse_id = warehouse_id 