
import requests
import base64
from base64 import binascii
import json
import pathlib
import os


#阿里身份证OCR API

# def ocr(url,data):
#     head = {
#             'origin': 'https://data.aliyun.com',
#             'pragma':'no-cache',
#             'referer': 'https://data.aliyun.com/demo/ai/ocr',
#             'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
#         }
#     req = requests.post(url,data=data,headers=head)
#     return req.text


class AliOcr(object):

    def __init__(self,ocr_type:dict=None):
        self.api_name = {
            '身份证识别':'ocr_idcard',
            '驾驶证识别':'ocr_driver_license',
            '名片识别':'ocr_business_card',
            '营业执照识别':'ocr_business',
            '门牌识别':'ocr_shop_sign',
            '银行卡识别':'ocr_bank_card',
            '行驶证识别':'ocr_vehicle',
            '护照识别':'ocr_passport',
            '英文单词识别':'ocr_babel'
        }
        if ocr_type:
            self.api_name.update(ocr_type)

        self.api_body = {'service_code':'ocr','api_name':'','api_body':''}
        self.value = {'inputs':[{"image":{"dataType":50,"dataValue":""},"configure":{"dataType":50,"dataValue":'{"side":"face"}'}}]}

        self.head = {
            'origin': 'https://data.aliyun.com',
            'pragma':'no-cache',
            'referer': 'https://data.aliyun.com/demo/ai/ocr',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

        self.ocr_url = 'https://biz.data.aliyun.com/api/prod/requestAiService'
    
    def ocr_check(self,api_name,imgobj):
        try:
            base64.b64decode(imgobj)
            Flag = True
        except binascii.Error as e:
            # print(e)
            Flag = False
        if not Flag:
            fs = pathlib.Path(imgobj)
            if(fs.is_file()):
                with open(imgobj,'rb') as f:
                    ft = f.read()
                imgobj = base64.b64encode(ft)
                imgobj = imgobj.decode()
            else:
                return '错误的参数'

        self.api_body['api_name'] = self.api_name[api_name]
        self.value['inputs'][0]['image']['dataValue'] = imgobj
        self.api_body['api_body'] = json.dumps(self.value)

        req = requests.post(self.ocr_url,data=self.api_body,headers=self.head)
        return req.text


if __name__ == '__main__':

    ocr = AliOcr()
    # txt = ocr.ocr_check('身份证识别',r'C:\Users\jlds\Desktop\1P4020F057-35O-0.jpg')
    txt = ocr.ocr_check('驾驶证识别',r'C:\Users\jlds\Desktop\20150411125606283.jpg')
    # print(txt)

    jn = json.loads(txt)
    print(jn)


            
