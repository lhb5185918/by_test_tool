import json
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
        warehouse_code: 仓库代码
        skuCode - 商品编码
        skuName - 商品名称
        spec - 规格
        mainUnit - 单位
        usableQty - 可用库存
        packageAttrName - 包装规格
        mfg - 生产厂家
        approvalNumber - 批准文号
        productionBatch - 生产批号（手动添加的）
        productionDate - 生产日期（手动添加的）
        invalidDate - 有效期（手动添加的
        PIECE: 整件
        ZERO: 零货
        "perQty"
    """
    create_out_order_url = f"{base_url}/oms/api/erp/apiOutOrder/addOrUpdateOutOrder"
    dt_list = []
    if owner_info['ownerCode'] == 'QDBYYYGF':
        if order_type == 'PFXSD':
            for sku_detail in sku_details:
                if sku_detail['packageAttrName'] == '零货':
                    dt_item = {
                        "amount": 175000000,
                        "assignedLot": f"{sku_details['productionBatch']}",
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
                        "assignedLot": f"{sku_details['productionBatch']}",
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
                "warehouseCode": f"{get_warehouse_code(base_url, warehouse_id, warehouse_name)}",
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
            elif order_type == 'WHL':
    #
    # elif if owner_info['ownerCode'] == '01':
    #     pass
