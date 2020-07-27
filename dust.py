import apikey
import requests
import xml.etree.ElementTree as ET
import time
from requests.adapters import HTTPAdapter

service_key = apikey.air_api_key


def msrstn_query(res_dict):
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
    msrstn_list = []
    res_list = []
    for key, values in res_dict.items():
        for value in values:
            msrstn_list.append((key, value['stationName']))
            break

    for loc, msrstn in msrstn_list:
        time.sleep(1)
        body = {'ServiceKey': service_key, 'numOfRows': 100, 'pageNo': 1,
                'stationName': msrstn, 'dataTerm': 'DAILY', 'ver': "1.0"}
        res = requests.post(url, data=body, verify=False)
        # print(res.text)
        result = make_item_dict_list(res)
        if len(result) != 0:
            res_list.append({
                'location': loc,
                'weather_data': result[0]
            })
        else:
            pass
    return res_list


def make_item_dict_list(res):  # ./body/items xml을 dict로 바꾼다.
    tree = ET.fromstring(res.text)
    items_tag = tree.find('./body/items')
    item_list = []
    for item in items_tag:
        item_info = dict()
        for i in item:
            item_info[i.tag] = i.text
        item_list.append(item_info)
    # print(item_list)
    return item_list


def query_md(pos_dict):  # X,Y좌표가 담긴 json을 받아서 그 좌표에서 가까운 측정소들을 api를 통해 요청하고 결과를 json으로 반환하는 함수.
    msrstn_dict = dict()
    for item in pos_dict:
        time.sleep(1)
        location = f"{item['sidoName']} {item['sggName']} {item['umdName']}"
        pos_x, pos_y = map(float, (item['tmX'], item['tmY']))
        url = "http://openapi.airkorea.or.kr/openapi/services/rest/MsrstnInfoInqireSvc/getNearbyMsrstnList"
        body = {'ServiceKey': service_key, 'tmX': pos_x, 'tmY': pos_y}
        res = requests.post(url, data=body, verify=False)
        msrstn_dict[location] = make_item_dict_list(res)
    return msrstn_dict


def query_pos(dong, num=1):  # 지역 이름을 입력받아 해당 지역의 X,Y좌표를 api를 통해 요청하고 응답결과를 json으로 반환하는함수.
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/MsrstnInfoInqireSvc/getTMStdrCrdnt"
    body = {'ServiceKey': service_key, 'numOfRows': 100, 'pageNo': num, 'umdName': dong}
    s = requests.session()
    s.mount("http://", HTTPAdapter(max_retries=3))
    res = s.post(url, data=body, verify=False)
    return make_item_dict_list(res)


def result_dict_naming(res): # response에서 원하는 리스트만 새로 dict 만들어서 값을 등급으로 바꾸고 리턴한다.
    grade_list = {'-': None, '1': '좋음', '2': '보통', '3': '나쁨', '4': '매우 나쁨'}
    print_list = ['pm10Value', 'pm25Value', 'pm10Grade', 'pm25Grade']
    loc = res['location']
    weather_data_dict = res['weather_data']
    ret = dict()
    for weather_data in weather_data_dict:
        if weather_data in print_list:
            if 'Grade' in weather_data:
                if weather_data_dict[weather_data] == None:
                    ret[weather_data] = None
                else:
                    ret[weather_data] = grade_list[weather_data_dict[weather_data]]
            else:
                ret[weather_data] = weather_data_dict[weather_data]
    return {"location": loc, "weather_data": ret}


result = query_pos("원미구")
print(result)
print('-----------------')
print()
a = query_md(result)
print('-----------------')
query_result = msrstn_query(a)
print(query_result)
print('-------------')
for i in query_result:
    data = result_dict_naming(i)
    print(data['location'])
    for i in data['weather_data']:
        print(i, data['weather_data'][i])

# my_id = apikey.my_id
# my_pwd = apikey.my_pwd
# et_session = Everytime()
# res = et_session.login(my_id, my_pwd)
# print(res.text)
# for i in msrstn_query(a):
#     print(parse_result(i))
#     time.sleep(5)
#     a = make_string(parse_result(i))
#     et_session.write_article("\n".join(a), 428564)
