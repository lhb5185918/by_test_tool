import requests
import time
from datetime import datetime, timedelta
import random
import yaml  # 添加到文件顶部的导入语句中
import os
import sys
import websocket  # 需要先 pip install websocket-client
import json
import threading


def generate_number(sequence=15):
    """
    生成编号
    sequence: 三位序号(1-999)
    """
    # 获取当前日期
    now = datetime.now()
    # 格式化日期部分
    date_str = now.strftime("%Y%m%d")
    # 组合编号
    return f"{date_str}"


# 使用示例
number = generate_number(15)  # 输出类似: 20250102015


def select_sku(is_drug, base_url, headers):
    """
    获取商品列表
    Args:
        is_drug: 是否药品
        base_url: 基础URL
        headers: 请求头
    Returns:
        dict: 商品列表
    """
    url = f"{base_url}/wms/sku/sku/pageInfo"
    data = {
        "productFormType": "YP",
        "idStr": None,
        "ownerId": None,
        "isDrugSuperCode": 0,
        "isDoubleCheck": 0,
        "page": 1,
        "limit": 50,
        "orderByColumnList": None
    }
    if is_drug == 1:
        data["isDrugSuperCode"] = 1
        response = requests.post(url, json=data, headers=headers)
        res = response.json()
        return response.json()
    elif is_drug == 0:
        data["isDrugSuperCode"] = 0
        response = requests.post(url, json=data, headers=headers)
        res = response.json()
        return response.json()
    else:
        return "is_drug参数错误"


def get_owner_list(base_url, headers):
    """获取货主列表"""
    try:
        url = f"{base_url}/wms/tm/owner/pageInfo"
        data = {
            "orderByColumnList": None,
            "ownerCode": None,
            "ownerName": None,
            "ownerShortName": None,
            "page": 1,
            "limit": 50
        }
        response = requests.post(url, json=data, headers=headers)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"获取货主列表失败: {str(e)}")
        return None


def get_warehouse_inventory(base_url, headers, owner_info):
    """获取商品库存信息"""
    url = f"{base_url}/wms/report/stock/stockInfoRpt/pageInfo"
    if owner_info == "QDBYYYGF":
        data = {
            "ownerId": "103",
            "orgIdList": [
                "1215770969117184"
            ],
            "enterWarehouseStatus": "SJWC",
            "skuCategoryIdList": [
                1114711910617600
            ],
            "orderByColumnList": [],
            "page": 1,
            "limit": 50
        }
        response = requests.post(url, json=data, headers=headers)
        sku_list = []
        for sku_data in response.json()['obj']:
            if sku_data['usableQty'] > 0:
                sku_list.append(sku_data)
                return sku_list
    elif owner_info == "01":
        data = {
            "ownerId": "100",
            "orgIdList": [
                "1098994695180800"
            ],
            "enterWarehouseStatus": "SJWC",
            "skuCategoryIdList": [
                1114711910617600
            ],
            "orderByColumnList": [],
            "page": 1,
            "limit": 50
        }
        response = requests.post(url, json=data, headers=headers)
        sku_list = []
        for sku_data in response.json()['obj']:
            if sku_data['usableQty'] > 0:
                sku_list.append(sku_data)
                return sku_list


