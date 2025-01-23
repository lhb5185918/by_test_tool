from common import *
from create_out_order import *


def make_so_order(base_url, headers):
    out_order_data = read_yaml("out_order_data.yaml")
    erp_no = out_order_data["origNo"]
    out_order_id_url = f'{base_url}/wms/order/outOrder/pageInfo'
    out_order_data = {
        "createTimeFm": "2025-01-01 00:00:00",
        "erpOrderNo": f"{erp_no}",
        "orderByColumnList": None,
        "page": 1,
        "limit": 50
    }
    response = requests.post(out_order_id_url, json=out_order_data, headers=headers)
    write_yaml('out_order_data_list.yaml', response.json()['obj'][0])
    make_so_url = f'{base_url}/wms/order/outOrder/createSo'
    out_order_data_list = read_yaml('out_order_data_list.yaml')
    make_so_result = requests.post(make_so_url, json=[f'{out_order_data_list["id"]}'], headers=headers)
    return make_so_result.json()


def make_assign_order(base_url, headers):
    so_url = f'{base_url}/wms/ob/so/pageInfo'
    out_order_data_list = read_yaml('out_order_data.yaml')
    erp_no = out_order_data_list["origNo"]
    so_data = {
        "createTimeBegin": "2025-01-01 00:00:00",
        "cusOrderNo": f"{erp_no}",
        "orderByColumnList": [],
        "page": 1,
        "limit": 50
    }
    response = requests.post(so_url, json=so_data, headers=headers)
    write_yaml('so_data.yaml', response.json()['obj'][0])
    out_data = read_yaml('so_data.yaml')
    assign_order_url = f'{base_url}/wms/ob/soAssignment/doAssign'
    assign_response = requests.post(assign_order_url, json=[f'{out_data["id"]}'], headers=headers)
    return assign_response.json()


def make_wave_order(base_url, headers, is_seed):
    so_data = read_yaml('so_data.yaml')
    so_no = so_data['soNo']
    so_id = so_data['id']
    create_wave_url = f'{base_url}/wms/ob/waveIssued/manualCreateWaveOrder'
    if is_seed == 0:
        create_wave_data = {
            "soIdList": [
                f"{so_id}"
            ],
            "pickOrderLevel": 1,
            "zjPickMode": "ZJBB",
            "lhPickMode": "ZJBB",
            "isUrgent": False
        }
        create_wave_response = requests.post(create_wave_url, json=create_wave_data, headers=headers).json()
        if create_wave_response['msg'] == "成功":
            wave_id_url = f'{base_url}/wms/ob/waveOrder/pageInfo'
            wave_id_data = {
                "createTimeFm": "2025-01-01 00:00:00",
                "wmsBusinessType": None,
                "soNo": f"{so_no}",
                "orderByColumnList": [],
                "page": 1,
                "limit": 50
            }
            so_response = requests.post(wave_id_url, json=wave_id_data, headers=headers).json()['obj'][0]
            wave_url = f'{base_url}/wms/ob/waveIssued/waveOrderRelease'
            wave_data = {
                "idList": [
                    f"{so_response['id']}"
                ],
                "isEmptyStagingArea": False
            }
            wave_response = requests.post(wave_url, json=wave_data, headers=headers).json()
            return wave_response

    else:
        create_wave_data = {
            "soIdList": [
                f"{so_id}"
            ],
            "pickOrderLevel": 1,
            "zjPickMode": "XJHB",
            "lhPickMode": "XJHB",
            "isUrgent": False
        }
        create_wave_response = requests.post(create_wave_url, json=create_wave_data, headers=headers).json()
        if create_wave_response['msg'] == "成功":
            wave_id_url = f'{base_url}/wms/ob/waveOrder/pageInfo'
            wave_id_data = {
                "createTimeFm": "2025-01-01 00:00:00",
                "wmsBusinessType": None,
                "soNo": f"{so_no}",
                "orderByColumnList": [],
                "page": 1,
                "limit": 50
            }
            so_response = requests.post(wave_id_url, json=wave_id_data, headers=headers).json()['obj'][0]
            wave_url = f'{base_url}/wms/ob/waveIssued/waveOrderRelease'
            wave_data = {
                "idList": [
                    f"{so_response['id']}"
                ],
                "isEmptyStagingArea": False
            }
            wave_response = requests.post(wave_url, json=wave_data, headers=headers).json()
            return wave_response


