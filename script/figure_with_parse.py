import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

# 指定要上传的文件路径
file_path = '/home/wsh/yolov5-master/test_file/Global Networks - 2002 - Wimmer - Methodological nationalism and beyond  nation state building  migration and the social.pdf'

with open(file_path, "rb") as file:
    content = file.read()
    file_name = os.path.basename(file.name)

print(file_name)
# 发送 POST 请求，并上传文件
#response = requests.post('http://172.104.109.175:9080/', files={'file': open(file_path, 'rb')})
response = requests.post('http://172.104.109.175:9080/', files={'file': (file_name, content, "application/pdf")})

# 将响应内容以 JSON 格式返回
response_data = {
    'status_code': response.status_code,
    'text': response.text
}


url = "http://localhost:9000/extract/with_parse"

encoder = MultipartEncoder(fields={
    "file_parse": response_data["text"],
    "file": (file_name, content, "application/pdf")
})

headers = {"Content-Type": encoder.content_type}
response_fig = requests.post(url, data=encoder, headers=headers)

print(response_fig)