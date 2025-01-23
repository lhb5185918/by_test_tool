import requests
from common import *


def create_asn_order(base_url, headers, owner_info):
    erp_data = read_yaml('in_order_data.yaml')
    erp_no = erp_data['origNo']
    print(f"原始订单明细数量: {len(erp_data['dtList'])}")  # 添加调试信息

    # 获取入库单ID
    order_id_url = f"{base_url}/wms/order/inOrder/pageInfo"
    order_id_data = {
        "orderByColumnList": None,
        "createTimeFm": "2025-01-01 00:00:00",
        "tempControlList": [],
        "erpOrderNo": f"{erp_no}",
        "page": 1,
        "limit": 100  # 增加限制数量
    }
    print(requests.post(order_id_url, json=order_id_data, headers=headers).json())
    in_order_data_dict = requests.post(order_id_url, json=order_id_data, headers=headers).json()['obj'][0]

    # 获取待处理的入库单明细
    wait_order_url = f"{base_url}/wms/ib/rec/queryUserNotFinishRecInOrderDt"
    wait_order_data = {
        "inOrderId": in_order_data_dict['id']
    }
    wait_order_response = requests.post(wait_order_url, json=wait_order_data, headers=headers).json()
    print(f"待处理入库单响应: {wait_order_response}")  # 添加调试信息

    # 确保获取所有明细
    wait_order_data_list = wait_order_response.get('obj', [])
    if not isinstance(wait_order_data_list, list):
        wait_order_data_list = [wait_order_data_list]

    print(f"待处理明细数量: {len(wait_order_data_list)}")  # 添加调试信息

    # 确保待处理明细与原始订单明细数量一致
    if len(wait_order_data_list) != len(erp_data['dtList']):
        print("警告：待处理明细数量与原始订单明细数量不一致")
        # 构建完整的待处理明细列表
        complete_wait_order_list = []
        for dt in erp_data['dtList']:
            matching_item = next(
                (item for item in wait_order_data_list if item.get('skuCode') == dt['skuCode']),
                None
            )
            if matching_item:
                complete_wait_order_list.append(matching_item)
            else:
                # 如果找不到对应的待处理明细，创建一个新的
                new_item = {
                    'skuCode': dt['skuCode'],
                    'commodityQty': dt['inOrderQty'],
                    # 其他必要的字段...
                }
                complete_wait_order_list.append(new_item)
        wait_order_data_list = complete_wait_order_list

    # 更新每个商品的数量，与原始订单明细对应
    for i, wait_order_item in enumerate(wait_order_data_list):
        matching_dt = next(
            (dt for dt in erp_data['dtList'] if dt['skuCode'] == wait_order_item.get('skuCode')),
            None
        )
        if matching_dt:
            wait_order_item['commodityQty'] = matching_dt['inOrderQty']
            print(f"设置商品 {wait_order_item.get('skuCode')} 的数量为: {matching_dt['inOrderQty']}")  # 添加调试信息
        wait_order_item['_X_ROW_KEY'] = f"row_{1830 + i}"

    # 合并数据
    merged = in_order_data_dict.copy()
    merged['_X_ROW_KEY'] = "row_969"
    merged['dtList'] = wait_order_data_list

    print(f"最终处理的明细数量: {len(merged['dtList'])}")  # 添加调试信息

    # 生成验收单
    asn_url = f"{base_url}/wms/ib/rec/generateAsn"
    asn_result = requests.post(asn_url, json=merged, headers=headers).json()

    # 获取验收单详情
    select_asn_url = f"{base_url}/wms/ib/rec/scanOrderNo/{asn_result['obj']['asnNo']}"
    select_asn_result = requests.post(select_asn_url, headers=headers).json()
    select_asn_dict = select_asn_result['obj']

    # 设置收货时间和到达时间
    select_asn_dict['shipTime'] = f"{generate_date()}"
    select_asn_dict['arriveTime'] = f"{generate_date()}"

    # 添加检查状态
    select_asn_result_dict = add_check_status_to_wait_rec_list(select_asn_dict)
    select_asn_result_dict['dtList'] = select_asn_result_dict['waitRecList']

    # 保存验收单
    rec_save_url = f"{base_url}/wms/ib/rec/recSave"
    rec_save_result = requests.post(rec_save_url, json=select_asn_result_dict, headers=headers).json()
    res = rec_save_result
    if rec_save_result['code'] == 200:
        # 获取质检单信息
        ac_data_url = f"{base_url}/wms/ib/qc/pageInfo"
        qc_data_data = {
            "orderByColumnList": None,
            "createTimeFm": "2025-01-01",
            "skuCategoryIdList": [],
            "erpOrderNo": f"{erp_no}",
            "page": 1,
            "limit": 50
        }
        qc_data = requests.post(ac_data_url, json=qc_data_data, headers=headers).json()['obj'][0]
        write_yaml('qc_data.yaml', qc_data)

        return {"code": 200, "erp_no": erp_no, "asn_no": rec_save_result['obj']['asnNo'], "qc_no": qc_data['qcNo']}
    else:
        return rec_save_result


