import json
import random
import time
import requests
from datetime import datetime
from common import *


def create_out_order(base_url, headers, order_type, owner_info, sku_details, warehouse_id,
                     warehouse_name):
    """
    创建出库单
    Args:
        base_url: 基础URL
        headers: 请求头
        order_type: 订单类型
        owner_info: 货主信息字典，包含 origCompanyCode 和 ownerCode
        sku_details: 商品明细列表
        warehouse_id: 仓库ID
        warehouse_name: 仓库名称
    """
    create_out_order_url = f"{base_url}/oms/api/erp/apiOutOrder/addOrUpdateOutOrder"
    dt_list = []
    if owner_info['ownerCode'] == 'QDBYYYGF':
        if order_type == 'PFXSD':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "江苏省;南京市;玄武区",
                "businessDepartment": "销售支持部",
                "businessType": 0,
                "carrierCode": "CY002",
                "companyCode": "50",
                "confirmTime": 1666540800000,
                "contactAddr": "南京市江北新区华康路95号现代医药物流平台B幢一层、二层",
                "creator": "李鸿宾",
                "customerCode": "C00077671",
                "contactName": "李鸿宾",
                "contactTel": "17856546504",
                "customerType": "CUSTOMER",
                "departmentCode": "N0028",
                "discountPrice": 22480000,
                "dtList": dt_list,
                "erpCreateTime": 1666601238000,
                "erpUpdateTime": 1666601261000,
                "isPrintInvoice": 1,
                "orderPrice": 27200000000,
                "orderStatus": 1,
                "origNo": f"PFXS-{generate_number()}-{random.randint(1, 9999)}",
                "origSys": "CQ_ERP",
                "origType": "WHL",
                "ownerCode": f"{owner_info['ownerCode']}",
                "productFormType": "YP",
                "sellerRemark": "股份-品牌零售事业部",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}",
                "pickUpType": "TY",
                "invoiceTitle": "1",
                "invoiceType": "INVOICE",
                "isPrintUpstreamOrder": "1",
                "isPrintUpstreamInvoice": "1",
                "orderPrintType": "1",
                "businessManager": "wwx",
                "extendOne": "xiaowang",
                "buyerMsg": "销售支持部",
                "saleDepartmentCode": "",
                "saleZoneCode": "",
                "saleOfficeCode": "",
                "planShipDate": "2023-09-18 15:30:10",
                "invoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500",
                "arrivalStationContactName": "江西百洋",
                "arrivalStationContactTel": "18525647850",
                "arrivalStationProvince": "云南省",
                "arrivalStationCity": "昆明市",
                "arrivalStationArea": "安宁市",
                "extendSix": "云南省昆明市安宁市八街街道八街村",
                "payType": "转账",
                "buyerName": "李鸿宾"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
        elif order_type == 'FHD':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "辽宁省;大连市;金州区",
                "carrierCode": "CY002",
                "companyCode": "50",
                "confirmTime": 1668408850000,
                "contactAddr": "辽宁省大连市金州区 金石滩街道鲁能泰山7号2期168号菜鸟驿站",
                "contactName": "雅婷",
                "contactTel": "18888888888",
                "creator": "wwx",
                "customerCode": "11001413",
                "customerName": "百洋易美官方店",
                "customerType": "ONLINE_SHOP",
                "discountPrice": 898000000,
                "dtList": dt_list,
                "endCustomer": "BYDP-10190002",
                "erpCreateTime": 1668409157000,
                "erpUpdateTime": 1668409157000,
                "isPrintInvoice": 0,
                "orderPrice": 898000000,
                "orderStatus": 1,
                "origNo": f"WDFHD-{generate_number()}-{random.randint(1, 9999)}",
                "origSys": "CQ_ERP",
                "origType": "OL_PCK",
                "ownerCode": "QDBYYYGF",
                "payMethod": "在线支付",
                "pickUpType": "0",
                "purchName": "雅婷",
                "shopOrderNo": "20221114145410614268888",
                "sourceCode": "",
                "updater": "wwx",
                "productFormType": "YP",
                "departmentCode": "N0028",
                "businessType": 0,
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            res = response.json()
            write_yaml('out_order_data.yaml', data)

            return response.json()
        elif order_type == 'CGTH':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "上海;上海市;浦东新区",
                "businessDepartment": "采购部",
                "businessType": 0,
                "buyerName": "wwx",
                "carrierCode": "CY002",
                "companyCode": "50",
                "confirmTime": 1666713600000,
                "creator": "wwx",
                "customerCode": "S00004158",
                "customerName": "安斯泰来制药（中国）有限公司",
                "contactAddr": "浦东新区鹿顺路55号2幢、4幢、5幢1层（101室除外，其中冷库含蛋肽类）、2层、4层（其中特温库含蛋肽类）；宣竹路270、276号2幢1-3层、4层401室（第二类精神药品库）",
                "customerType": "SUPPLIER",
                "contactPhone": "18930867331",
                "contactName": "王玮霞",
                "departmentCode": "N0028",
                "discountPrice": 7950000000,
                'dtList': dt_list,
                "erpCreateTime": 1666780230000,
                "erpUpdateTime": 1666780355000,
                "isPrintInvoice": 0,
                "orderPrice": 7950000000,
                "orderStatus": 1,
                "origNo": f"CGTHSQ-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "REJ",
                "ownerCode": "QDBYYYGF",
                "productFormType": "YP",
                "sourceCode": "CGTHSQ-240902-0000005",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}",
                "rowSupplierCode": "C00084685",
                "pickUpType": "ZPS"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
        elif order_type == 'CGTHZP':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "山东省;青岛市;市北区",
                "businessDepartment": "采购部",
                "businessType": 0,
                "buyerName": "李鸿宾",
                "carrierCode": "CY002",
                "companyCode": "50",
                "confirmTime": 1666713600000,
                "creator": "wwx",
                "customerCode": "S00004158",
                "customerName": "安斯泰来制药（中国）有限公司",
                "customerType": "SUPPLIER",
                "departmentCode": "N0028",
                "discountPrice": 7950000000,
                'dtList': dt_list,
                "erpCreateTime": 1666780230000,
                "erpUpdateTime": 1666780355000,
                "isPrintInvoice": 0,
                "orderPrice": 7950000000,
                "orderStatus": 1,
                "origNo": f"CGTHSQ-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "PSO",
                "ownerCode": f"{owner_info['ownerCode']}",
                "productFormType": "YP",
                "sourceCode": "CGTHSQ-241231-000008",
                "updater": "王玮霞",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}",
                "rowSupplierCode": "S00004158"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
        elif order_type == 'CGZPTH':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "山东省;青岛市;市北区",
                "businessDepartment": "采购部",
                "businessType": 0,
                "buyerName": "wwx",
                "carrierCode": "CY002",
                "companyCode": "50",
                "confirmTime": 1666713600000,
                "creator": "wwx",
                "customerCode": "S00004158",
                "customerName": "安斯泰来制药（中国）有限公司",
                "customerType": "SUPPLIER",
                "departmentCode": "N0028",
                "discountPrice": 7950000000,
                'dtList': dt_list,
                "erpCreateTime": 1666780230000,
                "erpUpdateTime": 1666780355000,
                "isPrintInvoice": 0,
                "orderPrice": 7950000000,
                "orderStatus": 1,
                "origNo": f"CGTHSQ-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "PSO",
                "ownerCode": f"{owner_info['owberCode']}",
                "productFormType": "YP",
                "sourceCode": "CGTHSQ-241231-000008",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}",
                "rowSupplierCode": "S00004158"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
        elif order_type == 'PSD':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "陕西省；西安市；高新区",
                "businessDepartment": "健康连锁总部",
                "businessType": 0,
                "buyerMsg": "",
                "buyerRemark": "",
                "carrierCode": "CY016",
                "companyCode": "50",
                "confirmTime": 1668415379000,
                "contactAddr": "山东省青岛市莱西市青岛市南区延安三路101号",
                "contactName": "",
                "contactPhone": "",
                "contactTel": "",
                "creator": "李鸿宾",
                "customerCode": "DP2007",
                "customerName": "",
                "customerType": "SHOP",
                "departmentCode": "N0028",
                "discountPrice": 68724000000,
                'dtList': dt_list,
                "ecpOrderNo": "CGDD-240305-99993",
                "emailAddr": "",
                "endCustomer": "",
                "erpCreateTime": 1668415379000,
                "erpUpdateTime": 1668415383000,
                "invoiceTitle": "",
                "invoiceType": "",
                "isPrintInvoice": 0,
                "oaid": "",
                "orderPrice": 68724000000,
                "orderStatus": 1,
                "origNo": f"XSCK-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "ADD",
                "ownerCode": f"{owner_info['ownerCode']}",
                "payMethod": "",
                "pickUpType": "",
                "productFormType": "YP",
                "purchName": "",
                "sellerRemark": "",
                "shopOrderNo": "",
                "sourceCode": "",
                "taxIdNum": "",
                "taxType": "",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
        elif order_type == 'PSDZP':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}", }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "山东省;青岛市;市北区",
                "businessDepartment": "线上业务采购部",
                "businessType": 0,
                "buyerName": "李鸿宾",
                "carrierCode": "CY002",
                "companyCode": "50",
                "confirmTime": 1729241512000,
                "creator": "李鸿宾",
                "customerCode": "11001411",
                "customerName": "青岛百洋健康药房连锁有限公司市立西院便民药房",
                "customerType": "SHOP",
                "departmentCode": "N0028",
                "discountPrice": 162700000,
                'dtList': dt_list,
                "ecpOrderNo": "CGDD-erp-20241224007",
                "erpCreateTime": 1729233720000,
                "erpUpdateTime": 1729233722000,
                "isModifyPricePrint": 0,
                "isPrintInvoice": 0,
                "orderPrice": 162700000,
                "orderStatus": 1,
                "origNo": f"PSZPD-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "ADDZP",
                "ownerCode": f"{owner_info['ownerCode']}",
                "productFormType": "YP",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
    elif owner_info['ownerCode'] == '01':
        if order_type == 'PFXSD':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "江苏省;南京市;玄武区",
                "businessDepartment": "销售支持部",
                "businessType": 0,
                "carrierCode": "CY002",
                "companyCode": "2",
                "confirmTime": 1666540800000,
                "contactAddr": "南京市江北新区华康路95号现代医药物流平台B幢一层、二层",
                "creator": "李鸿宾",
                "customerCode": "C00077671",
                "contactName": "李鸿宾",
                "contactTel": "17856546504",
                "customerType": "CUSTOMER",
                "departmentCode": "N0021",
                "discountPrice": 22480000,
                "dtList": dt_list,
                "erpCreateTime": 1666601238000,
                "erpUpdateTime": 1666601261000,
                "isPrintInvoice": 1,
                "orderPrice": 27200000000,
                "orderStatus": 1,
                "origNo": f"PFXS-{generate_number()}-{random.randint(1, 9999)}",
                "origSys": "CQ_ERP",
                "origType": "WHL",
                "ownerCode": f"{owner_info['ownerCode']}",
                "productFormType": "YP",
                "sellerRemark": "股份-品牌零售事业部",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}",
                "pickUpType": "TY",
                "invoiceTitle": "1",
                "invoiceType": "INVOICE",
                "isPrintUpstreamOrder": "1",
                "isPrintUpstreamInvoice": "1",
                "orderPrintType": "1",
                "businessManager": "wwx",
                "extendOne": "xiaowang",
                "buyerMsg": "销售支持部",
                "saleDepartmentCode": "",
                "saleZoneCode": "",
                "saleOfficeCode": "",
                "planShipDate": "2023-09-18 15:30:10",
                "invoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500",
                "arrivalStationContactName": "江西百洋",
                "arrivalStationContactTel": "18525647850",
                "arrivalStationProvince": "云南省",
                "arrivalStationCity": "昆明市",
                "arrivalStationArea": "安宁市",
                "extendSix": "云南省昆明市安宁市八街街道八街村",
                "payType": "转账",
                "buyerName": "李鸿宾"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers).json()
            write_yaml('out_order_data.yaml', data)
            return response
        elif order_type == 'FHD':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "辽宁省;大连市;金州区",
                "carrierCode": "CY002",
                "companyCode": "2",
                "confirmTime": 1668408850000,
                "contactAddr": "辽宁省大连市金州区 金石滩街道鲁能泰山7号2期168号菜鸟驿站",
                "contactName": "雅婷",
                "contactTel": "18888888888",
                "creator": "wwx",
                "customerCode": "11001413",
                "customerName": "百洋易美官方店",
                "customerType": "ONLINE_SHOP",
                "discountPrice": 898000000,
                "dtList": dt_list,
                "endCustomer": "BYDP-10190002",
                "erpCreateTime": 1668409157000,
                "erpUpdateTime": 1668409157000,
                "isPrintInvoice": 0,
                "orderPrice": 898000000,
                "orderStatus": 1,
                "origNo": f"WDFHD-{generate_number()}-{random.randint(1, 9999)}",
                "origSys": "CQ_ERP",
                "origType": "OL_PCK",
                "ownerCode": "01",
                "payMethod": "在线支付",
                "pickUpType": "0",
                "purchName": "雅婷",
                "shopOrderNo": "20221114145410614268888",
                "sourceCode": "",
                "updater": "wwx",
                "productFormType": "YP",
                "departmentCode": "N0021",
                "businessType": 0,
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            write_yaml('out_order_data.yaml', data)
            return response.json()
        elif order_type == 'CGTH':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "上海;上海市;浦东新区",
                "businessDepartment": "采购部",
                "businessType": 0,
                "buyerName": "wwx",
                "carrierCode": "CY002",
                "companyCode": "2",
                "confirmTime": 1666713600000,
                "creator": "wwx",
                "customerCode": "S00004158",
                "customerName": "安斯泰来制药（中国）有限公司",
                "contactAddr": "浦东新区鹿顺路55号2幢、4幢、5幢1层（101室除外，其中冷库含蛋肽类）、2层、4层（其中特温库含蛋肽类）；宣竹路270、276号2幢1-3层、4层401室（第二类精神药品库）",
                "customerType": "SUPPLIER",
                "contactPhone": "18930867331",
                "contactName": "王玮霞",
                "departmentCode": "N0021",
                "discountPrice": 7950000000,
                'dtList': dt_list,
                "erpCreateTime": 1666780230000,
                "erpUpdateTime": 1666780355000,
                "isPrintInvoice": 0,
                "orderPrice": 7950000000,
                "orderStatus": 1,
                "origNo": f"CGTHSQ-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "REJ",
                "ownerCode": "01",
                "productFormType": "YP",
                "sourceCode": "CGTHSQ-240902-0000005",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}",
                "rowSupplierCode": "C00084685",
                "pickUpType": "ZPS"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            write_yaml('out_order_data.yaml', data)
            return response.json()
        elif order_type == 'CGTHZP':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "putTogetherNo": "",
                        "stockStatus": "HG",
                        "upstreamInvoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "山东省;青岛市;市北区",
                "businessDepartment": "采购部",
                "businessType": 0,
                "buyerName": "李鸿宾",
                "carrierCode": "CY002",
                "companyCode": "2",
                "confirmTime": 1666713600000,
                "creator": "wwx",
                "customerCode": "S00004158",
                "customerName": "安斯泰来制药（中国）有限公司",
                "customerType": "SUPPLIER",
                "departmentCode": "N0021",
                "discountPrice": 7950000000,
                'dtList': dt_list,
                "erpCreateTime": 1666780230000,
                "erpUpdateTime": 1666780355000,
                "isPrintInvoice": 0,
                "orderPrice": 7950000000,
                "orderStatus": 1,
                "origNo": f"CGTHSQ-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "PSO",
                "ownerCode": f"{owner_info['ownerCode']}",
                "productFormType": "YP",
                "sourceCode": "CGTHSQ-241231-000008",
                "updater": "王玮霞",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}",
                "rowSupplierCode": "S00004158"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
        elif order_type == 'CGZPTH':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "山东省;青岛市;市北区",
                "businessDepartment": "采购部",
                "businessType": 0,
                "buyerName": "wwx",
                "carrierCode": "CY002",
                "companyCode": "2",
                "confirmTime": 1666713600000,
                "creator": "wwx",
                "customerCode": "S00004158",
                "customerName": "安斯泰来制药（中国）有限公司",
                "customerType": "SUPPLIER",
                "departmentCode": "N0021",
                "discountPrice": 7950000000,
                'dtList': dt_list,
                "erpCreateTime": 1666780230000,
                "erpUpdateTime": 1666780355000,
                "isPrintInvoice": 0,
                "orderPrice": 7950000000,
                "orderStatus": 1,
                "origNo": f"CGTHSQ-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "PSO",
                "ownerCode": f"{owner_info['owberCode']}",
                "productFormType": "YP",
                "sourceCode": "CGTHSQ-241231-000008",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}",
                "rowSupplierCode": "S00004158"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
        elif order_type == 'PSD':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "discountAmount": 175000000,
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                        "stockStatus": "HG"
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "陕西省；西安市；高新区",
                "businessDepartment": "健康连锁总部",
                "businessType": 0,
                "buyerMsg": "",
                "buyerRemark": "",
                "carrierCode": "CY016",
                "companyCode": "2",
                "confirmTime": 1668415379000,
                "contactAddr": "山东省青岛市莱西市青岛市南区延安三路101号",
                "contactName": "",
                "contactPhone": "",
                "contactTel": "",
                "creator": "李鸿宾",
                "customerCode": "DP2007",
                "customerName": "",
                "customerType": "SHOP",
                "departmentCode": "N0021",
                "discountPrice": 68724000000,
                'dtList': dt_list,
                "ecpOrderNo": "CGDD-240305-99993",
                "emailAddr": "",
                "endCustomer": "",
                "erpCreateTime": 1668415379000,
                "erpUpdateTime": 1668415383000,
                "invoiceTitle": "",
                "invoiceType": "",
                "isPrintInvoice": 0,
                "oaid": "",
                "orderPrice": 68724000000,
                "orderStatus": 1,
                "origNo": f"XSCK-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "ADD",
                "ownerCode": f"{owner_info['ownerCode']}",
                "payMethod": "",
                "pickUpType": "",
                "productFormType": "YP",
                "purchName": "",
                "sellerRemark": "",
                "shopOrderNo": "",
                "sourceCode": "",
                "taxIdNum": "",
                "taxType": "",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
        elif order_type == 'PSDZP':
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": 1,
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}", }
                    dt_list.append(dt_item)
                else:
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_detail['productionBatch']}",
                        "productDate": f"{sku_detail['productionDate']}",
                        "invalidDate": f"{sku_detail['invalidDate']}",
                        "limitValid": 0,
                        "mainUnit": "盒",
                        "outOrderQty": sku_detail['perQty'],
                        "rowNo": 1,
                        "skuCode": f"{sku_detail['skuCode']}",
                    }
                    dt_list.append(dt_item)
            data = {
                "adminAreaCode": "山东省;青岛市;市北区",
                "businessDepartment": "线上业务采购部",
                "businessType": 0,
                "buyerName": "李鸿宾",
                "carrierCode": "CY002",
                "companyCode": "2",
                "confirmTime": 1729241512000,
                "creator": "李鸿宾",
                "customerCode": "11001411",
                "customerName": "青岛百洋健康药房连锁有限公司市立西院便民药房",
                "customerType": "SHOP",
                "departmentCode": "N0021",
                "discountPrice": 162700000,
                'dtList': dt_list,
                "ecpOrderNo": "CGDD-erp-20241224007",
                "erpCreateTime": 1729233720000,
                "erpUpdateTime": 1729233722000,
                "isModifyPricePrint": 0,
                "isPrintInvoice": 0,
                "orderPrice": 162700000,
                "orderStatus": 1,
                "origNo": f"PSZPD-{generate_number()}-{random.randint(1, 99999)}",
                "origSys": "CQ_ERP",
                "origType": "ADDZP",
                "ownerCode": f"{owner_info['ownerCode']}",
                "productFormType": "YP",
                "updater": "李鸿宾",
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, owner_info['ownerName'])}"
            }
            response = requests.post(create_out_order_url, json=data, headers=headers)
            write_yaml('out_order_data.yaml', data)

            return response.json()