def get_sku_detail(base_url, headers, sku_code):
    """
    获取商品明细数据
    Args:
        base_url: 基础URL
        headers: 请求头
        sku_code: 商品编码(字符串)或商品编码列表
    Returns:
        dict/list: 单个商品返回字典，多个商品返回列表
    """
    try:
        url = f"{base_url}/wms/sku/sku/pageInfo"

        # 处理单个商品编码或多个商品编码的情况
        if isinstance(sku_code, str):
            sku_codes = [sku_code]
        elif isinstance(sku_code, (list, tuple)):
            sku_codes = sku_code
        else:
            return {"error": "无效的商品编码格式"}

        sku_details = []
        for code in sku_codes:
            data = {
                "productFormType": "YP",
                "skuCode": code,
                "page": 1,
                "limit": 1,
                "orderByColumnList": None
            }
            response = requests.post(url, json=data, headers=headers)
            result = response.json()

            if result.get("code") == 200 and result.get("obj"):
                sku_detail = result["obj"][0]
                detail_dict = {
                    "skuCode": sku_detail.get("skuCode"),
                    "skuName": sku_detail.get("skuName"),
                    "mainUnit": sku_detail.get("mainUnit"),
                    "departmentCode": "N0028",  # 默认部门编码
                    "rowSupplierCode": "S00024171",  # 默认供应商编码
                    "amount": 16000.12,  # 默认金额
                    "inOrderQty": sku_detail.get('perQty'),  # 数量需要用户输入
                    "productionDate": "",  # 生产日期需要用户输入
                    "invalidDate": "",  # 有效期需要用户输入
                    "productionBatch": "",  # 批次号需要用户输入
                    "spec": sku_detail.get("spec"),  # 规格
                    "approvalNumber": sku_detail.get("approvalNumber"),  # 批准文号
                    "mfg": sku_detail.get("mfg"),  # 生产厂家
                    "isBatchManage": sku_detail.get("isBatchManage"),  # 是否批次管理
                    "isValidity": sku_detail.get("isValidity"),  # 是否效期管理
                    "validityDay": sku_detail.get("validityDay"),  # 有效期天数
                    "perQty": sku_detail.get("perQty"),  # 每包装数量
                }
                sku_details.append(detail_dict)
            else:
                return {"error": f"获取商品 {code} 明细失败: {result.get('msg', '未知错误')}"}

        # 如果只有一个商品，返回字典；否则返回列表
        return sku_details[0] if len(sku_details) == 1 else sku_details

    except Exception as e:
        return {"error": f"获取商品明细失败: {str(e)}"}


def get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type=None, owner_info=None):
    """获取仓库编码"""
    url = f"{base_url}/oauth/password/unencrypted"
    data = {"userNo": "lhb2", "pwd": "Lhx7758521!", "platForm": "Web", "companyCode": "QDBYYYGF", "whId": "",
            "warehouseId": "", "haveWarehouse": "0", "clientId": "zhqc-sso", "userLanguage": "zh-CN"}
    response = requests.post(url=url, json=data, headers={'Content-Type': 'application/json'})
    token = response.json().get('obj').get('token')
    headers = {'Content-Type': 'application/json', 'Authorization': token}

    # 获取仓库列表
    select_warehouse_code_url = f"{base_url}/oms/base/whOrig/pageInfo"
    select_warehouse_code_data = {
        "orderByColumnList": None,
        "page": 1,
        "limit": 50
    }
    select_warehouse_code_response = requests.post(url=select_warehouse_code_url,
                                                   json=select_warehouse_code_data,
                                                   headers=headers)
    warehouse_list = select_warehouse_code_response.json()['obj']

    # 处理方式一：返回source_code和target_code
    if order_type:
        for warehouse in warehouse_list:
            if warehouse['whId'] == warehouse_id and warehouse['origCompanyName'] == warehouse_name:
                if warehouse['origCompanyName'] == '青岛百洋医药股份有限公司':
                    if warehouse['origCode'] == '50001':
                        return {"source_code": "50001", "target_code": "50002"}
                    else:
                        return {"source_code": "50002", "target_code": "50001"}
                elif warehouse['origCompanyName'] == '青岛百洋健康药房连锁有限公司':
                    if warehouse['origCode'] == '2000':
                        return {"source_code": "2000", "target_code": "3000"}
                    else:
                        return {"source_code": "3000", "target_code": "2000"}
        # 如果没有找到匹配的仓库，返回默认值
        return {"source_code": "50001", "target_code": "50002"}

    # 处理方式二：返回单个仓库编码
    else:
        # 如果有owner_info，使用owner_info匹配
        if owner_info:
            for warehouse in warehouse_list:
                if (warehouse['whId'] == warehouse_id and
                        warehouse['origCompanyName'] == warehouse_name and
                        owner_info['origCompanyCode'] == warehouse['origCompanyCode']):
                    return warehouse['origCode']

        # 如果没有owner_info或上面没找到，使用简单匹配
        for warehouse in warehouse_list:
            if warehouse['whId'] == warehouse_id and warehouse['origCompanyName'] == warehouse_name:
                return warehouse['origCode']

        # 如果都没找到，返回默认值
        return "50001"


def get_app_path():
    """获取应用程序路径"""
    if getattr(sys, 'frozen', False):
        # PyInstaller打包后的路径
        return os.path.dirname(sys.executable)
    # 开发环境路径
    return os.path.dirname(os.path.abspath(__file__))


def read_yaml(file_path):
    """读取YAML文件"""
    try:
        # 确保文件存在
        if not os.path.exists(file_path):
            # 尝试在应用程序目录下查找
            app_path = get_app_path()
            file_path = os.path.join(app_path, file_path)

            # 如果还是不存在，创建空文件
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.safe_dump({}, f)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data if data else {}
    except Exception as e:
        print(f"读取YAML文件失败: {str(e)}")
        return {}


