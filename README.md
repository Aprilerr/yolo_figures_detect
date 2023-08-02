# YOLO FIGURE DETECT

## WHAT IS FIGURE DETECT

The code in this repository uses YOLO-based image recognition technology to detect and extract the figures and tables present in a research paper, and identifies the label text and relevant text in the paper for each figure and table.

## HOW TO USE

You can take advantage of this repository in two ways:

- terminal execute
- web server using fastapi

**terminal execute**

We recommend executing the process using the terminal.

First, download trained model using this link(yolov5x_publaynet_figure_800)[https://drive.google.com/file/d/1BnCZP4hwenl7DHqQc6R7wrtVwt8W_CLV/view], and put it into repo root path(`./yolo_figures_detect`)

Prepare Python environment , python version at least 3.9

```
pip install -r ./requirements.txt
```

Copy config_example.ini to config.ini.

Detect papers in folders

```
python runs.py ./test_file
```

Find results at config `OUT` path.

**web server using fastapi**

