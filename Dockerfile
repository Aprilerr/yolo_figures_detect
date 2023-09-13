FROM python:3.9-alpine

RUN apt-get update --fix-missing && apt-get install -y tesseract-ocr tesseract-ocr-osd poppler-utils libgl1
WORKDIR /app
COPY . .

RUN pip install -r ./requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