def make_pick_order(base_url, headers, sku_details, username, user_no):
    """生成拣货单"""
    pick_order_id_url = f'{base_url}/wms/ob/pickOrder/pageInfo'
    pick_assign_url = f'{base_url}/wms/ob/pickOrder/pickAssignment'
    pick_task_id_url = f'{base_url}/wms/ob/pickTask/pageInfo'
    one_pick_url = f'{base_url}/wms/ob/pcPick/onekeyPic'

    # 获取拣货单信息
    pick_order_data = read_yaml('so_data.yaml')
    pick_order_no = pick_order_data['soNo']
    pick_order_id_data = {
        "createTimeFm": "2025-01-01 00:00:00",
        "soNo": f"{pick_order_no}",
        "orderByColumnList": [],
        "page": 1,
        "limit": 50
    }
    pick_order_response = requests.post(pick_order_id_url, json=pick_order_id_data, headers=headers).json()['obj'][0]

    responses = []  # 存储所有拣货任务的响应
    pick_data = {
        "pick_no": pick_order_response['pickOrderNo'],
        "lh_mission_ids": [],  # 存储零货任务ID
        "zj_mission_ids": [],  # 存储整件任务ID
        "lh_mission_pick_no": [],
        "zj_mission_pick_no": []
    }

    # 检查是否有零货商品
    has_loose_cargo = any(sku['packageType'] == '零货' for sku in sku_details)
    if has_loose_cargo:
        # 处理零货拣货
        pick_assign_data = {
            "userId": f"{get_user_info(base_url, headers, username, user_no)['id']}",
            "pickOrderId": f"{pick_order_response['id']}",
            "pickWay": "LH",
            "workMode": "RG"
        }
        pick_assign_response = requests.post(pick_assign_url, json=pick_assign_data, headers=headers).json()

        pick_task_id_data = {
            "createTimeFm": "2025-01-01 00:00:00",
            "pickOrderNo": f"{pick_order_response['pickOrderNo']}",
            "orderByColumnList": [],
            "page": 1,
            "limit": 50
        }
        pick_task_id_response = requests.post(pick_task_id_url, json=pick_task_id_data, headers=headers).json()['obj']

        for pick_task_mission in pick_task_id_response:
            if pick_task_mission['pickWay'] == "LH":
                one_pick_data = [f'{pick_task_mission["id"]}']
                response = requests.post(one_pick_url, json=one_pick_data, headers=headers).json()
                responses.append(response)
                pick_data['lh_mission_ids'].append(pick_task_mission['id'])
                pick_data['lh_mission_pick_no'].append(pick_task_mission['pickTaskNo'])

    # 检查是否有整件商品
    has_whole_piece = any(sku['packageType'] == '整件' for sku in sku_details)
    if has_whole_piece:
        # 处理整件拣货
        pick_assign_data = {
            "userId": f"{get_user_info(base_url, headers, username, user_no)['id']}",
            "pickOrderId": f"{pick_order_response['id']}",
            "pickWay": "ZJ",
            "workMode": "RG"
        }
        pick_assign_response = requests.post(pick_assign_url, json=pick_assign_data, headers=headers).json()

        pick_task_id_data = {
            "createTimeFm": "2025-01-01 00:00:00",
            "pickOrderNo": f"{pick_order_response['pickOrderNo']}",
            "orderByColumnList": [],
            "page": 1,
            "limit": 50
        }
        pick_task_id_response = requests.post(pick_task_id_url, json=pick_task_id_data, headers=headers).json()['obj']

        for pick_task_mission in pick_task_id_response:
            if pick_task_mission['pickWay'] == "ZJ":
                one_pick_data = [f'{pick_task_mission["id"]}']
                response = requests.post(one_pick_url, json=one_pick_data, headers=headers).json()
                responses.append(response)
                pick_data['zj_mission_ids'].append(pick_task_mission['id'])
                pick_data['zj_mission_pick_no'].append(pick_task_mission['pickTaskNo'])

    # 保存拣货单和任务ID信息
    write_yaml("pick_order_data.yaml", pick_data)

    # 返回所有拣货任务的响应
    return {
        'code': 200,
        'pick_order_no': pick_order_response['pickOrderNo'],
        'responses': responses
    }


