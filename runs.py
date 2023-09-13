import sys
import os
from pdf_to_image import pdf_to_image
from extract_figure import extract_figure
from extract_figures_info import extract_figure_info
# import detect


# For Inference Test
import detect1,torch
from models.common import DetectMultiBackend
from utils.general import check_img_size
from utils.torch_utils import prune

# imgsz=(640, 640)#(800,640)inference时间长，（640，640）inference时间2073.0ms 
# model = DetectMultiBackend("yolov5x_publaynet_figure_800.onnx") #2667.7ms inference
# model=DetectMultiBackend("yolov5x_publaynet_figure_800.pt") #2741.1ms inference
# prune(model,0.3)
# model.eval()
# state={'epoch':-1,'best_fitness':None,'model':model,'ema': None, 'updates': None, 'optimizer': None, 'wandb_id': None,'date':'2022-11-07T00:48:30.526552'}
# torch.save(state,'prune_03.pt')

# stride, names, pt = model.stride, model.names, model.pt
# imgsz = check_img_size(imgsz, s=stride)  # check image size
# yolo5={"model":model,
#        "stride":stride,
#        "names":names,
#        "pt":pt,
#        "imgsz":imgsz}

def main(folder_path: str):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # list all files in the folder
        for filename in os.listdir(folder_path):
            main_with_file(os.path.join(folder_path,filename),yolo5)
    else:
        print(f'{folder_path} does not exist or is not a folder.')    


def main_with_file(file_path,yolo5):
    filename = os.path.basename(file_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        name_stem, name_suffix = os.path.splitext(filename)
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
        extract_figure_info(name_stem, filename)
    else: 
        print(f'{file_path} does not exist or is not a file.') 

if __name__ == "__main__":
    print("start running")
    folder_path = sys.argv[1]
    print(f"folder path: {folder_path}")
    main(folder_path)