def make_put_shelf_data(base_url, headers, owner_info):
    qc_data = read_yaml('qc_data.yaml')
    receive_qc_url = f"{base_url}/wms/ib/qc/receiveTask"
    receive_qc_data = {
        "qcId": qc_data['id']
    }
    receive_qc_result = requests.post(receive_qc_url, json=receive_qc_data, headers=headers).json()
    qc_wait_data_url = f"{base_url}/wms/ib/qc/queryUserNotFinishQcDt"
    qc_wait_data_data = {
        "qcId": qc_data['id']
    }
    qc_wait_data = requests.post(qc_wait_data_url, json=qc_wait_data_data, headers=headers).json()
    qc_rec_data = add_check_status_to_wait_qc_list(qc_wait_data)['obj']['waitQcDtList']
    qc_save_url = f"{base_url}/wms/ib/qc/saveQc"
    qc_save_data = {
        "dtList": qc_rec_data,
        "qcId": qc_data['id'],
        "mac": "B0-7B-25-29-F7-04"
    }
    qc_save_result = requests.post(qc_save_url, json=qc_save_data, headers=headers).json()
    return qc_save_result


def put_shelf_down(base_url, headers, owner_info):
    erp_data = read_yaml('in_order_data.yaml')
    erp_no = erp_data['origNo']
    put_shelf_id_url = f"{base_url}/wms/ib/putShelf/pageInfo"
    put_shelf_id_data = {
        "orderByColumnList": None,
        "createTimeFm": "2025-01-01",
        "skuCategoryIdList": [],
        "erpOrderNo": f"{erp_no}",
        "page": 1,
        "limit": 50
    }
    put_shelf_result1 = requests.post(put_shelf_id_url, json=put_shelf_id_data, headers=headers).json()
    res = put_shelf_result1
    put_shelf_result = requests.post(put_shelf_id_url, json=put_shelf_id_data, headers=headers).json()['obj'][0]
    put_shelf_resave_url = f"{base_url}/wms/ib/putShelf/receiveTask"
    put_shelf_resave_data = {
        "putShelfId": put_shelf_result['id']
    }
    put_shelf_resave_result = requests.post(put_shelf_resave_url, json=put_shelf_resave_data, headers=headers).json()
    put_shelf_dt_url = f"{base_url}/wms/ib/putShelf/queryUserNotFinishPutShelfTaskDt"
    put_shelf_dt_data = {
        "putShelfId": put_shelf_result['id']
    }
    put_shelf_dt_result = requests.post(put_shelf_dt_url, json=put_shelf_dt_data, headers=headers).json()['obj']
    put_save_url = f"{base_url}/wms/ib/putShelf/savePutShelf"
    put_shelf_dt_result_dict = add_check_status_to_wait_put_list(put_shelf_dt_result)['waitPutShelfTaskDtList']
    put_save_data = {
        "dtList": put_shelf_dt_result_dict
    }
    put_save_data_result = requests.post(put_save_url, json=put_save_data, headers=headers).json()
    return put_save_data_result
