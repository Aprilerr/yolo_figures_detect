# fastapi接口启动文档

# 接口目录
# 1. 输入pdf文件，输出pdf文件中的图片figure的oss link name、capture和文中的text
# 2. 输入解析完成的pdf数据以及pdf原文，输出pdf文件中的图片figure的oss link name、capture和文中的text

import os, shutil
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from extract_figure import extract_figure
from extract_figures_info import extract_figure_info
from pdf_to_image import pdf_to_image
from runs import main_with_file
from OSSUtils import upload_image
import detect,detect1

# For Inference Test
from models.common import DetectMultiBackend
from utils.general import check_img_size

imgsz=(640, 640)
model = DetectMultiBackend("yolov5x_publaynet_figure_800.pt")
stride, names, pt = model.stride, model.names, model.pt
imgsz = check_img_size(imgsz, s=stride)  # check image size
yolo5={"model":model,
       "stride":stride,
       "names":names,
       "pt":pt,
       "imgsz":imgsz}
######################################


class Paper_without_parse(BaseModel):
    paper: str

class Paper_with_parse(BaseModel):
    paper: str
    paper_parse: str

app = FastAPI()


# In this function, there is a process that call parse service
# Request this api, you will have risk with parse error
@app.post("/extract/without_parse")
async def extract_figure_without_parse(file: UploadFile = File(...)):
    contents = await file.read()
    file_name = os.path.basename(file.filename)
    with open(f"/tmp/{file_name}", "wb") as f:
        f.write(contents)
    main_with_file(f"/tmp/{file_name}",yolo5)
    file_path = f"/tmp/{file_name}"
    name_stem, name_suffix = os.path.splitext(file.filename)
    figures = []
    if os.path.exists(f"/tmp/{name_stem}/figures") and os.path.isdir(f"/tmp/{name_stem}/figures"):
        for outfile in [os.path.splitext(x)[0] for x in os.listdir(f"/tmp/{name_stem}/figures") if x.endswith('.png')]:
            figure = wrap_figure_info_with_oss(f"/tmp/{name_stem}/figures/" + outfile)
            figures.append(figure)
    shutil.rmtree(f'/tmp/{name_stem}')
    if os.path.exists(file_path):
        os.remove(file_path)
    return figures

# This function have no parse seveice requirement, you should call parse service firse 
# and transmit the result into this function params
@app.post("/extract/with_parse")
async def extract_figure_with_parse(file_parse:str = Form(...) ,file: UploadFile=File(...)):
    contents = await file.read()
    file_name = os.path.basename(file.filename)
    with open(f"/tmp/{file_name}", "wb") as f:
        f.write(contents)
    file_path = f"/tmp/{file_name}"
    filename = os.path.basename(file_path)
    name_stem, name_suffix = os.path.splitext(filename)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # pdf 转 image 图片，保存到 img_source_path 文件夹下，
        # image_source_path 为./data/path/name_str/images
        # root_path 为 ./data/path/name_str
        img_source_path, root_path = pdf_to_image(file_path)
        # figure检测，保存到 ./root_path/name_stem_detect_result 文件夹下, label文件夹保存figure的位置框信息
        # detect.run(weights="yolov5x_publaynet_figure_800.onnx", source=img_source_path, imgsz=(800, 640), save_txt=True, name=name_stem+"_detect_result", project=root_path)
        detect1.run(model=yolo5["model"],stride=yolo5["stride"],names=yolo5["names"],pt=yolo5["pt"],imgsz=yolo5["imgsz"],source=img_source_path,save_txt=True, name=name_stem+"_detect_result", project=root_path)
        # 找到figure的capture
        extract_figure(name_stem)
        # 根据capture找到文中的text，这里调用parse的接口
        extract_figure_info(name_stem, filename, file_parse)
    else: 
        print(f'{file_path} does not exist or is not a file.') 
    figures = []
    if os.path.exists(f"/tmp/{name_stem}/figures") and os.path.isdir(f"/tmp/{name_stem}/figures"):
        for outfile in [os.path.splitext(x)[0] for x in os.listdir(f"/tmp/{name_stem}/figures") if x.endswith('.png')]:
            figure = wrap_figure_info_with_oss(f"/tmp/{name_stem}/figures/" + outfile)
            figures.append(figure)
    shutil.rmtree(f'/tmp/{name_stem}')
    if os.path.exists(file_path):
        os.remove(file_path)
    return figures

@app.get("/hello")
def hello():
    return "hello world"


### Service

# 提供包装服务
# 1. 上传png图片到OSS端
# 2. 包装txt文件中的capture以及text到json
# 3. 将上述两个服务整合为一个服务，返回一个figure字典

def upload_to_oss(file_path: str):
    return upload_image(file_path)

def wrap_figure_info(file_path: str):
    if os.path.splitext(file_path)[1] != '.txt':
        raise Exception(f"{file_path} is not a txt file")
    with open(file_path, 'r') as f:
        lines = f.readlines()
        figure_info = {}
        figure_info["capture"] = lines[0]
        figure_info["text"] = lines[1:]
        return figure_info
    
def wrap_figure_info_with_oss(file_path: str):
    figure_info = wrap_figure_info(f"{file_path}.txt")
    figure_info["oss_name"] = upload_to_oss(f"{file_path}.png")
    return figure_info