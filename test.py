import requests
import copy


def get_token():
    url = "http://192.168.111.232:17777/oauth/password/unencrypted"
    data = {
        "userNo": "lhb001",
        "pwd": "lhx7758521",
        "platForm": "app",
        "companyCode": "ZHQC",
        "whId": 1,
        "warehouseId": "",
        "haveWarehouse": 1,
        "clientId": "iowtb-new",
        "userLanguage": "zh-CN"
    }
    res = requests.post(url=url, json=data, headers={'Content-Type': 'application/json'})
    token = res.json()['obj']['token']
    headers = {'Content-Type': 'application/json', 'Authorization': token}
    return headers


print(get_token())

select_sku_data_url = "http://192.168.111.232:17777/wms_232/sku/sku/pageInfo"
data = {
    "productFormType": "YP",
    "idStr": None,
    "mnemonicCode": None,
    "ownerId": None,
    "skuCategoryIds": [],
    "skuCodes": None,
    "mfgId": None,
    "permitHolder": None,
    "maintenanceType": None,
    "isEnable": None,
    "isDrugSuperCode": None,
    "isValidity": None,
    "isDoubleCheck": None,
    "isFirstCamp": None,
    "hasAnaleptic": None,
    "tempControlList": None,
    "drugForm": None,
    "page": 1,
    "limit": 50,
    "orderByColumnList": None
}
dt_list = []
dt_data = {
    "sourceProductionDateType": "1",
    "sourceInvalidDateType": "1",
    "skuId": "2087528556007936",
    "key": "2087528556007936",
    "companyCode": "ZHQC",
    "whId": 1,
    "id": "2087528556007936",
    "remark": "",
    "createTime": "2025-01-14 16:23:52",
    "creator": "lhb001",
    "creatorName": "李鸿宾",
    "updateTime": "2025-01-14 16:23:52",
    "updater": "lhb001",
    "updaterName": "李鸿宾",
    "createTimeStr": "2025-01-14 16:23:52",
    "updateTimeStr": "2025-01-14 16:23:52",
    "ownerId": 1770570116141568,
    "sysSkuCode": "SS25011400001",
    "skuCode": "M001",
    "skuName": "测试商品1",
    "origSys": "WMS",
    "spec": "50g",
    "ephedrine": 1,
    "tradeName": "测试商品1",
    "skuCategoryId": 1770467433878016,
    "brandName": "青岛单位",
    "barcode": "001",
    "mainUnit": "青岛单位",
    "length": 10,
    "width": 10,
    "height": 10,
    "vol": 1000,
    "grossWeight": 10,
    "netWeight": 10,
    "abc": "A",
    "zjAbc": "A",
    "mfgId": 1842209098174976,
    "mfg": "测试生产企业",
    "outFactoryCode": "",
    "model": "",
    "originCountry": "青岛单位",
    "logistics": "",
    "isBatchManage": 1,
    "isValidity": 0,
    "validityType": "",
    "validityDay": 0,
    "warmValidityDay": 15,
    "isValuables": 0,
    "isCombination": 0,
    "isGift": 0,
    "isConsumables": 0,
    "isChangeable": 0,
    "isProneToMistakes": 0,
    "isHeteromorphicProduct": 0,
    "perQty": 150,
    "midPackQty": 50,
    "isEnable": 1,
    "auditOpinion": None,
    "auditStatus": 1,
    "auditTime": None,
    "auditName": None,
    "barcodeTwo": "",
    "barcodeThree": "",
    "taxCode": "",
    "taxName": "",
    "taxFee": None,
    "tempControl": "CW",
    "scatteredProperties": "",
    "gmpCertNo": "GMP1",
    "approvalNumber": "国药准字批准文号1",
    "categoryPrincipal": "",
    "permitHolder": "",
    "qtyStandard": "",
    "mnemonicCode": None,
    "limitSaleDay": 30,
    "routeOfAdministration": None,
    "tempMax": None,
    "tempMin": None,
    "minInvoicingUnit": None,
    "optimistic": 0,
    "packFactoryId": 0,
    "productFormType": "YP",
    "isLimitMidPack": 1,
    "hasAnaleptic": 0,
    "tempCondition": None,
    "diCode": None,
    "erpUpdaterName": None,
    "erpUpdateTime": None,
    "erpCreatorName": None,
    "erpCreateTime": None,
    "creditType": None,
    "medicalInsuranceCode": None,
    "instrumentModel": None,
    "entrustMfgId": None,
    "hasAnalepticName": "否",
    "ephedrineName": "是",
    "isDoubleCheckName": "否",
    "isDoubleCheck": 0,
    "isFirstCamp": 0,
    "isFirstCampName": "否",
    "isLimitMidPackName": "是",
    "prodLicenseCode": None,
    "ownerCode": "ZHQCHZ",
    "ownerName": "智汇奇策科技有限公司",
    "skuCategoryName": "药品",
    "skuCategoryCode": None,
    "skuCategoryParentId": None,
    "productFormTypeName": "药品",
    "maintenanceType": "",
    "maintenanceTypeName": None,
    "skuCategorySecondId": None,
    "drugForm": "瓶",
    "drugFormSpec": "",
    "grmpCertificateNo": None,
    "grmpExpirationDate": "2030-01-31",
    "pzwhExpirationDate": None,
    "bomVOList": None,
    "consumablesVOList": None,
    "certificateVOList": None,
    "approvalNumberList": None,
    "gspData": None,
    "imageVOList": None,
    "packingVOList": None,
    "tempControlName": "常温",
    "isEnableName": "是",
    "scatteredPropertiesName": None,
    "packFactoryName": "",
    "entrustMfgName": "",
    "isValidityName": "否",
    "sumUsableQty": None,
    "auditStatusName": "已审核",
    "isDrugSuperCode": 0,
    "isDrugSuperCodeName": "否",
    "auditorTime": None,
    "orgId": "1770560509055488",
    "orgName": "零售事业部",
    "orgFullName": "智汇奇策科技有限公司_零售事业部",
    "supplierId": "1838234556355072",
    "supplierName": "青岛医药科技集团有限公司--智汇奇策科技有限公司",
    "inOrderQty": "100000.000",
    "amount": "100000.00",
    "unitPrice": "1.00",
    "sourceProductionDate": "2025-01",
    "sourceInvalidDate": "2025-12",
    "manageValidDay": "30",
    "sourceProductionBatch": "20250114001",
    "_X_ROW_KEY": "row_4098"
}

