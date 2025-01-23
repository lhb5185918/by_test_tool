import requests
import time
from datetime import datetime
import random
from common import *


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
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    res = response.json()
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}"
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                else:
                    return "ownerCode参数错误"
    elif order_type == 'TCSQD':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,

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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "rowSupplierCode": "S00024188",
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "rowSupplierCode": "S00024188",
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                            "rowSupplierCode": "S00024188",
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                            "rowSupplierCode": "S00024188",
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                else:
                    return "ownerCode参数错误"
    elif order_type == 'TCSQDZP':
        if is_mixed == 0:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    data = {
                        "businessType": 0,

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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "rowSupplierCode": "S00024188",
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "rowSupplierCode": "S00024188",
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                            "rowSupplierCode": "S00024188",
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                            "rowSupplierCode": "S00024188",
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}",
                        "origPlatform": "抖音",
                        "isCrossBorderOrder": 0
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}",
                        "origPlatform": "抖音",
                        "isCrossBorderOrder": 0
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}",
                        "origPlatform": "抖音",
                        "isCrossBorderOrder": 0
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}",
                        "origPlatform": "抖音",
                        "isCrossBorderOrder": 0
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                            "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}",
                            "origPlatform": "抖音",
                            "isCrossBorderOrder": 0
                        }
                        response = requests.post(url, json=data, headers=headers)
                        write_yaml('in_order_data.yaml', data)
                        return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}",
                        "origPlatform": "抖音",
                        "isCrossBorderOrder": 0
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}",
                        "origPlatform": "抖音",
                        "isCrossBorderOrder": 0
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}",
                        "origPlatform": "抖音",
                        "isCrossBorderOrder": 0
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                elif owner_info['ownerCode'] == '01':
                    data = {
                        "businessType": 0,
                        "companyCode": "2",
                        "creator": "李鸿宾",
                        "creatorName": "李鸿宾",
                        "departmentCode": "N0021",
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
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                    res = data
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}

                else:
                    return "ownerCode参数错误"
    elif order_type == 'DBTCD':
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
                        "orderType": "DBTC",
                        "origNo": f"DBTC-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBTC-241231-005",
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "orderType": "DBTC",
                        "origNo": f"DBTC-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBTC-241231-005",
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "orderType": "DBTC",
                        "origNo": f"DBTC-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBTC-241231-005",
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                        "orderType": "DBTC",
                        "origNo": f"DBTC-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBTC-241231-005",
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                        "orderType": "DBTC",
                        "origNo": f"DBTC-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBTC-241231-005",
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                        "orderType": "DBTC",
                        "origNo": f"DBTC-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBTC-241231-005",
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                        "orderType": "DBTC",
                        "origNo": f"DBTC-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBTC-241231-005",
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    count = 0
                    for sku_detail in get_warehouse_inventory(base_url, headers, owner_info['ownerCode']):
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
                        "orderType": "DBTC",
                        "origNo": f"DBTC-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "DBTC-241231-005",
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
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}

                else:
                    return "ownerCode参数错误"
    elif order_type == 'LYTHD':
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
                                "inOrderQty": int(sku_details[0]['inOrderQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}",
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "LYTH",
                        "origNo": f"LYTH-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-20241231-006",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "C00084678",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "inOrderQty": int(sku_details[0]['inOrderQty']) - 1,
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024188",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}",
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "LYTH",
                        "origNo": f"LYTH-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-20241231-006",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "C00084678",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "inOrderQty": int(sku_details[0]['inOrderQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024171",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}",
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "LYTH",
                        "origNo": f"LYTH-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-20241231-006",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "C00084678",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
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
                                "inOrderQty": int(sku_details[0]['inOrderQty']),
                                "mainUnit": f"{sku_details[0]['mainUnit']}",
                                "orderLineNo": 1,
                                "rowSupplierCode": "S00024188",
                                "skuCode": f"{sku_details[0]['skuCode']}",
                                "productionDate": "2025-01",
                                "invalidDate": "2025-12",
                                "productionBatch": f"{generate_number()}",
                            }
                        ],
                        "erpCreateTime": 1666606057000,
                        "erpUpdateTime": 1666607051000,
                        "orderPrice": 738097330000,
                        "orderStatus": 1,
                        "orderType": "LYTH",
                        "origNo": f"LYTH-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-20241231-006",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "C00084678",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                else:
                    return "ownerCode参数错误"
        elif is_mixed == 1:
            if is_whole_piece == 0:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 16000.12,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['inOrderQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "rowSupplierCode": "S00024171",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "productionBatch": f"{generate_number()}",
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
                        "orderType": "LYTH",
                        "origNo": f"LYTH-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-20241231-006",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "C00084678",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 16000.12,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['inOrderQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "rowSupplierCode": "S00024188",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "productionBatch": f"{generate_number()}",
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
                        "orderType": "LYTH",
                        "origNo": f"LYTH-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-20241231-006",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "C00084678",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
            elif is_whole_piece == 1:
                if owner_info['ownerCode'] == 'QDBYYYGF':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 16000.12,
                            "departmentCode": "N0028",
                            "inOrderQty": int(sku_detail['inOrderQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "rowSupplierCode": "S00024171",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "productionBatch": f"{generate_number()}",
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
                        "orderType": "LYTH",
                        "origNo": f"LYTH-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-20241231-006",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "C00084678",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                elif owner_info['ownerCode'] == '01':
                    dt_list = []
                    for sku_detail in sku_details:
                        dt_item = {
                            "amount": 16000.12,
                            "departmentCode": "N0021",
                            "inOrderQty": int(sku_detail['inOrderQty']),
                            "mainUnit": f"{sku_detail['mainUnit']}",
                            "orderLineNo": 1,
                            "rowSupplierCode": "S00024188",
                            "skuCode": f"{sku_detail['skuCode']}",
                            "productionDate": "2025-01",
                            "invalidDate": "2025-12",
                            "productionBatch": f"{generate_number()}",
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
                        "orderType": "LYTH",
                        "origNo": f"LYTH-{generate_number()}-{random.randint(1, 9999)}",
                        "origPurchaseOrderNo": "CGDD-20241231-006",
                        "origSys": "CQ_ERP",
                        "ownerCode": f"{owner_info['ownerCode']}",
                        "productFormType": "YP",
                        "splitNum": 1,
                        "supplierCode": "C00084678",
                        "updater": "李鸿宾",
                        "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'], owner_info=owner_info)}"
                    }
                    response = requests.post(url, json=data, headers=headers)
                    write_yaml('in_order_data.yaml', data)
                    return {"result": response.json(), "order_no": f"{data['origNo']}"}
                else:
                    return "ownerCode参数错误"
