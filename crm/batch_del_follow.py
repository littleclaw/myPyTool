import json

import requests
from requests.structures import CaseInsensitiveDict

url = "http://114.116.37.224/prod-api/"
login_url = url + "login"
follow_list_url = url + "crm/follow/list"
del_follow_url = url + "crm/follow/"
work_report_url = url + "work/report/list"

del_id_list = []

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["content-type"] = "application/json"
headers["Authorization"] = "Bearer"


def get_all_follow_list_count():
    follow_list_resp = requests.get(follow_list_url, headers=headers)
    if follow_list_resp.status_code == 200:
        print(follow_list_resp.json()["total"])
        # all_follow_list = follow_list_resp.json()["rows"]
        # for item in all_follow_list:
        #     print(item)


def del_follow_item(del_item_list):
    del_count = 0
    print("total item to be deleted:" + str(len(del_item_list)))
    for item in del_item_list:
        id2del = item
        print("id to del " + str(id2del))
        del_result = requests.delete(del_follow_url + str(id2del), headers=headers)
        if del_result.status_code == 200:
            print(del_result.json())
            del_count += 1
    print("del finished, del count :" + str(del_count))


def search_follow_list(append_id=False, filter_param=None):
    if filter_param is None:
        filter_param = {"content": "0分 0秒"}
    filter_list_resp = requests.get(follow_list_url, params=filter_param, headers=headers)
    if filter_list_resp.status_code == 200:
        print(filter_list_resp.json()["total"])
        for item in filter_list_resp.json()["rows"]:
            print(item)
            if append_id:
                del_id_list.append(item["id"])


def search_work_report_list(pageNum=1):
    filter_list_resp = requests.get(work_report_url, params={"type": 1, "time": "2022-04-19",
                                                             "pageNum": pageNum, "pageSize": 10}, headers=headers)
    if filter_list_resp.status_code == 200:
        print(filter_list_resp.request.url)
        print(filter_list_resp.json())


if __name__ == '__main__':
    print("login")
    data = {"username": "admin", "password": "admin123"}
    resp = requests.post(login_url, data=json.dumps(data), headers=headers)
    if resp.status_code == 200:
        print(resp.json())
        login_result = resp.json()
        headers["Authorization"] = "Bearer " + login_result["token"]
        get_all_follow_list_count()
        search_follow_list(True)
        # del_follow_item(del_id_list)
        # search_follow_list(False)
        # get_all_follow_list_count()
