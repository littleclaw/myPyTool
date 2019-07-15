import getopt
import json
import re

import requests
from progressbar import *
from requests_toolbelt.multipart import encoder

server_url = "http://xyz.net:8000/file/upload"
update_url = "http://xyz.net:8000/app/update"
apk_info = {}
force_update = False
target = None
token = ""
widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
pbar = progressbar.ProgressBar(widgets=widgets)


def my_callback(monitor):
    pbar.update(monitor.bytes_read)
    if pbar.maxval == monitor.bytes_read:
        pbar.finish()
        print("上传到服务器完成，等待服务器上传至阿里云后返回下载链接...")


def getPreviousAppInfo():
    app_info_url = "http://xianzixun.net:8000/app/getApps?categoryId=2&top=1"
    print("访问原apk信息接口：" + app_info_url)
    resp = requests.get(app_info_url)
    print(resp.status_code, resp.text)
    resp_data = json.loads(resp.text)
    info = resp_data["data"]["apps"][0]
    apk_info.update(info)
    print("将接口得到的数据加入到字典中")
    print("------------------------------------------")


def authLogin():
    auth_data = {
        "name": "admin2",
        "password": "111111",
        "authAdminId": "111111111111",
    }
    print("以用户名%s,密码%s,登录" % (auth_data["name"], auth_data["password"]))
    login_url = "http://api.xianzixun.net/admin/login"
    login_resp = requests.post(login_url, data=auth_data, timeout=6)
    if login_resp.status_code == 200:
        print("login result: " + login_resp.text)
        login_result = login_resp.json()
        if login_result["code"] == 0:
            global token
            token = login_result["data"]["accessToken"]
            print("token设置成功")


def searchExtractApkVersionInfo():
    print("搜索脚本所在路径下所有的命名符合鲜资讯的apk...")
    file_list = os.listdir(os.path.split(os.path.realpath(__file__))[0])
    filtered_list = []
    for file_name in file_list:
        if re.match(r"^xianzixun_.*.apk$", file_name):
            filtered_list.append(file_name)
    if len(filtered_list) == 1:
        print(filtered_list[0])
        app_version = re.findall(r'^xianzixun.*_(.*)_([0-9]+).apk$', filtered_list[0])
        version_name, version_code = app_version[0]
        print("文件全名：{0}，分析出到的apk版本名：{1},版本号：{2}".format(filtered_list[0], version_name, version_code))
        apk_info["appVersion"] = version_name
        apk_info["versionCode"] = version_code
        print("更新apk_info中的版本名与版本号，更新后为" + json.dumps(apk_info))
        print("------------------------------------------")
        return filtered_list[0]
    elif len(filtered_list) > 1:
        print("符合命名规则的apk存在多个!")
        exit(0)
    else:
        print("符合规则的apk不存在!")
        exit(0)


def uploadFile(filename):
    e = encoder.MultipartEncoder(
        fields={'file': ('xianzixun.apk', open(filename, 'rb'), 'application/vnd.android.package-archive')})
    m = encoder.MultipartEncoderMonitor(e, my_callback)
    headers = {
        'Authorization': "Bearer" + token,
        'Referer': "http://xianzixun.net:8000/swagger-ui.html",
        'Origin': 'http://xianzixun.net:8000',
        'Content-Type': m.content_type}
    print("上传中...")
    pbar.maxval = m.len
    pbar.term_width = 60
    print("total len:" + str(m.len))
    pbar.start()
    resp = requests.post(server_url, data=m, headers=headers)

    print(resp.status_code, resp.text)
    down_url = json.loads(resp.text)["data"]
    print("更新apk_info中的下载链接...")
    apk_info["downUrl"] = down_url
    print("更新后apk_info:" + json.dumps(apk_info))
    print("------------------------------------------")
    return json.loads(resp.text)["data"]


def updateApkVersionInfo():
    apk_info["authAdminId"] = '1'
    headers = {
        'Authorization': "Bearer " + token,
        'Referer': "http://xianzixun.net:8000/swagger-ui.html",
        'Origin': 'http://xianzixun.net:8000'}
    print("更新后数据将变成：")
    print(apk_info)
    resp = requests.post(update_url, headers=headers, data=apk_info)
    print(resp.status_code, resp.text)
    if resp.status_code == 200:
        print("更新数据成功,再次查询服务端apk里数据……")
        getPreviousAppInfo()


def extract_args(argv):
    desc = None
    print("脚本所在路径：" + os.path.split(os.path.realpath(__file__))[0])
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    try:
        opts, args = getopt.getopt(argv[1:], "fhd:t:v", ['help', "desc=", "force", "target="])
    except getopt.GetoptError:
        print('usage: python tool.py -d description -f -t <apkPath>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('useage:设置更新描述，是否强制更新（默认为否） python tool.py -d <description> -d')
            sys.exit()
        elif opt in ("-d", "--desc"):
            desc = arg
        elif opt in ("-f", "--force"):
            global force_update
            force_update = True
        elif opt in ("-t", "--target"):
            global target
            target = arg
            pass

    if desc is not None:
        print("接收到的app更新描述为：" + desc)
        print("是否强制更新：" + str(force_update))
        print("目标路径：" + str(target))
    return desc


def extractApkInfoFromTarget():
    target_name = target.split('\\')[-1]
    app_version = re.findall(r'^xianzixun.*_(.*)_([0-9]+).apk$', target_name)
    version_name, version_code = app_version[0]
    print("文件路径：{0}，分析出到的apk版本名：{1},版本号：{2}".format(target, version_name, version_code))
    apk_info["appVersion"] = version_name
    apk_info["versionCode"] = version_code
    print("更新apk_info中的版本名与版本号，更新后为" + json.dumps(apk_info))
    print("------------------------------------------")


if __name__ == '__main__':
    authLogin()
    description = extract_args(sys.argv)
    getPreviousAppInfo()
    if target is not None:
        extractApkInfoFromTarget()
        print("上传文件路径：" + str(target))
        uploadFile(target)
    else:
        apk_name = searchExtractApkVersionInfo()
        apk_name = os.getcwd() + "\\" + apk_name
        print("上传文件路径：" + apk_name)
        uploadFile(apk_name)

    if description is not None:
        apk_info["updateDescribe"] = description
    if force_update is not None:
        apk_info["isMustUpdate"] = force_update
    print(apk_info)
    updateApkVersionInfo()
