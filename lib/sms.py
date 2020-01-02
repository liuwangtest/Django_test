import random

import requests
from django.core.cache import cache

from common.config import SMS_SENDSMS, MOBILE_NONE_SMS
from common.keys import VCODE_PREFIX


def send_sms(phone):
    print(f"send sms: {phone}")

    # 先生成一个4位的随机验证码
    vcode = random.randrange(1000, 9999)

    # 保存验证码：缓存
    VCODE = VCODE_PREFIX
    cache.set(f'{VCODE}{phone}', vcode)

    # 调用发短信api，发短信
    sms_api_url = SMS_SENDSMS

    sms_params = MOBILE_NONE_SMS

    sms_params["mobile"] = phone
    sms_params["param"] = f"{vcode}, 300"

    resp = requests.post(sms_api_url, json=sms_params)
    if resp.status_code == 200:
        result_json = resp.json()
        print(result_json)
        if result_json['code'] == '000000':
            return True, result_json['msg']
        else:
            print('由于此账号没有实名认证，发送失败')
            return False, result_json['msg']
    else:
        return False, '短信服务器错误'