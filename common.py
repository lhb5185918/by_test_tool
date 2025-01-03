import requests
import time
from datetime import datetime


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


def get_sku_detail(base_url, headers, sku_code):
    """
    获取商品明细数据
    Args:
        base_url: 基础URL
        headers: 请求头
        sku_code: 商品编码
    Returns:
        dict: 商品明细数据
    """
    try:
        url = f"{base_url}/wms/sku/sku/pageInfo"
        data = {
            "productFormType": "YP",
            "skuCode": sku_code,
            "page": 1,
            "limit": 1,
            "orderByColumnList": None
        }
        response = requests.post(url, json=data, headers=headers)
        result = response.json()

        if result.get("code") == 200 and result.get("obj"):
            sku_detail = result["obj"][0]
            return {
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
        else:
            return {"error": f"获取商品明细失败: {result.get('msg', '未知错误')}"}

    except Exception as e:
        return {"error": f"获取商品明细失败: {str(e)}"}


def get_warehouse_code(base_url, warehouse_id):
    """获取仓库编码"""
    url = f"{base_url}/oauth/password/unencrypted"
    data = {"userNo": "lhb2", "pwd": "Lhx7758521!", "platForm": "Web", "companyCode": "QDBYYYGF", "whId": "",
            "warehouseId": "", "haveWarehouse": "0", "clientId": "zhqc-sso", "userLanguage": "zh-CN"}
    response = requests.post(url=url, json=data, headers={'Content-Type': 'application/json'})
    token = response.json().get('obj').get('token')
    headers = {'Content-Type': 'application/json', 'Authorization': token}
    select_warehouse_code_url = f"{base_url}/oms/base/whOrig/pageInfo"
    select_warehouse_code_data = {
        "whCode": "QDC",
        "orderByColumnList": None,
        "page": 1,
        "limit": 50
    }
    select_warehouse_code_response = requests.post(url=select_warehouse_code_url, json=select_warehouse_code_data,
                                                   headers=headers)
    for warehouse in select_warehouse_code_response.json()['obj']:
        if warehouse['whId'] == warehouse_id:
            return warehouse['origCode']
        else:
            return "未找到仓库编码"


def create_in_order(base_url, headers, order_type, owner_info, sku_details, is_whole_piece, is_mixed):
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
                                "inOrderQty": int(sku_details['preQty']) - 10,
                                "mainUnit": f"{sku_details['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details['skuCode']}",
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
                        "origNo": f"CGDD-erp-{generate_number}-{range(1, 9999)}",
                        "origPurchaseOrderNo": f"CGDD-erp-{generate_number}-{range(1, 9999)}",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "S00004158",
                        "updater": "李鸿宾",
                        "warehouseCode": "50001"
                    }
        elif order_type == 'CGDDZP':
            pass