def pick_order_down(base_url, headers, user_no, warehouse_id):
    """下架拣货任务"""
    pick_order = read_yaml('pick_order_data.yaml')  # 修正文件名
    pick_order_down_url = f"{base_url}/wms/ob/pcPick/onekeyPick"
    pick_order_down_data = []

    # 检查并添加零货任务ID
    if pick_order.get('lh_mission_ids') and len(pick_order['lh_mission_ids']) > 0:
        pick_order_down_data.extend(pick_order['lh_mission_ids'])

    # 检查并添加整件任务ID
    if pick_order.get('zj_mission_ids') and len(pick_order['zj_mission_ids']) > 0:
        pick_order_down_data.extend(pick_order['zj_mission_ids'])

    # 如果没有任何任务ID，返回错误
    if not pick_order_down_data:
        return {
            'code': 400,
            'msg': '没有找到可下架的拣货任务'
        }

    # 执行下架操作
    response = requests.post(pick_order_down_url, json=pick_order_down_data, headers=headers).json()
    res = response
    if response['code'] == 1000:
        websocket_response = reconnect_websocket(base_url, warehouse_id, user_no)
        if websocket_response['code'] == 200:
            response = requests.post(pick_order_down_url, json=pick_order_down_data, headers=headers).json()
            if response['code'] != 200:
                return {"error": "websocket重连失败，请退出工具，重新登录后重试"}
    return response


def bz_order_down(base_url, headers, sku_details):
    """播种单"""
    pick_mission_data = read_yaml('pick_order_data.yaml')
    responses = {
        'code': 200,
        'msg': '播种成功',
        'lh_responses': [],  # 存储零货播种响应
        'zj_responses': []  # 存储整件播种响应
    }

    try:
        # 处理零货播种
        has_loose_cargo = any(sku['packageType'] == '零货' for sku in sku_details)
        if has_loose_cargo and pick_mission_data.get('lh_mission_pick_no'):
            for sku_detail in sku_details:
                if sku_detail['packageType'] == '零货':
                    # 获取零货播种任务
                    get_bz_mission_url = f"{base_url}/wms/ob/sowInfoTob/pcLhScanPickTaskNo/{pick_mission_data['lh_mission_pick_no'][0]}"
                    get_bz_mission_response = requests.post(get_bz_mission_url, headers=headers).json()

                    if get_bz_mission_response.get('code') == 200:
                        # 执行零货播种
                        bz_order_url = f"{base_url}/wms/ob/sowInfoTob/pcLhScanSkuCode/{get_bz_mission_response['obj']['pickTaskId']}/{sku_detail['skuCode']}"
                        bz_order_response = requests.post(bz_order_url, headers=headers).json()
                        responses['lh_responses'].append({
                            'sku_code': sku_detail['skuCode'],
                            'response': bz_order_response
                        })

        # 处理整件播种
        has_whole_piece = any(sku['packageType'] == '整件' for sku in sku_details)
        if has_whole_piece and pick_mission_data.get('zj_mission_ids'):
            # 执行整件播种
            get_bz_mission_url = f"{base_url}/wms/ob/sowInfoTob/pcForceSow/{pick_mission_data['zj_mission_ids'][0]}"
            get_bz_mission_response = requests.post(get_bz_mission_url, headers=headers).json()
            responses['zj_responses'].append(get_bz_mission_response)

        # 检查播种结果
        if not responses['lh_responses'] and not responses['zj_responses']:
            return {
                'code': 400,
                'msg': '没有找到可播种的任务'
            }

        # 检查是否所有播种都成功
        all_success = True
        error_msgs = []

        # 检查零货播种结果
        for lh_resp in responses['lh_responses']:
            if lh_resp['response'].get('code') != 200:
                all_success = False
                error_msgs.append(f"零货商品 {lh_resp['sku_code']} 播种失败: {lh_resp['response'].get('msg')}")

        # 检查整件播种结果
        for zj_resp in responses['zj_responses']:
            if zj_resp.get('code') != 200:
                all_success = False
                error_msgs.append(f"整件播种失败: {zj_resp.get('msg')}")

        if not all_success:
            return {
                'code': 400,
                'msg': '播种部分失败',
                'errors': error_msgs,
                'responses': responses
            }

        return responses

    except Exception as e:
        return {
            'code': 500,
            'msg': f'播种异常: {str(e)}',
            'responses': responses
        }