def write_yaml(file_path, data):
    """写入YAML文件"""
    try:
        # 确保目录存在
        app_path = get_app_path()
        full_path = os.path.join(app_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        print(f"写入YAML文件失败: {str(e)}")
        return False


# 使用示例:
"""
# 读取YAML文件
config = read_yaml('config.yaml')
if config:
    print("读取成功:", config)

# 写入YAML文件
data = {
    'environment': {
        'dev': {
            'host': 'http://dev.example.com',
            'port': 8080
        },
        'prod': {
            'host': 'http://prod.example.com',
            'port': 80
        }
    },
    'settings': {
        'debug': True,
        'timeout': 30
    }
}

if write_yaml('config.yaml', data):
    print("写入成功")
"""


def generate_date(days_offset=0):
    """
    生成指定格式的日期字符串，时分秒固定为00:00

    Args:
        days_offset (int): 相对当前日期的偏移天数，可以是正数或负数
                          正数表示未来日期，负数表示过去日期

    Returns:
        str: 格式化的日期字符串，如 '2025-01-11 00:00'

    Example:
        print(generate_date())  # 当天日期 00:00
        print(generate_date(1))  # 明天 00:00
        print(generate_date(-1))  # 昨天 00:00
    """
    # 获取当前日期
    current_date = datetime.now()

    # 添加偏移天数
    target_date = current_date + timedelta(days=days_offset)

    # 将时分秒设置为00:00
    target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)

    # 返回格式化的日期字符串
    return target_date.strftime('%Y-%m-%d %H:%M')


def add_check_status_to_wait_rec_list(data_dict):
    """
    为waitRecList中的每个字典添加检查状态字段

    Args:
        data_dict (dict): 包含waitRecList的字典

    Returns:
        dict: 处理后的字典
    """
    # 检查是否存在waitRecList字段
    if 'waitRecList' not in data_dict or not data_dict['waitRecList']:
        return data_dict

    # 为每个字典添加新字段
    for index, item in enumerate(data_dict['waitRecList']):
        additional_fields = {
            "isChecked": True,
            "isCheckedNo": True,
            "isSecondCheck": "allFinish",
            "_X_ROW_KEY": "row_2793"  # 根据索引生成不同的row key
        }
        item.update(additional_fields)

    return data_dict


def add_check_status_to_wait_qc_list(data_dict):
    """
    为waitRecList中的每个字典添加检查状态字段

    Args:
        data_dict (dict): 包含waitRecList的字典

    Returns:
        dict: 处理后的字典
    """
    # 检查是否存在waitRecList字段
    if 'waitQcDtList' not in data_dict['obj']:
        return data_dict

    # 为每个字典添加新字段
    for index, item in enumerate(data_dict['obj']['waitQcDtList']):
        additional_fields = {
            "_X_ROW_KEY": "row_19",
            "checkResultDesc": None,
            "handleMeasure": None
        }
        item['checkResult'] = 'HG'
        item.update(additional_fields)

    return data_dict


def add_check_status_to_wait_put_list(data_dict):
    """
    为waitRecList中的每个字典添加检查状态字段

    Args:
        data_dict (dict): 包含waitRecList的字典

    Returns:
        dict: 处理后的字典
    """
    # 检查是否存在waitRecList字段
    if 'waitPutShelfTaskDtList' not in data_dict:
        return data_dict

    # 为每个字典添加新字段
    for index, item in enumerate(data_dict['waitPutShelfTaskDtList']):
        additional_fields = {
            "_X_ROW_KEY": "row_703"
        }
        item.update(additional_fields)

    return data_dict


