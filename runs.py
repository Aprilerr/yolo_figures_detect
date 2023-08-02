import sys
import os
from pdf_to_image import pdf_to_image
from extract_figure import extract_figure
from extract_figures_info import extract_figure_info
import detect

def main(folder_path: str):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # list all files in the folder
        for filename in os.listdir(folder_path):
            main_with_file(os.path.join(folder_path,filename))
    else:
        print(f'{folder_path} does not exist or is not a folder.')    


def main_with_file(file_path):
    filename = os.path.basename(file_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        name_stem, name_suffix = os.path.splitext(filename)
        # pdf 转 image 图片，保存到 img_source_path 文件夹下，
        # image_source_path 为./data/path/name_str/images
        # root_path 为 ./data/path/name_str
        img_source_path, root_path = pdf_to_image(file_path)
        # figure检测，保存到 ./root_path/name_stem_detect_result 文件夹下, label文件夹保存figure的位置框信息
        detect.run(weights="yolov5x_publaynet_figure_800.pt", source=img_source_path, imgsz=(800, 640), save_txt=True, name=name_stem+"_detect_result", project=root_path)
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