#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import ssl

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models

def tencentBaseOcr(base64Str):
    try:
        cred = credential.Credential("AKIDNfmjlhVcxJg0ES5EjJvP0b9Whmt1q43K", "EpFUbaQ5atDZp9VgiZHtKZjqobEl7NaA")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        ssl._create_default_https_context = ssl._create_unverified_context

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

        req = models.GeneralBasicOCRRequest()
        params = '{"ImageBase64":"'+base64Str+'"}'
        req.from_json_string(params)

        resp = client.GeneralBasicOCR(req)
        js = json.loads(resp.to_json_string())
        return js["TextDetections"]

    except TencentCloudSDKException as err:
        print(err)


if __name__ == '__main__':
    str=''
    tencentBaseOcr(str)