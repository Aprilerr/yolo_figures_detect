import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

# 指定要上传的文件路径
file_path = '/home/wsh/yolov5-master/test_file/New Dir Adult Contin Educ - 2023 - Wright - What is critical media literacy in an age of disinformation.pdf'

# 发送 POST 请求，并上传文件
response = requests.post('http://172.104.109.175:9080/', files={'file': open(file_path, 'rb')})

# 将响应内容以 JSON 格式返回
response_data = {
    'status_code': response.status_code,
    'headers': dict(response.headers),
    'text': response.text
}
    
payload = {
    'file': open(file_path,'rb'),
    'data': ('file_parse', json.dumps(response_data["text"]), 'application/json')
}


url = "http://localhost:8000/extract/with_parse"
file_parse = "abc"

encoder = MultipartEncoder(fields={
    "file_parse": response_data["text"],
    "file": ("file.pdf", open(file_path, "rb"), "application/pdf")
})

headers = {"Content-Type": encoder.content_type}
response_fig = requests.post(url, data=encoder, headers=headers)

print(response_fig.json())