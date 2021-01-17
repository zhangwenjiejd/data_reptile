#!/usr/bin/python
# -*- coding: UTF-8 -*-
import base64
import os
import re
import time
import urllib
import uuid
from urllib.request import urlretrieve

from PIL import Image


def urllib_download(picName,imageUrl):
    os.makedirs('./image/', exist_ok=True)
    urlretrieve(imageUrl, './image/pic_'+picName+'.png')
    print('pic_'+picName+'.png')

def decode_base64(basedata,rootpath):

    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", basedata, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
    else:
        raise Exception("Do not parse!")
    # 2、base64解码
    img = base64.urlsafe_b64decode(data)
    # 3、二进制文件保存
    filename = rootpath+"/image/right/{}.{}".format(uuid.uuid4(), ext)
    with open(filename, "wb") as f:
        f.write(img)

    return filename


def imgUrl2Base64(url,filename,max_length=800):
    img=urllib.request.urlopen(url).read()
    base64_str = base64.b64encode(img).decode("utf-8")

    image_data = base64.b64decode(base64_str)

    with open(filename, 'wb') as f:
        f.write(image_data)
        f.close()
    return base64_str
    # return ""

def localPic2Base64(filename):
    with open(filename, 'rb') as f:
        base64_str = base64.b64encode(f.read()).decode("utf-8")
    return base64_str

def ResizeImage(filein, fileout, width, height, type):
    img = Image.open(filein)
    out = img.resize((width, height), Image.ANTIALIAS)
    out.save(fileout, type)


if __name__ == '__main__':

    imageUrl = "http://pin.aliyun.com/get_img?sessionid=ALIe2e338e188cb8712abdf753003977358&amp;identity=zhaoshang_sellermanager"
    for i in range(10000):
        urllib_download("2404"+str(i),imageUrl)
        time.sleep(0.5)

    # url = get_code()
    # base64 = imgUrl2Base64(url)
    # result = tencentBaseOcr(base64)
    # for str in result:
    #     if str['DetectedText'].strip():
    #         print(str['DetectedText'])
    #         break
