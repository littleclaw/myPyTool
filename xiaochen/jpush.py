import base64
import json

import requests

push_url = "https://api.jpush.cn/v3/push"
header = {"Content-Type": "application/json"}
appKey = "c48c0906e554f88ad914329b"
materSecret = "9b6082ef0c5d1ad5d6734da7"
authBytes = base64.b64encode((appKey + ":" + materSecret).encode('utf-8'))
authStr = authBytes.decode('utf-8')
header["Authorization"] = "Basic " + authStr
print(header)
msg = {
    "platform": "android",
    "audience": {
        "registration_id": ["160a3797c8f373355a2"]
    },
    "message": {
        "msg_content": "check",
        "content_type": "text",
        "title": "cmd",
        "extras": {"key": "value"}
    },
}

if __name__ == '__main__':
    resp = requests.post(push_url, data=json.dumps(msg), headers=header)
    if resp.status_code == 200:
        print(resp.text)
