from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QHBoxLayout, QComboBox, QPushButton, QCheckBox,
                             QGroupBox, QGridLayout, QScrollArea, QFrame, QMessageBox,
                             QListWidget, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPainter, QPen
from common import select_sku, get_owner_list, get_sku_detail, read_yaml, get_out_sku_details  # 导入商品列表查询方法
from create_in_order import create_in_order  # 导入创建入库单方法
from creat_asn_order import create_asn_order, make_put_shelf_data, put_shelf_down  # 导入创建asn单的方法
from create_out_order import create_out_order
import os
import sys
from PyQt5.QtWidgets import QListWidgetItem
import json  # 添加到文件顶部的导入语句中


def get_resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的路径
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


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
        self.warehouse_id = None
        self.warehouse_name = None
        self.sku_list = []
        self.owner_dict = {}
        self.selected_sku_details = []
        self.current_owner = {
            'origCompanyCode': '',
            'ownerCode': '',
            'ownerName': '',
            'id': ''
        }

        # 使用绝对路径读写配置文件
        self.config_path = get_resource_path('config.py')
        self.in_order_data_path = get_resource_path('in_order_data.yaml')
        self.qc_data_path = get_resource_path('qc_data.yaml')

        # 添加新的属性来存储选中的出库商品数据
        self.selected_outbound_sku_details = []

        # 初始化出库相关的按钮
        self.generate_outbound_button = None
        self.generate_pick_button = None
        self.quick_outbound_button = None

        # 初始化UI
        self.initUI()

        # 加载数据
        self.load_owner_list()
        self.load_sku_list()

        # 添加信号连接
        if hasattr(self, 'product_list'):
            self.product_list.itemSelectionChanged.connect(self.on_product_selected)
        if hasattr(self, 'storage_owner_combo'):
            self.storage_owner_combo.currentIndexChanged.connect(self.on_owner_selected)
        if hasattr(self, 'outbound_owner_combo'):
            self.outbound_owner_combo.currentIndexChanged.connect(self.on_outbound_owner_selected)
        if hasattr(self, 'outbound_product_combo'):
            self.outbound_product_combo.currentIndexChanged.connect(self.on_outbound_product_selected)

        # 确保按钮已经被创建
        if not self.generate_outbound_button:
            self.generate_outbound_button = LoadingButton('生成出库单')
            self.generate_outbound_button.clicked.connect(self.generate_outbound)
        if not self.generate_pick_button:
            self.generate_pick_button = LoadingButton('生成拣货单')
            self.generate_pick_button.clicked.connect(self.generate_pick)
        if not self.quick_outbound_button:
            self.quick_outbound_button = LoadingButton('一键出库')
            self.quick_outbound_button.clicked.connect(self.quick_outbound)

    def load_sku_list(self):
        """加载商品列表"""
        try:
            if not self.base_url or not self.headers:
                QMessageBox.warning(self, '警告', '缺少必要的配置信息')
                return

            print("开始加载商品列表...")  # 添加调试信息

            # 根据不同的操作区域调用不同的接口
            if hasattr(self, 'trace_checkbox'):  # 入库操作管理
                # 根据追溯码复选框状态决定是否查询药品
                is_drug = 1 if self.trace_checkbox.isChecked() else 0

                # 调用入库商品列表接口
                result = select_sku(
                    is_drug=is_drug,
                    base_url=self.base_url,
                    headers=self.headers
                )

                if isinstance(result, dict) and result.get('code') == 200:
                    self.sku_list = result.get('obj', [])
                else:
                    QMessageBox.warning(self, '警告', f'获取商品列表失败：{result.get("msg", "未知错误")}')

            else:  # 出库操作管理
                # 获取当前选择的货主信息
                current_text = self.outbound_owner_combo.currentText()
                owner_info = self.owner_dict.get(current_text)

                if owner_info:
                    print(f"正在获取货主 {owner_info.get('ownerName')} 的商品列表...")  # 添加调试信息
                    # 调用出库商品列表接口
                    result = get_out_sku_details(
                        base_url=self.base_url,
                        owner_info=owner_info,
                        headers=self.headers
                    )

                    if isinstance(result, list):
                        self.sku_list = result
                        print(f"成功获取到 {len(result)} 个商品")  # 添加调试信息
                    else:
                        print(f"获取商品列表失败: {result}")  # 添加调试信息
                        QMessageBox.warning(self, '警告', f'获取商品列表失败：{result}')
                else:
                    QMessageBox.warning(self, '警告', '请先选择货主')
                    return

            # 更新商品列表显示
            self.update_product_lists()

        except Exception as e:
            print(f"加载商品列表时发生异常: {str(e)}")
            QMessageBox.warning(self, '警告', f'获取商品列表失败：{str(e)}')

    def update_product_lists(self):
        """更新商品列表显示"""
        try:
            # 清空现有列表
            if hasattr(self, 'product_list'):
                self.product_list.clear()
            if hasattr(self, 'outbound_product_list'):
                self.outbound_product_list.clear()

            # 获取当前选择的货主
            storage_owner = None
            if hasattr(self, 'storage_owner_combo'):
                storage_owner = self.storage_owner_combo.currentText()

            # 添加商品到列表
            for sku in self.sku_list:
                if hasattr(self, 'trace_checkbox'):  # 入库操作管理
                    # 入库相关的代码保持不变
                    sku_name = sku.get('skuName', '')
                    spec = sku.get('spec', '')
                    sku_code = sku.get('skuCode', '')
                    owner_name = sku.get('ownerName', '')
                    owner_code = sku.get('ownerCode', '')
                    current_owner = f"{owner_name} ({owner_code})"
                    display_text = f"{sku_name} - {spec} - {sku_code}"

                    if not storage_owner or current_owner == storage_owner:
                        self.product_list.addItem(display_text)

                elif hasattr(self, 'outbound_product_list'):  # 出库操作管理
                    try:
                        # 创建列表项
                        item = QListWidgetItem()
                        
                        # 构建显示文本
                        display_text = (
                            f"{sku.get('skuName', '')} - "
                            f"{sku.get('spec', '')} - "
                            f"{sku.get('packageAttrName', '整件')} - "
                            f"{sku.get('skuCode', '')} (可用库存: {sku.get('usableQty', 0)})"
                        )
                        
                        # 设置显示文本
                        item.setText(display_text)
                        
                        # 直接存储完整的商品数据
                        item.setData(Qt.UserRole, sku)
                        
                        # 添加到列表
                        self.outbound_product_list.addItem(item)
                        
                    except Exception as e:
                        print(f"处理出库商品时出错: {str(e)}")
                        continue

            print(f"商品列表更新完成，共 {len(self.sku_list)} 个商品")

        except Exception as e:
            print(f"更新商品列表时发生错误: {str(e)}")
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
        self.setWindowTitle('百洋一体化测试工具 - 操作页面')
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
                background-color: #f8f9fa;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
                min-height: 100px;
                qproperty-alignment: AlignLeft | AlignTop;
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

        # 创建按钮组
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)  # 设置按钮之间的间距

        # 创建入库单按钮
        self.receipt_button = LoadingButton('生成验收单')
        self.receipt_button.clicked.connect(self.generate_receipt)

        # 创建上架单按钮
        self.putaway_button = LoadingButton('生成上架单')
        self.putaway_button.clicked.connect(self.generate_putaway)

        # 创建一键入库按钮
        self.quick_storage_button = LoadingButton('一键入库')
        self.quick_storage_button.clicked.connect(self.quick_storage)

        # 添加按钮到布局
        button_layout.addWidget(self.receipt_button)
        button_layout.addWidget(self.putaway_button)
        button_layout.addWidget(self.quick_storage_button)

        # 创建一个容器来放置按钮组
        button_container = QWidget()
        button_container.setLayout(button_layout)

        # 将按钮组添加到内容布局的下一行
        content_layout.addWidget(button_container, 5, 0, 1, 3)  # 跨越3列

        # 将内容区域添加到主布局
        layout.addWidget(content_widget)

    def create_outbound_area(self, layout):
        """创建出库操作区域"""
        # 创建出库操作管理标题
        title_label = QLabel('出库操作管理')
        title_label.setStyleSheet('''
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #333;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dcdcdc;
                margin-bottom: 10px;
            }
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 创建内容区域
        content_widget = QWidget()
        # 设置整个区域的背景色
        content_widget.setStyleSheet('''
            QWidget#outboundContent {
                background-color: #f5f5f5;  /* 设置与入库区域相同的灰色背景 */
                border-radius: 6px;
                border: 1px solid #dcdcdc;
            }
            QLabel {
                font-size: 15px;
                font-weight: bold;
                background: transparent;
            }
            QComboBox {
                padding: 8px;
                font-size: 14px;
                min-width: 300px;
                min-height: 35px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                min-height: 35px;
            }
            QCheckBox {
                font-size: 15px;
                padding: 8px;
                spacing: 10px;
                background: transparent;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QListWidget {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 5px;
                min-height: 200px;
                font-size: 14px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e6f3ff;
                color: #000;
            }
        ''')
        content_widget.setObjectName("outboundContent")  # 设置对象名，用于样式表定位

        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # 创建出库单类型选择
        type_label = QLabel('出库订单类型:')
        self.outbound_type_combo = QComboBox()
        # 添加出库订单类型选项
        self.outbound_types = [
            {"key": "网店发货单", "value": "FHD"},
            {"key": "采购退货通知单", "value": "CGTH"},
            {"key": "采购退货通知单(直配)", "value": "CGTHZP"},
            {"key": "赠品出库单", "value": "CGZPTH"},
            {"key": "配送单", "value": "PSD"},
            {"key": "配送单(直配)", "value": "PSDZP"},
            {"key": "批发销售单", "value": "PFXSD"},
            {"key": "移仓出库单", "value": "YCCKD"},
            {"key": "调拨出库单", "value": "DBCKD"},
            {"key": "领样出库单", "value": "LYCKD"}
        ]
        self.outbound_type_combo.addItems([t["key"] for t in self.outbound_types])
        content_layout.addWidget(type_label, 0, 0)
        content_layout.addWidget(self.outbound_type_combo, 0, 1, 1, 2)

        # 创建货主选择
        owner_label = QLabel('选择货主:')
        self.outbound_owner_combo = QComboBox()
        get_owner_button = QPushButton('获取货主')
        get_owner_button.clicked.connect(self.load_owner_list)
        content_layout.addWidget(owner_label, 1, 0)
        content_layout.addWidget(self.outbound_owner_combo, 1, 1)
        content_layout.addWidget(get_owner_button, 1, 2)

        # 创建复选框组
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.setSpacing(20)

        self.outbound_trace_checkbox = QCheckBox('是否需要采集追溯码')
        self.outbound_seed_checkbox = QCheckBox('是否播种')

        checkbox_layout.addWidget(self.outbound_trace_checkbox)
        checkbox_layout.addWidget(self.outbound_seed_checkbox)
        checkbox_layout.addStretch()

        content_layout.addWidget(checkbox_widget, 2, 0, 1, 3)

        # 创建商品选择
        product_label = QLabel('选择出库商品:')
        self.outbound_product_list = QListWidget()
        self.outbound_product_list.setSelectionMode(QListWidget.MultiSelection)

        refresh_button = QPushButton('获取商品')
        refresh_button.clicked.connect(self.load_sku_list)

        content_layout.addWidget(product_label, 3, 0)
        content_layout.addWidget(self.outbound_product_list, 4, 0, 1, 2)
        content_layout.addWidget(refresh_button, 4, 2, Qt.AlignTop)

        # 创建按钮组
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(15)

        # 初始化出库相关按钮 - 使用 LoadingButton 而不是普通的 QPushButton
        self.generate_outbound_button = LoadingButton('生成出库单')
        self.generate_pick_button = LoadingButton('生成拣货单')
        self.quick_outbound_button = LoadingButton('一键出库')

        # 添加按钮点击事件
        self.generate_outbound_button.clicked.connect(self.generate_outbound)
        self.generate_pick_button.clicked.connect(self.generate_pick)
        self.quick_outbound_button.clicked.connect(self.quick_outbound)

        # 添加按钮到布局
        button_layout.addWidget(self.generate_outbound_button)
        button_layout.addWidget(self.generate_pick_button)
        button_layout.addWidget(self.quick_outbound_button)

        # 创建一个容器来放置按钮组
        button_container = QWidget()
        button_container.setLayout(button_layout)

        # 将按钮组添加到内容布局的下一行
        content_layout.addWidget(button_container, 5, 0, 1, 3)  # 跨越3列

        # 将内容区域添加到主布局
        layout.addWidget(content_widget)
        layout.addStretch()

        # 添加商品列表选择变化的信号连接
        self.outbound_product_list.itemSelectionChanged.connect(self.on_outbound_product_selected)

    def generate_receipt(self):
        """生成验收单"""
        try:
            self.receipt_button.start_loading()
            print("开始生成验收单...")  # 调试信息

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
            owner_name = owner_info.get('ownerName') if owner_info else None

            # 检查仓库信息
            if not self.warehouse_id or not owner_name:
                QMessageBox.warning(self, "警告", "缺少仓库信息或货主名称，请确保已正确登录并选择货主")
                return

            # 1. 先调用创建入库单接口
            print("调用创建入库单接口...")  # 调试信息
            in_order_result = create_in_order(
                base_url=self.base_url,
                headers=self.headers,
                order_type=selected_type_value,
                owner_info=self.current_owner,
                sku_details=self.selected_sku_details,
                is_whole_piece=1 if self.whole_piece_checkbox.isChecked() else 0,
                is_mixed=1 if self.mixed_checkbox.isChecked() else 0,
                warehouse_id=self.warehouse_id,
                warehouse_name=owner_name
            )

            # 检查入库单创建结果
            if not isinstance(in_order_result, dict) or in_order_result['result'].get('code') != 200:
                error_msg = in_order_result['result'].get('msg', '未知错误') if isinstance(in_order_result, dict) else '创建入库单失败'
                QMessageBox.warning(self, "错误", f"创建入库单失败: {error_msg}")
                return

            # 2. 调用创建验收单接口
            print("调用创建验收单接口...")  # 调试信息
            asn_result = create_asn_order(
                base_url=self.base_url,
                headers=self.headers,
                owner_info=self.current_owner
            )

            # 处理验收单创建结果
            if isinstance(asn_result, dict):
                # 读取质检单号
                qc_data = read_yaml('qc_data.yaml')
                qc_no = qc_data.get('qcNo', '') if qc_data else ''

                success_message = (
                    f"验收单创建成功\n"
                    f"入库单号: {in_order_result['order_no']}\n"
                    f"验收单号: {qc_no}"  # 使用质检单号作为验收单号
                )
                QMessageBox.information(self, "成功", success_message)
            else:
                QMessageBox.warning(self, "错误", "创建验收单失败")

        except Exception as e:
            print(f"生成验收单异常: {str(e)}")
            QMessageBox.warning(self, "错误", f"生成验收单时发生异常: {str(e)}")
        finally:
            self.receipt_button.stop_loading()

    def generate_shelf(self):
        """生成上架单"""
        try:
            self.putaway_button.start_loading()
            # ... 处理逻辑 ...
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成上架单时发生异常: {str(e)}")
        finally:
            self.putaway_button.stop_loading()

    def quick_storage(self):
        """一键入库"""
        try:
            self.quick_storage_button.start_loading()
            print("开始一键入库流程...")  # 调试信息

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
            owner_name = owner_info.get('ownerName') if owner_info else None

            # 检查仓库信息
            if not self.warehouse_id or not owner_name:
                QMessageBox.warning(self, "警告", "缺少仓库信息或货主名称，请确保已正确登录并选择货主")
                return

            # 1. 创建入库单
            print("1. 创建入库单...")  # 调试信息
            in_order_result = create_in_order(
                base_url=self.base_url,
                headers=self.headers,
                order_type=selected_type_value,
                owner_info=self.current_owner,
                sku_details=self.selected_sku_details,
                is_whole_piece=1 if self.whole_piece_checkbox.isChecked() else 0,
                is_mixed=1 if self.mixed_checkbox.isChecked() else 0,
                warehouse_id=self.warehouse_id,
                warehouse_name=owner_name
            )

            # 检查入库单创建结果
            if not isinstance(in_order_result, dict) or in_order_result['result'].get('code') != 200:
                error_msg = in_order_result['result'].get('msg', '未知错误') if isinstance(in_order_result, dict) else '创建入库单失败'
                QMessageBox.warning(self, "错误", f"创建入库单失败: {error_msg}")
                return

            # 2. 创建验收单
            print("2. 创建验收单...")  # 调试信息
            asn_result = create_asn_order(
                base_url=self.base_url,
                headers=self.headers,
                owner_info=self.current_owner
            )

            # 检查验收单创建结果
            if not isinstance(asn_result, dict):
                QMessageBox.warning(self, "错误", "创建验收单失败")
                return

            # 3. 创建质检单
            print("3. 创建质检单...")  # 调试信息
            qc_result = make_put_shelf_data(
                base_url=self.base_url,
                headers=self.headers,
                owner_info=self.current_owner
            )

            # 检查质检单创建结果
            if not isinstance(qc_result, dict) or qc_result.get('code') != 200:
                error_msg = qc_result.get('msg', '未知错误') if isinstance(qc_result, dict) else '创建质检单失败'
                QMessageBox.warning(self, "错误", f"创建质检单失败: {error_msg}")
                return

            # 4. 执行上架
            print("4. 执行上架...")  # 调试信息
            put_shelf_result = put_shelf_down(
                base_url=self.base_url,
                headers=self.headers,
                owner_info=self.current_owner
            )

            # 处理最终结果
            if isinstance(put_shelf_result, dict) and put_shelf_result.get('code') == 200:
                # 读取质检单号
                qc_data = read_yaml('qc_data.yaml')
                qc_no = qc_data.get('qcNo', '') if qc_data else ''

                success_message = (
                    f"一键入库成功\n"
                    f"入库单号: {in_order_result['order_no']}\n"
                    f"验收单号: {qc_no}"  # 使用质检单号作为验收单号
                )
                QMessageBox.information(self, "成功", success_message)
            else:
                error_msg = put_shelf_result.get('msg', '未知错误') if isinstance(put_shelf_result, dict) else '上架失败'
                QMessageBox.warning(self, "错误", f"上架失败: {error_msg}")

        except Exception as e:
            print(f"一键入库异常: {str(e)}")
            QMessageBox.warning(self, "错误", f"一键入库时发生异常: {str(e)}")
        finally:
            self.quick_storage_button.stop_loading()

    def generate_outbound(self):
        """生成出库单"""
        try:
            print("开始生成出库单...")  # 调试信息
            print(f"按钮状态: {self.generate_outbound_button}")  # 检查按钮是否存在

            if not self.generate_outbound_button:
                print("警告：出库按钮未初始化")
                self.generate_outbound_button = LoadingButton('生成出库单')
                self.generate_outbound_button.clicked.connect(self.generate_outbound)

            self.generate_outbound_button.start_loading()

            # 检查是否选择了商品
            if not self.selected_outbound_sku_details:
                QMessageBox.warning(self, "警告", "请先选择要出库的商品")
                return

            # 获取选中的出库单类型
            selected_type = self.get_selected_outbound_type_value()
            if not selected_type:
                QMessageBox.warning(self, "警告", "请选择出库单类型")
                return

            # 获取当前选中的货主信息
            current_text = self.outbound_owner_combo.currentText()
            owner_info = self.owner_dict.get(current_text)

            # 检查仓库信息
            if not self.warehouse_id or not self.warehouse_name or not owner_info:
                QMessageBox.warning(self, "警告", "缺少仓库信息或货主信息，请确保已正确登录并选择货主")
                return

            # 打印调试信息
            print(f"warehouse_id: {self.warehouse_id}")
            print(f"warehouse_name: {self.warehouse_name}")
            print(f"owner_info: {owner_info}")
            print(f"selected_type: {selected_type}")
            print(f"sku_details: {self.selected_outbound_sku_details}")

            # 调用创建出库单方法
            result = create_out_order(
                base_url=self.base_url,
                headers=self.headers,
                order_type=selected_type,
                owner_info=owner_info,
                sku_details=self.selected_outbound_sku_details,
                warehouse_id=self.warehouse_id,
                warehouse_name=self.warehouse_name  # 添加仓库名称参数
            )

            # 处理返回结果
            if isinstance(result, dict):
                if result.get('code') == 200:
                    order_no = result.get('obj', {}).get('orderNo', '')
                    success_message = (
                        f"出库单创建成功\n"
                        f"订单号: {order_no}\n"
                        f"货主: {owner_info.get('ownerName')}\n"
                        f"商品数量: {len(self.selected_outbound_sku_details)}个\n"
                        f"仓库: {self.warehouse_name}"
                    )
                    QMessageBox.information(self, "成功", success_message)

                    # 更新状态标签
                    self.status_label.setText(
                        f"出库单创建成功\n"
                        f"订单号: {order_no}\n"
                        f"货主: {owner_info.get('ownerName')}\n"
                        f"订单类型: {self.outbound_type_combo.currentText()}\n"
                        f"仓库: {self.warehouse_name}"
                    )
                else:
                    error_msg = result.get('msg', '未知错误')
                    QMessageBox.warning(self, "错误", f"创建出库单失败: {error_msg}")
            else:
                QMessageBox.warning(self, "错误", f"创建出库单失败: {str(result)}")

        except Exception as e:
            print(f"生成出库单异常: {str(e)}")
            QMessageBox.warning(self, "错误", f"生成出库单时发生异常: {str(e)}")
        finally:
            self.generate_outbound_button.stop_loading()

    def generate_pick(self):
        """生成拣货单"""
        try:
            self.generate_pick_button.start_loading()
            # TODO: 实现拣货单生成逻辑
            QMessageBox.information(self, "提示", "拣货单生成功能开发中...")

        except Exception as e:
            print(f"生成拣货单异常: {str(e)}")
            QMessageBox.warning(self, "错误", f"生成拣货单时发生异常: {str(e)}")
        finally:
            self.generate_pick_button.stop_loading()

    def quick_outbound(self):
        """一键出库"""
        try:
            self.quick_outbound_button.start_loading()
            selected_product = self.outbound_product_combo.currentText()
            selected_type = self.outbound_type_combo.currentText()
            need_trace = 1 if self.outbound_trace_checkbox.isChecked() else 0
            is_seed = 1 if self.outbound_seed_checkbox.isChecked() else 0  # 新增播种标记

            # TODO: 实现一键出库逻辑
            QMessageBox.information(self, "提示", "一键出库功能开发中...")

        except Exception as e:
            print(f"一键出库异常: {str(e)}")
            QMessageBox.warning(self, "错误", f"一键出库时发生异常: {str(e)}")
        finally:
            self.quick_outbound_button.stop_loading()

    def get_selected_outbound_type_value(self):
        """获取选中的出库单类型值"""
        current_text = self.outbound_type_combo.currentText()
        for type_info in self.outbound_types:
            if type_info["key"] == current_text:
                return type_info["value"]
        return None

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
        """处理出库商品选择事件"""
        try:
            selected_items = self.outbound_product_list.selectedItems()
            self.selected_outbound_sku_details = []
            
            if not selected_items:
                self.status_label.setText("未选择任何商品")
                return
            
            # 分类存储整件和零货商品
            whole_pieces = []
            single_pieces = []
            
            # 遍历所有选中的商品项
            for item in selected_items:
                item_text = item.text()
                parts = item_text.split(' - ')
                if len(parts) >= 4:  # 确保有足够的部分可以解析
                    sku_name = parts[0]
                    spec = parts[1]
                    package_type = parts[2]  # 包装规格（整件/零货）
                    # 处理最后一部分，它包含商品编码和库存信息
                    last_part = parts[-1]
                    sku_code = last_part.split(' (')[0]
                    usable_qty = last_part.split('可用库存: ')[-1].rstrip(')')
                    
                    # 构建商品数据
                    sku_data = {
                        'skuName': sku_name,
                        'spec': spec,
                        'packageType': package_type,
                        'skuCode': sku_code,
                        'usableQty': float(usable_qty),
                        'planQty': float(usable_qty)  # 设置计划数量等于可用数量
                    }
                    
                    # 根据包装类型分类
                    if '整件' in package_type:
                        whole_pieces.append(sku_data)
                    else:
                        single_pieces.append(sku_data)
                    
                    self.selected_outbound_sku_details.append(sku_data)
            
            # 构建状态文本
            status_text = f"已选择 {len(selected_items)} 个商品:\n"
            
            # 显示整件商品
            if whole_pieces:
                status_text += "\n=== 整件商品 ===\n"
                for index, sku in enumerate(whole_pieces, 1):
                    status_text += f"\n{index}. {sku['skuName']}:\n"
                    status_text += (
                        f"   • 商品编码: {sku['skuCode']}\n"
                        f"   • 规格: {sku['spec']}\n"
                        f"   • 包装类型: {sku['packageType']}\n"
                        f"   • 可用数量: {sku['usableQty']}\n"
                        f"   • 计划出库数量: {sku['planQty']}\n"
                    )
            
            # 显示零货商品
            if single_pieces:
                status_text += "\n=== 零货商品 ===\n"
                for index, sku in enumerate(single_pieces, 1):
                    status_text += f"\n{index}. {sku['skuName']}:\n"
                    status_text += (
                        f"   • 商品编码: {sku['skuCode']}\n"
                        f"   • 规格: {sku['spec']}\n"
                        f"   • 包装类型: {sku['packageType']}\n"
                        f"   • 可用数量: {sku['usableQty']}\n"
                        f"   • 计划出库数量: {sku['planQty']}\n"
                    )
            
            # 添加汇总信息
            status_text += f"\n=== 汇总信息 ===\n"
            status_text += f"整件商品数: {len(whole_pieces)} 个\n"
            status_text += f"零货商品数: {len(single_pieces)} 个\n"
            
            # 更新状态标签显示
            if self.selected_outbound_sku_details:
                self.status_label.setText(status_text)
            else:
                self.status_label.setText("未能获取选中商品的详细信息")
            
        except Exception as e:
            print(f"选择商品时发生错误: {str(e)}")
            QMessageBox.warning(self, '警告', f'选择商品失败：{str(e)}')

    def on_owner_selected(self):
        """处理入库货主选择变化"""
        try:
            current_text = self.storage_owner_combo.currentText()
            owner_info = self.owner_dict.get(current_text)
            if owner_info:
                self.current_owner = {
                    'origCompanyCode': owner_info.get('origCompanyCode', ''),
                    'ownerCode': owner_info.get('ownerCode', ''),
                    'ownerName': owner_info.get('ownerName', ''),  # 添加货主名称
                    'id': owner_info.get('id', '')  # 添加货主ID
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
                    'ownerCode': owner_info.get('ownerCode', ''),
                    'ownerName': owner_info.get('ownerName', ''),  # 添加货主名称
                    'id': owner_info.get('id', '')  # 添加货主ID
                }

                # 更新状态显示
                self.status_label.setText(
                    f"已选择出库货主:\n"
                    f"货主名称: {owner_info.get('ownerName')}\n"
                    f"货主编码: {owner_info.get('ownerCode')}\n"
                    f"公司编码: {owner_info.get('origCompanyCode')}\n"
                    f"货主类型: {owner_info.get('ownerTypeStr')}"
                )

                # 清空商品列表
                self.outbound_product_list.clear()

                # 获取可用库存商品列表
                result = get_out_sku_details(
                    base_url=self.base_url,
                    owner_info=owner_info,
                    headers=self.headers
                )

                if isinstance(result, list):
                    self.sku_list = result
                    # 更新商品列表显示
                    for sku in result:
                        sku_name = sku.get('skuName', '')
                        spec = sku.get('spec', '')
                        sku_code = sku.get('skuCode', '')
                        usable_qty = sku.get('usableQty', 0)
                        package_attr = sku.get('packageAttrName', '')  # 获取包装规格

                        # 构建显示文本，包含包装规格
                        display_text = (
                            f"{sku_name} - {spec}"
                            f"{f' - {package_attr}' if package_attr else ''}"  # 如果有包装规格则显示
                            f" - {sku_code} (可用库存: {usable_qty})"
                        )

                        self.outbound_product_list.addItem(display_text)
                else:
                    QMessageBox.warning(self, "警告", f"获取商品列表失败：{result}")

        except Exception as e:
            print(f"选择货主异常: {str(e)}")
            QMessageBox.warning(self, "错误", f"选择货主失败: {str(e)}")

    def set_warehouse_id(self, warehouse_id):
        """设置仓库ID"""
        print(f"设置仓库ID: {warehouse_id}")  # 添加调试信息
        self.warehouse_id = warehouse_id

    def set_warehouse_name(self, warehouse_name):
        """设置仓库名称"""
        print(f"设置仓库名称: {warehouse_name}")  # 添加调试信息
        self.warehouse_name = warehouse_name

    def one_click_putaway(self):
        """一键上架"""
        try:
            self.putaway_button.start_loading()

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
            owner_name = owner_info.get('ownerName') if owner_info else None

            # 检查仓库信息
            if not self.warehouse_id or not owner_name:
                QMessageBox.warning(self, "警告", "缺少仓库信息或货主名称，请确保已正确登录并选择货主")
                return

            # 1. 先调用创建入库单接口
            in_order_result = create_in_order(
                base_url=self.base_url,
                headers=self.headers,
                order_type=selected_type_value,
                owner_info=self.current_owner,
                sku_details=self.selected_sku_details,
                is_whole_piece=1 if self.whole_piece_checkbox.isChecked() else 0,
                is_mixed=1 if self.mixed_checkbox.isChecked() else 0,
                warehouse_id=self.warehouse_id,
                warehouse_name=owner_name
            )

            # 检查入库单创建结果
            if not isinstance(in_order_result, dict) or in_order_result['result'].get('code') != 200:
                error_msg = in_order_result['result'].get('msg', '未知错误') if isinstance(in_order_result, dict) else '创建入库单失败'
                QMessageBox.warning(self, "错误", f"创建入库单失败: {error_msg}")
                return

            # 2. 调用创建验收单接口
            asn_result = create_asn_order(
                base_url=self.base_url,
                headers=self.headers,
                owner_info=self.current_owner
            )

            # 检查验收单创建结果
            if not isinstance(asn_result, dict):
                QMessageBox.warning(self, "错误", "创建验收单失败")
                return

            # 3. 调用上架接口
            print("调用上架接口...")  # 调试信息
            put_shelf_result = make_put_shelf_data(
                base_url=self.base_url,
                headers=self.headers,
                owner_info=self.current_owner
            )

            # 处理最终结果
            if isinstance(put_shelf_result, dict) and put_shelf_result.get('code') == 200:
                # 读取质检单号
                qc_data = read_yaml('qc_data.yaml')
                qc_no = qc_data.get('qcNo', '') if qc_data else ''

                success_message = (
                    f"一键上架成功\n"
                    f"入库单号: {in_order_result['order_no']}\n"
                    f"验收单号: {qc_no}"  # 使用质检单号作为验收单号
                )
                QMessageBox.information(self, "成功", success_message)
            else:
                error_msg = put_shelf_result.get('msg', '未知错误') if isinstance(put_shelf_result, dict) else '上架失败'
                QMessageBox.warning(self, "错误", f"上架失败: {error_msg}")

        except Exception as e:
            print(f"一键上架异常: {str(e)}")
            QMessageBox.warning(self, "错误", f"一键上架时发生异常: {str(e)}")
        finally:
            self.putaway_button.stop_loading()

    def generate_putaway(self):
        """生成上架单"""
        print("generate_putaway 方法被调用")  # 添加调试打印
        try:
            self.putaway_button.start_loading()
            print("开始生成上架单...")  # 调试信息

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
            owner_name = owner_info.get('ownerName') if owner_info else None

            # 检查仓库信息
            if not self.warehouse_id or not owner_name:
                QMessageBox.warning(self, "警告", "缺少仓库信息或货主名称，请确保已正确登录并选择货主")
                return

            # 1. 先调用创建入库单接口
            print("调用创建入库单接口...")  # 调试信息
            in_order_result = create_in_order(
                base_url=self.base_url,
                headers=self.headers,
                order_type=selected_type_value,
                owner_info=self.current_owner,
                sku_details=self.selected_sku_details,
                is_whole_piece=1 if self.whole_piece_checkbox.isChecked() else 0,
                is_mixed=1 if self.mixed_checkbox.isChecked() else 0,
                warehouse_id=self.warehouse_id,
                warehouse_name=owner_name
            )

            # 检查入库单创建结果
            if not isinstance(in_order_result, dict) or in_order_result['result'].get('code') != 200:
                error_msg = in_order_result['result'].get('msg', '未知错误') if isinstance(in_order_result, dict) else '创建入库单失败'
                QMessageBox.warning(self, "错误", f"创建入库单失败: {error_msg}")
                return

            # 2. 调用创建验收单接口
            print("调用创建验收单接口...")  # 调试信息
            asn_result = create_asn_order(
                base_url=self.base_url,
                headers=self.headers,
                owner_info=self.current_owner
            )

            # 检查验收单创建结果
            if not isinstance(asn_result, dict):
                QMessageBox.warning(self, "错误", "创建验收单失败")
                return

            # 3. 调用上架接口
            print("调用上架接口...")  # 调试信息
            put_shelf_result = make_put_shelf_data(
                base_url=self.base_url,
                headers=self.headers,
                owner_info=self.current_owner
            )

            # 处理最终结果
            if isinstance(put_shelf_result, dict) and put_shelf_result.get('code') == 200:
                # 读取质检单号
                qc_data = read_yaml('qc_data.yaml')
                qc_no = qc_data.get('qcNo', '') if qc_data else ''

                success_message = (
                    f"上架单创建成功\n"
                    f"入库单号: {in_order_result['order_no']}\n"
                    f"验收单号: {qc_no}"  # 使用质检单号作为验收单号
                )
                QMessageBox.information(self, "成功", success_message)
            else:
                error_msg = put_shelf_result.get('msg', '未知错误') if isinstance(put_shelf_result, dict) else '上架失败'
                QMessageBox.warning(self, "错误", f"上架失败: {error_msg}")

        except Exception as e:
            print(f"生成上架单异常: {str(e)}")  # 调试信息
            QMessageBox.warning(self, "错误", f"生成上架单时发生异常: {str(e)}")
        finally:
            self.putaway_button.stop_loading()

    def test_click(self):
        print("测试点击")
        QMessageBox.information(self, "测试", "按钮点击成功")