for i in requests.post(url=select_sku_data_url, json=data, headers=get_token()).json()['obj']:
    if "测试商品" in i['skuName']:
        # 创建 dt_data 的副本
        new_dt_data = copy.deepcopy(dt_data)
        new_dt_data['skuCode'] = i['skuCode']
        new_dt_data['skuName'] = i['skuName']
        new_dt_data['skuCategoryId'] = i['skuCategoryId']
        new_dt_data['tradeName'] = i['tradeName']
        new_dt_data['barcode'] = i['barcode']
        new_dt_data['skuId'] = i['id']
        new_dt_data['id'] = i['id']
        new_dt_data['key'] = i['id']
        new_dt_data['sysSkuCode'] = i['sysSkuCode']
        new_dt_data['skuCategoryId'] = i['skuCategoryId']
        dt_list.append(new_dt_data)
print(dt_list)
make_order_url = "http://192.168.111.232:17777/wms_232/order/inOrder/add"
make_order_data = {
    "origSys": "WMS",
    "orderStatus": "CJ",
    "jobType": "PTDD",
    "ownerName": "智汇奇策科技有限公司",
    "supplierName": "青岛医药科技集团有限公司--智汇奇策科技有限公司",
    "origNo": "test-20250114020",
    "orderType": "CGDD",
    "partnerType": "SUPPLIER",
    "supplierId": "1838234556355072",
    "customerId": None,
    "storeId": None,
    "ownerId": "1770570116141568",
    "productFormType": "YP",
    "dtReqList": dt_list,
    "extendReq": {
        "refundReason": None,
        "isSqueezed": 1
    }
}

print(requests.post(url=make_order_url, json=make_order_data, headers=get_token()).json())