def get_out_sku_details(base_url, owner_info, headers, is_drug=0):
    """获取出库商品库存信息"""
    select_sku_inventory_url = f"{base_url}/wms/report/stock/stockInfoRpt/pageInfo"
    inventory_list = []
    all_sku_codes = []

    try:
        if owner_info['ownerCode'] == 'QDBYYYGF':
            # 分页获取库存信息
            page = 1
            while True:
                select_sku_inventory_data = {
                    "ownerId": "103",
                    "orgIdList": ["1215770969117184"],
                    "stockStatusList": ["HG"],
                    "enterWarehouseStatus": "SJWC",
                    "stockSourceList": ["PT"],
                    "skuCategoryIdList": [1114711910617600],
                    "orderByColumnList": ["instore_date desc"],
                    "page": page,
                    "limit": 100
                }

                inventory_response = requests.post(
                    select_sku_inventory_url,
                    json=select_sku_inventory_data,
                    headers=headers
                ).json()

                # 收集有库存的商品编码
                for sku_detail in inventory_response['obj']:
                    if sku_detail['usableQty'] > 0:
                        # 判断是否为整件商品
                        if sku_detail['packageAttrName'] == '整件':
                            # 判断每箱数量是否为整数
                            if sku_detail['usableQty'] % sku_detail['perQty'] == 0:
                                all_sku_codes.append(sku_detail['skuCode'])
                        else:
                            # 非整件商品直接添加
                            all_sku_codes.append(sku_detail['skuCode'])

                # 判断是否还有下一页
                if len(inventory_response['obj']) < 100:
                    break
                page += 1

            if all_sku_codes:
                # 分页查询商品追溯码状态
                drug_sku_codes = set()
                page = 1
                chunk_size = 100  # 每次查询的商品数量

                while True:
                    # 计算当前页的商品编码范围
                    start_idx = (page - 1) * chunk_size
                    end_idx = min(start_idx + chunk_size, len(all_sku_codes))
                    current_sku_codes = all_sku_codes[start_idx:end_idx]

                    if not current_sku_codes:
                        break

                    select_drug_data = {
                        "productFormType": "YP",
                        "ownerId": "103",
                        "skuCodes": ",".join(current_sku_codes),
                        "isDrugSuperCode": 1,
                        "page": 1,
                        "limit": 100,
                        "orderByColumnList": None
                    }

                    drug_response = requests.post(
                        f"{base_url}/wms/sku/sku/pageInfo",
                        json=select_drug_data,
                        headers=headers
                    ).json()

                    # 收集需要追溯码的商品编码
                    drug_sku_codes.update(
                        sku['skuCode'] for sku in drug_response.get('obj', [])
                    )

                    page += 1

                # 重新遍历库存数据，根据追溯码状态筛选
                page = 1
                while True:
                    select_sku_inventory_data['page'] = page
                    inventory_response = requests.post(
                        select_sku_inventory_url,
                        json=select_sku_inventory_data,
                        headers=headers
                    ).json()

                    for sku_detail in inventory_response['obj']:
                        if sku_detail['usableQty'] > 0:
                            sku_code = sku_detail['skuCode']
                            # 判断是否为整件商品
                            if sku_detail['packageAttrName'] == '整件':
                                # 判断每箱数量是否为整数
                                if sku_detail['usableQty'] % sku_detail['perQty'] == 0:
                                    if is_drug == 1 and sku_code in drug_sku_codes:
                                        inventory_list.append(sku_detail)
                                    elif is_drug == 0 and sku_code not in drug_sku_codes:
                                        inventory_list.append(sku_detail)
                            else:
                                # 非整件商品直接添加
                                if is_drug == 1 and sku_code in drug_sku_codes:
                                    inventory_list.append(sku_detail)
                                elif is_drug == 0 and sku_code not in drug_sku_codes:
                                    inventory_list.append(sku_detail)

                    if len(inventory_response['obj']) < 100:
                        break
                    page += 1

            return inventory_list

        elif owner_info['ownerCode'] == '01':
            # 分页获取库存信息
            page = 1
            while True:
                select_sku_inventory_data = {
                    "ownerId": "100",
                    "orgIdList": ["1098994695180800"],
                    "stockStatusList": ["HG"],
                    "enterWarehouseStatus": "SJWC",
                    "stockSourceList": ["PT"],
                    "skuCategoryIdList": [1114711910617600],
                    "orderByColumnList": ["instore_date desc"],
                    "page": page,
                    "limit": 100
                }

                inventory_response = requests.post(
                    select_sku_inventory_url,
                    json=select_sku_inventory_data,
                    headers=headers
                ).json()

                # 收集有库存的商品编码
                for sku_detail in inventory_response['obj']:
                    if sku_detail['usableQty'] > 0:
                        # 判断是否为整件商品
                        if sku_detail['packageAttrName'] == '整件':
                            # 判断每箱数量是否为整数
                            if sku_detail['usableQty'] % sku_detail['perQty'] == 0:
                                all_sku_codes.append(sku_detail['skuCode'])
                        else:
                            # 非整件商品直接添加
                            all_sku_codes.append(sku_detail['skuCode'])

                if len(inventory_response['obj']) < 100:
                    break
                page += 1

            if all_sku_codes:
                # 分页查询商品追溯码状态
                drug_sku_codes = set()
                page = 1
                chunk_size = 100

                while True:
                    start_idx = (page - 1) * chunk_size
                    end_idx = min(start_idx + chunk_size, len(all_sku_codes))
                    current_sku_codes = all_sku_codes[start_idx:end_idx]

                    if not current_sku_codes:
                        break

                    select_drug_data = {
                        "productFormType": "YP",
                        "ownerId": "100",  # 修改为对应的货主ID
                        "skuCodes": ",".join(current_sku_codes),
                        "isDrugSuperCode": 1,
                        "page": 1,
                        "limit": 100,
                        "orderByColumnList": None
                    }

                    drug_response = requests.post(
                        f"{base_url}/wms/sku/sku/pageInfo",
                        json=select_drug_data,
                        headers=headers
                    ).json()

                    drug_sku_codes.update(
                        sku['skuCode'] for sku in drug_response.get('obj', [])
                    )

                    page += 1

                # 重新遍历库存数据，根据追溯码状态筛选
                page = 1
                while True:
                    select_sku_inventory_data['page'] = page
                    inventory_response = requests.post(
                        select_sku_inventory_url,
                        json=select_sku_inventory_data,
                        headers=headers
                    ).json()

                    for sku_detail in inventory_response['obj']:
                        if sku_detail['usableQty'] > 0:
                            sku_code = sku_detail['skuCode']
                            # 判断是否为整件商品
                            if sku_detail['packageAttrName'] == '整件':
                                # 判断每箱数量是否为整数
                                if sku_detail['usableQty'] % sku_detail['perQty'] == 0:
                                    if is_drug == 1 and sku_code in drug_sku_codes:
                                        inventory_list.append(sku_detail)
                                    elif is_drug == 0 and sku_code not in drug_sku_codes:
                                        inventory_list.append(sku_detail)
                            else:
                                # 非整件商品直接添加
                                if is_drug == 1 and sku_code in drug_sku_codes:
                                    inventory_list.append(sku_detail)
                                elif is_drug == 0 and sku_code not in drug_sku_codes:
                                    inventory_list.append(sku_detail)

                    if len(inventory_response['obj']) < 100:
                        break
                    page += 1

            return inventory_list

        else:
            return "暂不支持该货主"

    except Exception as e:
        print(f"获取出库商品库存信息失败: {str(e)}")
        return []


