import requests
import time
from datetime import datetime
import random


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
    url = f"{base_url}/wms/sku/sku/pageInfo"
    data = {
        "productFormType": "YP",
        "idStr": None,
        "ownerId": None,
        "isDrugSuperCode": 0,
        "page": 1,
        "limit": 50,
        "orderByColumnList": None
    }
    if is_drug == 1:
        data["isDrugSuperCode"] = 1
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    elif is_drug == 0:
        data["isDrugSuperCode"] = 0
        response = requests.post(url, json=data, headers=headers)
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
        return response.json()
    except Exception as e:
        print(f"获取货主列表失败: {str(e)}")
        return None


def get_warehouse_inventory(base_url, headers, owner_info):
    """获取商品库存信息"""
    url = f"{base_url}/wms/report/stock/stockInfoRpt/pageInfo"
    if owner_info['ownerCode'] == "QDBYYYGF":
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
    elif owner_info['ownerCode'] == "02":
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
                    "inOrderQty": 0,  # 数量需要用户输入
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


def get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type=None):
    """获取仓库编码"""
    url = f"{base_url}/oauth/password/unencrypted"
    data = {"userNo": "lhb2", "pwd": "Lhx7758521!", "platForm": "Web", "companyCode": "QDBYYYGF", "whId": "",
            "warehouseId": "", "haveWarehouse": "0", "clientId": "zhqc-sso", "userLanguage": "zh-CN"}
    response = requests.post(url=url, json=data, headers={'Content-Type': 'application/json'})
    token = response.json().get('obj').get('token')
    headers = {'Content-Type': 'application/json', 'Authorization': token}
    select_warehouse_code_url = f"{base_url}/oms/base/whOrig/pageInfo"
    select_warehouse_code_data = {
        "orderByColumnList": None,
        "page": 1,
        "limit": 50
    }
    select_warehouse_code_response = requests.post(url=select_warehouse_code_url, json=select_warehouse_code_data,
                                                   headers=headers)

    # 如果order_type不为None，返回source_code和target_code
    if order_type:
        for warehouse in select_warehouse_code_response.json()['obj']:
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

    # 如果order_type为None，返回单个仓库编码
    else:
        for warehouse in select_warehouse_code_response.json()['obj']:
            if warehouse['whId'] == warehouse_id and warehouse['origCompanyName'] == warehouse_name:
                return warehouse['origCode']
        # 如果没有找到匹配的仓库，返回默认值
        return "50001"