def try_review_platform(base_url, headers, box_no):
    """尝试不同的复核台ID"""
    # 定义所有可能的复核台ID
    platform_ids = [
        1092414772990464,  # 默认复核台
        1252363905208832,  # 备用复核台1
        1092415203725824,  # 备用复核台2
        1092415533945344,  # 备用复核台3
        1092415805788672  # 备用复核台4
    ]

    init_review_data_url = f"{base_url}/wms/ob/review/b2b/initReviewData"

    # 依次尝试每个复核台ID
    for platform_id in platform_ids:
        init_review_data = {
            "checkPlatformId": platform_id,
            "platform": "PC",
            "boxNo": f"{box_no}"
        }

        response = requests.post(
            init_review_data_url,
            json=init_review_data,
            headers=headers
        ).json()

        # 如果成功，直接返回响应
        if response.get('code') == 200:
            return response

        # 如果不是复核台不匹配的错误，也返回响应
        if response.get('code') != 1000 and response.get('msg') != '复核台不匹配，请选择指定的复核台':
            return response

    # 如果所有复核台都尝试失败，返回最后一次的响应
    return response


def piece_order_review(base_url, headers, sku_details, is_drug):
    """零货复核"""
    type_mapping = {
        "FHD": "网店发货单",
        "CGTH": "采购退货通知单",
        "CGTHZP": "采购退货通知单(直配)",
        "CGZPTH": "赠品出库单",
        "PSD": "配送单",
        "PSDZP": "配送单(直配)",
        "PFXSD": "批发销售单",
        "YCCKD": "移仓出库单",
        "DBCKD": "调拨出库单",
        "LYCKD": "领样出库单"
    }
    pick_data = read_yaml('pick_order_data.yaml')
    for sku_detail in sku_details:
        if sku_detail['packageType'] == '零货':
            # 获取箱号
            box_no_url = f"{base_url}/wms/ob/pickTask/initUpdate/{pick_data['lh_mission_ids'][0]}"
            box_no_response = requests.post(box_no_url, headers=headers).json()
            box_no = box_no_response['obj']['sowDtList'][0]['boxNo']

            # 尝试初始化复核数据
            init_review_data_response = try_review_platform(base_url, headers, box_no)

            # 检查最终结果
            if init_review_data_response.get('code') != 200:
                return {
                    'code': init_review_data_response.get('code', 500),
                    'msg': f"初始化复核数据失败: {init_review_data_response.get('msg', '未知错误')}"
                }

            review_id = init_review_data_response['obj']['id']
            for dt_data in init_review_data_response['obj']['dtList']:
                if is_drug == 1:
                    scan_barcode_url = f"{base_url}/wms/drug/drugElectrSuperviseCodeCollection/scanBarcodeForReview"
                    scan_barcode_data = {
                        "originId": init_review_data_response['obj']['soId'],
                        "originNo": f"{init_review_data_response['obj']['cusOrderNo']}",
                        "originType": "OUT",
                        "skuCode": f"{sku_detail['skuCode']}",
                        "productionBatch": f"{sku_detail['productionBatch']}",
                        "reviewId": f"{review_id}"
                    }
                    scan_barcode_response = requests.post(scan_barcode_url, json=scan_barcode_data,
                                                          headers=headers).json()
                    for up_plat_form in scan_barcode_response['obj']['dtList']:
                        if up_plat_form['uploadPlatform'] == '101':

                            save_scan_url = f"{base_url}/wms/drug/drugElectrSuperviseCodeCollection/saveDrugSupervisionCode"
                            save_scan_data = {
                                "orderNo": f"[{review_id}]",
                                "ownerId": init_review_data_response['obj']['ownerId'],
                                "ownerName": None,
                                "originId": init_review_data_response['obj']['soId'],
                                "originNo": f"{init_review_data_response['obj']['cusOrderNo']}",
                                "orderType": f"{init_review_data_response['obj']['orderType']}",
                                "cooperativePartnerCode": "",
                                "cooperativePartnerName": "个人",
                                "originType": "OUT",
                                "dtList": init_review_data_response['obj']['dtList'],
                                "orderTypeName": type_mapping[f"{init_review_data_response['obj']['orderType']}"],
                                "shouldTaskCount": len(scan_barcode_response['obj']['dtList']),
                                "alreadyTaskCount": 0,
                                "isFinish": None,
                                "outBoxId": None,
                                "reviewId": f"{review_id}",
                                "whetherList": None,
                                "skuFlagSystemNameList": None,
                                "skuId": dt_data['commonSku']['skuId'],
                                "skuCode": f"{dt_data['skuCode']}",
                                "scannSkuCode": f"{dt_data['skuCode']}",
                                "productionBatch": f"{dt_data['commonInvBatch']['productionBatch']}",
                                "shouldGatherQty": 1,
                                "batchNo": up_plat_form['batchNo'],
                                "uploadPlatform": f"{up_plat_form['uploadPlatform']}",
                                "reviewType": "INNER",
                                "electrSuperviseCode": None,
                                "electrSuperviseCodeList": [
                                    "81181181118118118111"
                                ]
                            }
                            save_scan_response = requests.post(save_scan_url, json=save_scan_data,
                                                               headers=headers).json()
                            save_review_data = {
                                "id": f"{review_id}",
                                "barcode": f"{dt_data['skuCode']}",
                                "batchNo": f"{dt_data['commonInvBatch']['productionBatch']}",
                                "reviewQty": 1
                            }
                            save_review_data_url = f"{base_url}/wms/ob/review/b2b/saveReviewData"
                            save_review_data_response = requests.post(save_review_data_url, json=save_review_data,
                                                                      headers=headers).json()
                        elif up_plat_form['uploadPlatform'] == '102':

                            save_scan_url = f"{base_url}/wms/drug/drugElectrSuperviseCodeCollection/saveDrugSupervisionCode"
                            save_scan_data = {
                                "orderNo": f"[{review_id}]",
                                "ownerId": init_review_data_response['obj']['ownerId'],
                                "ownerName": None,
                                "originId": init_review_data_response['obj']['soId'],
                                "originNo": f"{init_review_data_response['obj']['cusOrderNo']}",
                                "orderType": f"{init_review_data_response['obj']['orderType']}",
                                "cooperativePartnerCode": "",
                                "cooperativePartnerName": "个人",
                                "originType": "OUT",
                                "dtList": init_review_data_response['obj']['dtList'],
                                "orderTypeName": type_mapping[f"{init_review_data_response['obj']['orderType']}"],
                                "shouldTaskCount": len(scan_barcode_response['obj']['dtList']),
                                "alreadyTaskCount": 0,
                                "isFinish": None,
                                "outBoxId": None,
                                "reviewId": f"{review_id}",
                                "whetherList": None,
                                "skuFlagSystemNameList": None,
                                "skuId": dt_data['commonSku']['skuId'],
                                "skuCode": f"{dt_data['skuCode']}",
                                "scannSkuCode": f"{dt_data['skuCode']}",
                                "productionBatch": f"{dt_data['commonInvBatch']['productionBatch']}",
                                "shouldGatherQty": 1,
                                "batchNo": up_plat_form['batchNo'],
                                "uploadPlatform": f"{up_plat_form['uploadPlatform']}",
                                "reviewType": "INNER",
                                "electrSuperviseCode": None,
                                "electrSuperviseCodeList": [
                                    "1"
                                ]
                            }
                            save_scan_response = requests.post(save_scan_url, json=save_scan_data,
                                                               headers=headers).json()
                            res = save_scan_response
                            save_review_data = {
                                "id": f"{review_id}",
                                "barcode": f"{dt_data['skuCode']}",
                                "batchNo": f"{dt_data['commonInvBatch']['productionBatch']}",
                                "reviewQty": 1
                            }
                            save_review_data_url = f"{base_url}/wms/ob/review/b2b/saveReviewData"
                            save_review_data_response = requests.post(save_review_data_url, json=save_review_data,
                                                                      headers=headers).json()
                        elif up_plat_form['uploadPlatform'] == 'WU':

                            save_scan_url = f"{base_url}/wms/drug/drugElectrSuperviseCodeCollection/saveDrugSupervisionCode"
                            save_scan_data = {
                                "orderNo": f"[{review_id}]",
                                "ownerId": init_review_data_response['obj']['ownerId'],
                                "ownerName": None,
                                "originId": init_review_data_response['obj']['soId'],
                                "originNo": f"{init_review_data_response['obj']['cusOrderNo']}",
                                "orderType": f"{init_review_data_response['obj']['orderType']}",
                                "cooperativePartnerCode": "",
                                "cooperativePartnerName": "个人",
                                "originType": "OUT",
                                "dtList": init_review_data_response['obj']['dtList'],
                                "orderTypeName": type_mapping[f"{init_review_data_response['obj']['orderType']}"],
                                "shouldTaskCount": len(scan_barcode_response['obj']['dtList']),
                                "alreadyTaskCount": 0,
                                "isFinish": None,
                                "outBoxId": None,
                                "reviewId": f"{review_id}",
                                "whetherList": None,
                                "skuFlagSystemNameList": None,
                                "skuId": dt_data['commonSku']['skuId'],
                                "skuCode": f"{dt_data['skuCode']}",
                                "scannSkuCode": f"{dt_data['skuCode']}",
                                "productionBatch": f"{dt_data['commonInvBatch']['productionBatch']}",
                                "shouldGatherQty": 1,
                                "batchNo": up_plat_form['batchNo'],
                                "uploadPlatform": f"{up_plat_form['uploadPlatform']}",
                                "reviewType": "INNER",
                                "electrSuperviseCode": None,
                                "electrSuperviseCodeList": [
                                    "q"
                                ]
                            }
                            save_scan_response = requests.post(save_scan_url, json=save_scan_data,
                                                               headers=headers).json()
                            res1 = save_scan_response
                            save_review_data = {
                                "id": f"{review_id}",
                                "barcode": f"{dt_data['skuCode']}",
                                "batchNo": f"{dt_data['commonInvBatch']['productionBatch']}",
                                "reviewQty": 1
                            }
                            save_review_data_url = f"{base_url}/wms/ob/review/b2b/saveReviewData"
                            save_review_data_response = requests.post(save_review_data_url, json=save_review_data,
                                                                      headers=headers).json()
                            res = save_scan_response

                        review_down_url = f"{base_url}/wms/ob/review/b2b/reviewDone"
                        review_down_data = {
                            "id": f"{review_id}",
                        }
                        review_down_response = requests.post(review_down_url, json=review_down_data,
                                                             headers=headers).json()
                        res = review_down_response
                else:
                    for dt_item in init_review_data_response['obj']['dtList']:
                        scan_code_url = f"{base_url}/wms/ob/review/b2b/scanCode"
                        scan_code_data = {
                            "id": f"{review_id}",
                            "barcode": f"{dt_item['skuCode']}",
                            "batchNo": f"{dt_item['commonInvBatch']['productionBatch']}",
                            "reviewQty": 1
                        }
                        scan_code_response = requests.post(scan_code_url, json=scan_code_data,
                                                           headers=headers).json()
                        save_review_url = f"{base_url}/wms/ob/review/b2b/saveReviewData"
                        save_review_data = {
                            "id": f"{review_id}",
                            "barcode": f"{scan_code_response['obj']['skuCode']}",
                            "batchNo": f"{scan_code_response['obj']['commonInvBatch']['productionBatch']}",
                            "reviewQty": 1
                        }
                        save_review_response = requests.post(save_review_url, json=save_review_data,
                                                             headers=headers).json()
                        res1 = save_review_response
                    review_down_url = f"{base_url}/wms/ob/review/b2b/reviewDone"
                    review_down_data = {
                        "id": f"{review_id}",
                    }
                    review_down_response = requests.post(review_down_url, json=review_down_data,
                                                         headers=headers).json()
                    res = review_down_response
                    return review_down_response