def get_user_info(base_url, headers, username, user_no):
    user_id_url = f'{base_url}/wms/org/user/queryUserCbList'
    user_id_data = {
        "queryText": f"{username}"
    }
    user_id_response = requests.post(user_id_url, json=user_id_data, headers=headers).json()['obj']
    for user in user_id_response:
        if user['userName'] == username and user['userNo'] == user_no:
            return {"id": user['id']}
        else:
            continue


def reconnect_websocket(base_url, warehouse_id, user_no):
    """重新连接WebSocket"""
    try:
        # 从base_url中提取域名和端口
        domain_port = base_url.split('//')[1]  # 获取 bswms-uat-01.baheal.com:7777

        # 构建WebSocket URL
        ws_url = f"ws://{domain_port}/webSocket/webSocket/customWebSocketHandler?userId={warehouse_id}_PC_PICK_{user_no}"

        # 创建WebSocket连接
        ws = websocket.WebSocket()
        ws.connect(ws_url)

        # 创建心跳线程保持连接
        def heartbeat():
            while True:
                try:
                    ws.send(json.dumps({"type": "heartbeat"}))
                    time.sleep(30)  # 每30秒发送一次心跳
                except:
                    break

        heartbeat_thread = threading.Thread(target=heartbeat)
        heartbeat_thread.daemon = True  # 设置为守护线程
        heartbeat_thread.start()

        return {
            'code': 200,
            'msg': '连接成功',
            'ws': ws  # 返回WebSocket连接对象
        }

    except Exception as e:
        return {
            'code': 500,
            'msg': f'连接异常: {str(e)}'
        }


def close_websocket(ws):
    """关闭WebSocket连接"""
    try:
        if ws:
            ws.close()
        return {
            'code': 200,
            'msg': '连接已关闭'
        }
    except Exception as e:
        return {
            'code': 500,
            'msg': f'关闭连接异常: {str(e)}'
        }