def create_in_order(base_url, headers, order_type, owner_info, sku_details, is_whole_piece, is_mixed, warehouse_id,
                    warehouse_name):
    """
    创建入库单
    Args:
        base_url: 基础URL
        headers: 请求头
        order_type: 订单类型
        owner_info: 货主信息字典，包含 origCompanyCode 和 ownerCode
        sku_details: 商品明细列表
    """
    url = f"{base_url}/oms/api/erp/apiInOrder/addOrUpdateInOrder"

    if order_type == 'CGDD':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "extendOne": "山东省青岛市市北区",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "",
                                "invalidDate": "",
                                "productionBatch": ""
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INT",
                        "origNo": f"CGDD-erp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "extendOne": "山东省青岛市市北区",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "",
                                "invalidDate": "",
                                "productionBatch": ""
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INT",
                        "origNo": f"CGDD-erp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "extendOne": "山东省青岛市市北区",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "",
                                "invalidDate": "",
                                "productionBatch": ""
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INT",
                        "origNo": f"CGDD-erp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "extendOne": "山东省青岛市市北区",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "",
                                "invalidDate": "",
                                "productionBatch": ""
                            },

                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INT",
                        "origNo": f"CGDD-erp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']) - 1,
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "extendOne": "山东省青岛市市北区",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INT",
                        "origNo": f"CGDD-erp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']) - 1,
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "extendOne": "山东省青岛市市北区",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INT",
                        "origNo": f"CGDD-erp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "extendOne": "山东省青岛市市北区",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INT",
                        "origNo": f"CGDD-erp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "extendOne": "山东省青岛市市北区",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INT",
                        "origNo": f"CGDD-erp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
    elif order_type == 'CGDDZP':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 15000000000,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionBatch": f"{generate_number()}",  # 生产批次号
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "rowSupplierCode": "S00024171",
                                "buyer": "李鸿宾"
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INTZP",
                        "origNo": f"CGDD-zp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-231213-000011",
                        "ecpOrderNo": "FHTZ-241231-0008",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 15000000000,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionBatch": f"{generate_number()}",  # 生产批次号
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "rowSupplierCode": "S00024171",
                                "buyer": "李鸿宾"
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INTZP",
                        "origNo": f"CGDD-zp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-231213-000011",
                        "ecpOrderNo": "FHTZ-241231-0008",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 15000000000,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionBatch": f"{generate_number()}",  # 生产批次号
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "rowSupplierCode": "S00024171",
                                "buyer": "李鸿宾"
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INTZP",
                        "origNo": f"CGDD-zp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-231213-000011",
                        "ecpOrderNo": "FHTZ-241231-0008",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 15000000000,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionBatch": f"{generate_number()}",  # 生产批次号
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "rowSupplierCode": "S00024171",
                                "buyer": "李鸿宾"
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INTZP",
                        "origNo": f"CGDD-zp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-231213-000011",
                        "ecpOrderNo": "FHTZ-241231-0008",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INTZP",
                        "origNo": f"CGDD-zp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-231213-000011",
                        "ecpOrderNo": "FHTZ-241231-0008",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INTZP",
                        "origNo": f"CGDD-zp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-231213-000011",
                        "ecpOrderNo": "FHTZ-241231-0008",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INTZP",
                        "origNo": f"CGDD-zp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-231213-000011",
                        "ecpOrderNo": "FHTZ-241231-0008",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "extendOne": "山东省青岛市市北区",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "INT",
                        "origNo": f"CGDD-erp-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
    elif order_type == 'ZPCGDD':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "PSTIN",
                        "origNo": f"ZPCGD-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-241230-00000",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "PSTIN",
                        "origNo": f"ZPCGD-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-241230-00000",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "PSTIN",
                        "origNo": f"ZPCGD-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-241230-00000",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "PSTIN",
                        "origNo": f"ZPCGD-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-241230-00000",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "PSTIN",
                        "origNo": f"ZPCGD-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-241230-00000",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "PSTIN",
                        "origNo": f"ZPCGD-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-241230-00000",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "PSTIN",
                        "origNo": f"ZPCGD-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-241230-00000",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "PSTIN",
                        "origNo": f"ZPCGD-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-241230-00000",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
    elif order_type == 'TCSQD':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 1,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDN",
                        "origNo": f"RTDN-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDN",
                        "origNo": f"RTDN-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDN",
                        "origNo": f"RTDN-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDN",
                        "origNo": f"RTDN-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDN",
                        "origNo": f"RTDN-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDN",
                        "origNo": f"RTDN-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDN",
                        "origNo": f"RTDN-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDN",
                        "origNo": f"RTDN-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
    elif order_type == 'TCSQDZP':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 1,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDNZP",
                        "origNo": f"TCZP-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDNZP",
                        "origNo": f"TCZP-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDNZP",
                        "origNo": f"TCZP-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 16000.12,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDNZP",
                        "origNo": f"TCZP-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDNZP",
                        "origNo": f"TCZP-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDNZP",
                        "origNo": f"TCZP-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDNZP",
                        "origNo": f"TCZP-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 15000000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionBatch": f"{generate_number()}",  # 生产批次号
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "rowSupplierCode": "S00024171",
                            "buyer": "李鸿宾"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "buyer": "李鸿宾",
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "RTDNZP",
                        "origNo": f"TCZP-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00077671",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
    elif order_type == 'WDTKSQD':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "adminAreaCode": "山东;青岛;市北区",
                        "contactAddr": "",
                        "contactName": "",
                        "contactPhone": "",
                        "contactTel": "",
                        "creator": "李鸿宾",
                        "buyer": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 136000000,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "invalidDate": "2025-12",
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "productionBatch": f"{generate_number()}",
                                "productionDate": "2025-01",
                                "rowSupplierCode": "S00005889",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "sourceOutNo": "test-erp-out-20241230015",
                                "sourceDiscountAmount": "11240000",
                                "sourceAmount": "10240000",
                                "buyer": "lihongbin"
                            }
                        ],
                        "erpCreateTime": 1666074517000,
                        "erpUpdateTime": 1666092926000,
                        "orderPrice": 311500000,
                        "olineCustomerId": "20100053",
                        "orderStatus": 1,
                        "orderType": "OL_BAC",
                        "refundReason": "包装损坏，退货退货退货",
                        "refundType": "OL_BAC",
                        "shopCode": "11231507",
                        "sourceCode": "DFHD-20241231-001",
                        "origNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 2,
                        "supplierCode": "S00004158",
                        "updater": "王玮霞",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}",
                        "origPlatform": "抖音"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "adminAreaCode": "山东;青岛;市北区",
                        "contactAddr": "",
                        "contactName": "",
                        "contactPhone": "",
                        "contactTel": "",
                        "creator": "李鸿宾",
                        "buyer": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 136000000,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']) - 1,
                                "invalidDate": "2025-12",
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "productionBatch": f"{generate_number()}",
                                "productionDate": "2025-01",
                                "rowSupplierCode": "S00005889",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "sourceOutNo": "test-erp-out-20241230015",
                                "sourceDiscountAmount": "11240000",
                                "sourceAmount": "10240000",
                                "buyer": "lihongbin"
                            }
                        ],
                        "erpCreateTime": 1666074517000,
                        "erpUpdateTime": 1666092926000,
                        "orderPrice": 311500000,
                        "olineCustomerId": "20100053",
                        "orderStatus": 1,
                        "orderType": "OL_BAC",
                        "refundReason": "包装损坏，退货退货退货",
                        "refundType": "OL_BAC",
                        "shopCode": "11231507",
                        "sourceCode": "DFHD-20241231-001",
                        "origNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 2,
                        "supplierCode": "S00004158",
                        "updater": "王玮霞",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}",
                        "origPlatform": "抖音"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "adminAreaCode": "山东;青岛;市北区",
                        "contactAddr": "",
                        "contactName": "",
                        "contactPhone": "",
                        "contactTel": "",
                        "creator": "李鸿宾",
                        "buyer": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 136000000,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "invalidDate": "2025-12",
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "productionBatch": f"{generate_number()}",
                                "productionDate": "2025-01",
                                "rowSupplierCode": "S00005889",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "sourceOutNo": "test-erp-out-20241230015",
                                "sourceDiscountAmount": "11240000",
                                "sourceAmount": "10240000",
                                "buyer": "lihongbin"
                            }
                        ],
                        "erpCreateTime": 1666074517000,
                        "erpUpdateTime": 1666092926000,
                        "orderPrice": 311500000,
                        "olineCustomerId": "20100053",
                        "orderStatus": 1,
                        "orderType": "OL_BAC",
                        "refundReason": "包装损坏，退货退货退货",
                        "refundType": "OL_BAC",
                        "shopCode": "11231507",
                        "sourceCode": "DFHD-20241231-001",
                        "origNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 2,
                        "supplierCode": "S00004158",
                        "updater": "王玮霞",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}",
                        "origPlatform": "抖音"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "adminAreaCode": "山东;青岛;市北区",
                        "contactAddr": "",
                        "contactName": "",
                        "contactPhone": "",
                        "contactTel": "",
                        "creator": "李鸿宾",
                        "buyer": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 136000000,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['perQty']),
                                "invalidDate": "2025-12",
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "productionBatch": f"{generate_number()}",
                                "productionDate": "2025-01",
                                "rowSupplierCode": "S00005889",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "sourceOutNo": "test-erp-out-20241230015",
                                "sourceDiscountAmount": "11240000",
                                "sourceAmount": "10240000",
                                "buyer": "lihongbin"
                            }
                        ],
                        "erpCreateTime": 1666074517000,
                        "erpUpdateTime": 1666092926000,
                        "orderPrice": 311500000,
                        "olineCustomerId": "20100053",
                        "orderStatus": 1,
                        "orderType": "OL_BAC",
                        "refundReason": "包装损坏，退货退货退货",
                        "refundType": "OL_BAC",
                        "shopCode": "11231507",
                        "sourceCode": "DFHD-20241231-001",
                        "origNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 2,
                        "supplierCode": "S00004158",
                        "updater": "王玮霞",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}",
                        "origPlatform": "抖音"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    try:
                        for sku_detail in sku_details:
                            dt_item = {
                                "amount": 136000000,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_detail['perQty']),
                                "invalidDate": "2025-12",
                                "mainUnit": f"{sku_detail['mainUnit']}",
                                "orderLineNo": 1,
                                "productionBatch": f"{generate_number()}",
                                "productionDate": "2025-01",
                                "rowSupplierCode": "S00005889",
                                "skuCode": f"{sku_detail['skuCode']}",
                                "sourceOutNo": "test-erp-out-20241230015",
                                "sourceDiscountAmount": "11240000",
                                "sourceAmount": "10240000",
                                "buyer": "lihongbin"
                            }
                            dt_list.append(dt_item)
                        dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                        data = {
                            "businessType": 0,
                            "companyCode": "50",
                            "adminAreaCode": "山东;青岛;市北区",
                            "contactAddr": "",
                            "contactName": "",
                            "contactPhone": "",
                            "contactTel": "",
                            "creator": "李鸿宾",
                            "buyer": "李鸿宾",
                            "dtList": dt_list,
                            "erpCreateTime": 1666074517000,
                            "erpUpdateTime": 1666092926000,
                            "orderPrice": 311500000,
                            "olineCustomerId": "20100053",
                            "orderStatus": 1,
                            "orderType": "OL_BAC",
                            "refundReason": "包装损坏，退货退货退货",
                            "refundType": "OL_BAC",
                            "shopCode": "11231507",
                            "sourceCode": "DFHD-20241231-001",
                            "origNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                            "origPurchaseOrderNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                            "origSys": "CQ_ERP",
                            "ownerCode": f"{owner_info['ownerCode']}",
                            "productFormType": "YP",
                            "splitNum": 2,
                            "supplierCode": "S00004158",
                            "updater": "王玮霞",
                            "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}",
                            "origPlatform": "抖音"
                        }
                        response = requests.post(url, json=data, headers=headers)
                        return response.json()
                    except Exception as e:
                        return str(e)
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 136000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "invalidDate": "2025-12",
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "productionBatch": f"{generate_number()}",
                            "productionDate": "2025-01",
                            "rowSupplierCode": "S00005889",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "sourceOutNo": "test-erp-out-20241230015",
                            "sourceDiscountAmount": "11240000",
                            "sourceAmount": "10240000",
                            "buyer": "lihongbin"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "adminAreaCode": "山东;青岛;市北区",
                        "contactAddr": "",
                        "contactName": "",
                        "contactPhone": "",
                        "contactTel": "",
                        "creator": "李鸿宾",
                        "buyer": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666074517000,
                        "erpUpdateTime": 1666092926000,
                        "orderPrice": 311500000,
                        "olineCustomerId": "20100053",
                        "orderStatus": 1,
                        "orderType": "OL_BAC",
                        "refundReason": "包装损坏，退货退货退货",
                        "refundType": "OL_BAC",
                        "shopCode": "11231507",
                        "sourceCode": "DFHD-20241231-001",
                        "origNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 2,
                        "supplierCode": "S00004158",
                        "updater": "王玮霞",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}",
                        "origPlatform": "抖音"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 136000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['perQty']),
                            "invalidDate": "2025-12",
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "productionBatch": f"{generate_number()}",
                            "productionDate": "2025-01",
                            "rowSupplierCode": "S00005889",
                            "skuCode": f"{sku_detail[0]['skuCode']}",
                            "sourceOutNo": "test-erp-out-20241230015",
                            "sourceDiscountAmount": "11240000",
                            "sourceAmount": "10240000",
                            "buyer": "lihongbin"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "adminAreaCode": "山东;青岛;市北区",
                        "contactAddr": "",
                        "contactName": "",
                        "contactPhone": "",
                        "contactTel": "",
                        "creator": "李鸿宾",
                        "buyer": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666074517000,
                        "erpUpdateTime": 1666092926000,
                        "orderPrice": 311500000,
                        "olineCustomerId": "20100053",
                        "orderStatus": 1,
                        "orderType": "OL_BAC",
                        "refundReason": "包装损坏，退货退货退货",
                        "refundType": "OL_BAC",
                        "shopCode": "11231507",
                        "sourceCode": "DFHD-20241231-001",
                        "origNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 2,
                        "supplierCode": "S00004158",
                        "updater": "王玮霞",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}",
                        "origPlatform": "抖音"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 136000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['perQty']),
                            "invalidDate": "2025-12",
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "productionBatch": f"{generate_number()}",
                            "productionDate": "2025-01",
                            "rowSupplierCode": "S00005889",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "sourceOutNo": "test-erp-out-20241230015",
                            "sourceDiscountAmount": "11240000",
                            "sourceAmount": "10240000",
                            "buyer": "lihongbin"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "adminAreaCode": "山东;青岛;市北区",
                        "contactAddr": "",
                        "contactName": "",
                        "contactPhone": "",
                        "contactTel": "",
                        "creator": "李鸿宾",
                        "buyer": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666074517000,
                        "erpUpdateTime": 1666092926000,
                        "orderPrice": 311500000,
                        "olineCustomerId": "20100053",
                        "orderStatus": 1,
                        "orderType": "OL_BAC",
                        "refundReason": "包装损坏，退货退货退货",
                        "refundType": "OL_BAC",
                        "shopCode": "11231507",
                        "sourceCode": "DFHD-20241231-001",
                        "origNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": f"wdtkth-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 2,
                        "supplierCode": "S00004158",
                        "updater": "王玮霞",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}",
                        "origPlatform": "抖音"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
    elif order_type == 'PFXSTHD':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 136000000,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['inOrderQty']) - 1,
                                "invalidDate": "2025-12",
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "productionBatch": f"{generate_number()}",
                                "productionDate": "2025-01",
                                "rowSupplierCode": "S00005889",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "sourceOutNo": "test-erp-out-20241230015",
                                "sourceDiscountAmount": "11240000",
                                "sourceAmount": "10240000",
                                "buyer": "lihongbin"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "PFTH",
                        "origNo": f"PFXSTHD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00015063",
                        "refundReason": "质量问题",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 136000000,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['inOrderQty']) - 1,
                                "invalidDate": "2025-12",
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "productionBatch": f"{generate_number()}",
                                "productionDate": "2025-01",
                                "rowSupplierCode": "S00005889",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "sourceOutNo": "test-erp-out-20241230015",
                                "sourceDiscountAmount": "11240000",
                                "sourceAmount": "10240000",
                                "buyer": "lihongbin"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "PFTH",
                        "origNo": f"PFXSTHD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00015063",
                        "refundReason": "质量问题",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 136000000,
                                "departmentCode": "N0028",
                                "inOrderQty": int(sku_details[0]['inOrderQty']),
                                "invalidDate": "2025-12",
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "productionBatch": f"{generate_number()}",
                                "productionDate": "2025-01",
                                "rowSupplierCode": "S00005889",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "sourceOutNo": "test-erp-out-20241230015",
                                "sourceDiscountAmount": "11240000",
                                "sourceAmount": "10240000",
                                "buyer": "lihongbin"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "PFTH",
                        "origNo": f"PFXSTHD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00015063",
                        "refundReason": "质量问题",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 136000000,
                                "departmentCode": "N0021",
                                "inOrderQty": int(sku_details[0]['inOrderQty']) - 1,
                                "invalidDate": "2025-12",
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "productionBatch": f"{generate_number()}",
                                "productionDate": "2025-01",
                                "rowSupplierCode": "S00005889",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "sourceOutNo": "test-erp-out-20241230015",
                                "sourceDiscountAmount": "11240000",
                                "sourceAmount": "10240000",
                                "buyer": "lihongbin"
                            }
                        ],
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "PFTH",
                        "origNo": f"PFXSTHD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00015063",
                        "refundReason": "质量问题",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 136000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['inOrderQty']),
                            "invalidDate": "2025-12",
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "productionBatch": f"{generate_number()}",
                            "productionDate": "2025-01",
                            "rowSupplierCode": "S00005889",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "sourceOutNo": "test-erp-out-20241230015",
                            "sourceDiscountAmount": "11240000",
                            "sourceAmount": "10240000",
                            "buyer": "lihongbin"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "PFTH",
                        "origNo": f"PFXSTHD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00015063",
                        "refundReason": "质量问题",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 136000000,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['inOrderQty']),
                            "invalidDate": "2025-12",
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "productionBatch": f"{generate_number()}",
                            "productionDate": "2025-01",
                            "rowSupplierCode": "S00005889",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "sourceOutNo": "test-erp-out-20241230015",
                            "sourceDiscountAmount": "11240000",
                            "sourceAmount": "10240000",
                            "buyer": "lihongbin"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "PFTH",
                        "origNo": f"PFXSTHD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00015063",
                        "refundReason": "质量问题",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 136000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['inOrderQty']),
                            "invalidDate": "2025-12",
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "productionBatch": f"{generate_number()}",
                            "productionDate": "2025-01",
                            "rowSupplierCode": "S00005889",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "sourceOutNo": "test-erp-out-20241230015",
                            "sourceDiscountAmount": "11240000",
                            "sourceAmount": "10240000",
                            "buyer": "lihongbin"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "PFTH",
                        "origNo": f"PFXSTHD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00015063",
                        "refundReason": "质量问题",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 136000000,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['inOrderQty']),
                            "invalidDate": "2025-12",
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "productionBatch": f"{generate_number()}",
                            "productionDate": "2025-01",
                            "rowSupplierCode": "S00005889",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "sourceOutNo": "test-erp-out-20241230015",
                            "sourceDiscountAmount": "11240000",
                            "sourceAmount": "10240000",
                            "buyer": "lihongbin"
                        }
                        dt_list.append(dt_item)
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1666662459000,
                        "erpUpdateTime": 1666663139000,
                        "orderPrice": 6800000000,
                        "orderStatus": 1,
                        "orderType": "PFTH",
                        "origNo": f"PFXSTHD-{generate_number()}-{random.randint(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "C00015063",
                        "refundReason": "质量问题",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
    elif order_type == 'YCRKD':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "creatorName": "李鸿宾",
                        "departmentCode": "N0028",
                        "dtList": [
                            {
                                "productBatch": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionBatch']}",
                                "productDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionDate']}",
                                "invalidDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['invalidDate']}",
                                "rowNo": 1,
                                "skuCode": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['skuCode']}",
                                "skuQty": 1,
                                "supplierCode": "S00004158",
                                "stockStatus": "HG"
                            }
                        ],
                        "erpCreateTime": "2021-10-01 11:30:00",
                        "erpUpdateTime": "2021-10-01 11:30:00",
                        "moveWhNo": f"YCRK-{generate_number()}-{random.randint(1, 9999)}",
                        "orderType": "NORMAL",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "remark": "",
                        "sourceWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "origSys": "CQ_ERP",
                        "status": 1,
                        "targetWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['target_code']}",
                        "updater": "3890",
                        "productFormType": "YP"
                    }
                    response = requests.post(url=f"{base_url}/oms/api/erp/moveWh/addOrUpdateMoveWh", json=data,
                                             headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "creatorName": "李鸿宾",
                        "departmentCode": "N0021",
                        "dtList": [
                            {
                                "productBatch": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['productionBatch']}",
                                "productDate": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['productionDate']}",
                                "invalidDate": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['invalidDate']}",
                                "rowNo": 1,
                                "skuCode": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['skuCode']}",
                                "skuQty": 1,
                                "supplierCode": "S00004158",
                                "stockStatus": "HG"
                            }
                        ],
                        "erpCreateTime": "2021-10-01 11:30:00",
                        "erpUpdateTime": "2021-10-01 11:30:00",
                        "moveWhNo": f"YCRK-{generate_number()}-{random.randint(1, 9999)}",
                        "orderType": "NORMAL",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "remark": "",
                        "sourceWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "origSys": "CQ_ERP",
                        "status": 1,
                        "targetWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['target_code']}",
                        "updater": "3890",
                        "productFormType": "YP"
                    }
                    response = requests.post(url=f"{base_url}/oms/api/erp/moveWh/addOrUpdateMoveWh", json=data,
                                             headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "creatorName": "李鸿宾",
                        "departmentCode": "N0028",
                        "dtList": [
                            {
                                "productBatch": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['productionBatch']}",
                                "productDate": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['productionDate']}",
                                "invalidDate": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['invalidDate']}",
                                "rowNo": 1,
                                "skuCode": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['skuCode']}",
                                "skuQty": 1,
                                "supplierCode": "S00004158",
                                "stockStatus": "HG"
                            }
                        ],
                        "erpCreateTime": "2021-10-01 11:30:00",
                        "erpUpdateTime": "2021-10-01 11:30:00",
                        "moveWhNo": f"YCRK-{generate_number()}-{random.randint(1, 9999)}",
                        "orderType": "NORMAL",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "remark": "",
                        "sourceWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "origSys": "CQ_ERP",
                        "status": 1,
                        "targetWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['target_code']}",
                        "updater": "3890",
                        "productFormType": "YP"
                    }
                    response = requests.post(url=f"{base_url}/oms/api/erp/moveWh/addOrUpdateMoveWh", json=data,
                                             headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "creatorName": "李鸿宾",
                        "departmentCode": "N0021",
                        "dtList": [
                            {
                                "productBatch": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['productionBatch']}",
                                "productDate": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['productionDate']}",
                                "invalidDate": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['invalidDate']}",
                                "rowNo": 1,
                                "skuCode": f"{get_warehouse_inventory(base_url, headers, owner_info)[0]['skuCode']}",
                                "skuQty": 1,
                                "supplierCode": "S00004158",
                                "stockStatus": "HG"
                            }
                        ],
                        "erpCreateTime": "2021-10-01 11:30:00",
                        "erpUpdateTime": "2021-10-01 11:30:00",
                        "moveWhNo": f"YCRK-{generate_number()}-{random.randint(1, 9999)}",
                        "orderType": "NORMAL",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "remark": "",
                        "sourceWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "origSys": "CQ_ERP",
                        "status": 1,
                        "targetWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['target_code']}",
                        "updater": "3890",
                        "productFormType": "YP"
                    }
                    response = requests.post(url=f"{base_url}/oms/api/erp/moveWh/addOrUpdateMoveWh", json=data,
                                             headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info):
                        if count >= 2:
                            break
                        dt_item = {
                            "productBatch": f"{sku_detail['productionBatch']}",
                            "productDate": f"{sku_detail['productionDate']}",
                            "invalidDate": f"{sku_detail['invalidDate']}",
                            "rowNo": 1,
                            "skuCode": f"{sku_detail['skuCode']}",
                            "skuQty": 1,
                            "supplierCode": "S00004158",
                            "stockStatus": "HG"
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "creatorName": "李鸿宾",
                        "departmentCode": "N0028",
                        "dtList": dt_list,
                        "erpCreateTime": "2021-10-01 11:30:00",
                        "erpUpdateTime": "2021-10-01 11:30:00",
                        "moveWhNo": f"YCRK-{generate_number()}-{random.randint(1, 9999)}",
                        "orderType": "NORMAL",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "remark": "",
                        "sourceWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "origSys": "CQ_ERP",
                        "status": 1,
                        "targetWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['target_code']}",
                        "updater": "3890",
                        "productFormType": "YP"
                    }
                    response = requests.post(url=f"{base_url}/oms/api/erp/moveWh/addOrUpdateMoveWh", json=data,
                                             headers=headers)
                    return response.json()
            elif owner_info['ownerCode'] == '01':
                dt_list = []
                count = 0
                for sku_detail in get_warehouse_inventory(base_url, headers, owner_info):
                    if count >= 2:
                        break
                    dt_item = {
                        "productBatch": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "skuQty": 1,
                        "supplierCode": "S00004158",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
                dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                data = {
                    "companyCode": "2",
                    "creator": "李鸿宾",
                    "creatorName": "李鸿宾",
                    "departmentCode": "N0021",
                    "dtList": dt_list,
                    "erpCreateTime": "2021-10-01 11:30:00",
                    "erpUpdateTime": "2021-10-01 11:30:00",
                    "moveWhNo": f"YCRK-{generate_number()}-{random.randint(1, 9999)}",
                    "orderType": "NORMAL",
                    "ownerCode": f"{owner_info['ownerCode']}",
                    "remark": "",
                    "sourceWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                    "origSys": "CQ_ERP",
                    "status": 1,
                    "targetWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['target_code']}",
                    "updater": "3890",
                    "productFormType": "YP"
                }
                response = requests.post(url=f"{base_url}/oms/api/erp/moveWh/addOrUpdateMoveWh", json=data,
                                         headers=headers)
                return response.json()
        elif is_whole_piece == 1:
            if owner_info['ownerCode'] == 'QDBYYYGF':
                dt_list = []
                count = 0
                for sku_detail in get_warehouse_inventory(base_url, headers, owner_info):
                    if count >= 2:
                        break
                    dt_item = {
                        "productBatch": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "skuQty": 1,
                        "supplierCode": "S00004158",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
                dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                data = {
                    "companyCode": "50",
                    "creator": "李鸿宾",
                    "creatorName": "李鸿宾",
                    "departmentCode": "N0028",
                    "dtList": dt_list,
                    "erpCreateTime": "2021-10-01 11:30:00",
                    "erpUpdateTime": "2021-10-01 11:30:00",
                    "moveWhNo": f"YCRK-{generate_number()}-{random.randint(1, 9999)}",
                    "orderType": "NORMAL",
                    "ownerCode": f"{owner_info['ownerCode']}",
                    "remark": "",
                    "sourceWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                    "origSys": "CQ_ERP",
                    "status": 1,
                    "targetWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['target_code']}",
                    "updater": "3890",
                    "productFormType": "YP"
                }
                response = requests.post(url=f"{base_url}/oms/api/erp/moveWh/addOrUpdateMoveWh", json=data,
                                         headers=headers)
                return response.json()
            elif owner_info['ownerCode'] == '01':
                dt_list = []
                count = 0
                for sku_detail in get_warehouse_inventory(base_url, headers, owner_info):
                    if count >= 2:
                        break
                    dt_item = {
                        "productBatch": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "skuQty": 1,
                        "supplierCode": "S00004158",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
                dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                data = {
                    "companyCode": "50",
                    "creator": "李鸿宾",
                    "creatorName": "李鸿宾",
                    "departmentCode": "N0028",
                    "dtList": dt_list,
                    "erpCreateTime": "2021-10-01 11:30:00",
                    "erpUpdateTime": "2021-10-01 11:30:00",
                    "moveWhNo": f"YCRK-{generate_number()}-{random.randint(1, 9999)}",
                    "orderType": "NORMAL",
                    "ownerCode": f"{owner_info['ownerCode']}",
                    "remark": "",
                    "sourceWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                    "origSys": "CQ_ERP",
                    "status": 1,
                    "targetWhCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['target_code']}",
                    "updater": "3890",
                    "productFormType": "YP"
                }
                response = requests.post(url=f"{base_url}/oms/api/erp/moveWh/addOrUpdateMoveWh", json=data,
                                         headers=headers)
                return response.json()
            else:
                return "ownerCode参数错误"
    elif order_type == 'DBRKD':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 10000000,
                                "departmentCode": "N0028",
                                "inOrderQty": 1,
                                "invalidDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['invalidDate']}",
                                "mainUnit": "罐",
                                "orderLineNo": 1,
                                "productionBatch": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionBatch']}",
                                "productionDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionDate']}",
                                "rowSupplierCode": "S00004158",
                                "skuCode": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['skuCode']}",
                            }
                        ],
                        "erpCreateTime": 1684981849000,
                        "erpUpdateTime": 1684981850000,
                        "orderPrice": 10000000,
                        "orderStatus": 1,
                        "orderType": "DBRK",
                        "origNo": f"DBRK-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBRK-241231-005",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "S00004158",
                        "updater": "刘春苗",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "outWarehouseName": "青岛仓"
                    }
                    response = requests.post(url, json=data,
                                             headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 10000000,
                                "departmentCode": "N0021",
                                "inOrderQty": 1,
                                "invalidDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['invalidDate']}",
                                "mainUnit": "罐",
                                "orderLineNo": 1,
                                "productionBatch": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionBatch']}",
                                "productionDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionDate']}",
                                "rowSupplierCode": "S00004158",
                                "skuCode": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['skuCode']}",
                            }
                        ],
                        "erpCreateTime": 1684981849000,
                        "erpUpdateTime": 1684981850000,
                        "orderPrice": 10000000,
                        "orderStatus": 1,
                        "orderType": "DBRK",
                        "origNo": f"DBRK-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBRK-241231-005",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "S00004158",
                        "updater": "刘春苗",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "outWarehouseName": "青岛仓"
                    }
                    response = requests.post(url, json=data,
                                             headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 10000000,
                                "departmentCode": "N0021",
                                "inOrderQty": 1,
                                "invalidDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['invalidDate']}",
                                "mainUnit": "罐",
                                "orderLineNo": 1,
                                "productionBatch": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionBatch']}",
                                "productionDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionDate']}",
                                "rowSupplierCode": "S00004158",
                                "skuCode": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['skuCode']}",
                            }
                        ],
                        "erpCreateTime": 1684981849000,
                        "erpUpdateTime": 1684981850000,
                        "orderPrice": 10000000,
                        "orderStatus": 1,
                        "orderType": "DBRK",
                        "origNo": f"DBRK-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBRK-241231-005",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "S00004158",
                        "updater": "刘春苗",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "outWarehouseName": "青岛仓"
                    }
                    response = requests.post(url, json=data,
                                             headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": [
                            {
                                "amount": 10000000,
                                "departmentCode": "N0021",
                                "inOrderQty": 1,
                                "invalidDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['invalidDate']}",
                                "mainUnit": "罐",
                                "orderLineNo": 1,
                                "productionBatch": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionBatch']}",
                                "productionDate": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['productionDate']}",
                                "rowSupplierCode": "S00004158",
                                "skuCode": f"{get_warehouse_inventory(base_url, headers, owner_info['ownerCode'])[0]['skuCode']}",
                            }
                        ],
                        "erpCreateTime": 1684981849000,
                        "erpUpdateTime": 1684981850000,
                        "orderPrice": 10000000,
                        "orderStatus": 1,
                        "orderType": "DBRK",
                        "origNo": f"DBRK-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBRK-241231-005",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "S00004158",
                        "updater": "刘春苗",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "outWarehouseName": "青岛仓"
                    }
                    response = requests.post(url, json=data,
                                             headers=headers)
                    return response.json()
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info):
                        if count >= 2:
                            break
                        dt_item = {
                            "amount": 10000000,
                            "departmentCode": "N0028",
                            "inOrderQty": 1,
                            "invalidDate": f"{sku_detail['invalidDate']}",
                            "mainUnit": "罐",
                            "orderLineNo": 1,
                            "productionBatch": f"{sku_detail['productionBatch']}",
                            "productionDate": f"{sku_detail['productionDate']}",
                            "rowSupplierCode": "S00004158",
                            "skuCode": f"{sku_detail['skuCode']}",
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1684981849000,
                        "erpUpdateTime": 1684981850000,
                        "orderPrice": 10000000,
                        "orderStatus": 1,
                        "orderType": "DBRK",
                        "origNo": f"DBRK-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBRK-241231-005",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "S00004158",
                        "updater": "刘春苗",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "outWarehouseName": "青岛仓"
                    }
                    response = requests.post(url, json=data,
                                             headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info):
                        if count >= 2:
                            break
                        dt_item = {
                            "amount": 10000000,
                            "departmentCode": "N0021",
                            "inOrderQty": 1,
                            "invalidDate": f"{sku_detail['invalidDate']}",
                            "mainUnit": "罐",
                            "orderLineNo": 1,
                            "productionBatch": f"{sku_detail['productionBatch']}",
                            "productionDate": f"{sku_detail['productionDate']}",
                            "rowSupplierCode": "S00004158",
                            "skuCode": f"{sku_detail['skuCode']}",
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1684981849000,
                        "erpUpdateTime": 1684981850000,
                        "orderPrice": 10000000,
                        "orderStatus": 1,
                        "orderType": "DBRK",
                        "origNo": f"DBRK-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBRK-241231-005",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "S00004158",
                        "updater": "刘春苗",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "outWarehouseName": "青岛仓"
                    }
                    response = requests.post(url, json=data,
                                             headers=headers)
                    return response.json()
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info):
                        if count >= 2:
                            break
                        dt_item = {
                            "amount": 10000000,
                            "departmentCode": "N0028",
                            "inOrderQty": 1,
                            "invalidDate": f"{sku_detail['invalidDate']}",
                            "mainUnit": "罐",
                            "orderLineNo": 1,
                            "productionBatch": f"{sku_detail['productionBatch']}",
                            "productionDate": f"{sku_detail['productionDate']}",
                            "rowSupplierCode": "S00004158",
                            "skuCode": f"{sku_detail['skuCode']}",
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "companyCode": "50",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1684981849000,
                        "erpUpdateTime": 1684981850000,
                        "orderPrice": 10000000,
                        "orderStatus": 1,
                        "orderType": "DBRK",
                        "origNo": f"DBRK-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBRK-241231-005",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "S00004158",
                        "updater": "刘春苗",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "outWarehouseName": "青岛仓"
                    }
                    response = requests.post(url, json=data,
                                             headers=headers)
                    return response.json()
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info):
                        if count >= 2:
                            break
                        dt_item = {
                            "amount": 10000000,
                            "departmentCode": "N0021",
                            "inOrderQty": 1,
                            "invalidDate": f"{sku_detail['invalidDate']}",
                            "mainUnit": "罐",
                            "orderLineNo": 1,
                            "productionBatch": f"{sku_detail['productionBatch']}",
                            "productionDate": f"{sku_detail['productionDate']}",
                            "rowSupplierCode": "S00004158",
                            "skuCode": f"{sku_detail['skuCode']}",
                        }
                        dt_list.append(dt_item)
                    dt_list[0]['inOrderQty'] = int(sku_details[0]['perQty']) - 1
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "dtList": dt_list,
                        "erpCreateTime": 1684981849000,
                        "erpUpdateTime": 1684981850000,
                        "orderPrice": 10000000,
                        "orderStatus": 1,
                        "orderType": "DBRK",
                        "origNo": f"DBRK-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBRK-241231-005",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "supplierCode": "S00004158",
                        "updater": "刘春苗",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name, order_type='YCRKD')['source_code']}",
                        "outWarehouseName": "青岛仓"
                    }
                    response = requests.post(url, json=data,
                                             headers=headers)
                    return response.json()

                else:
                    return "ownerCode参数错误"
