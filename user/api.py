from lib.http import render_json
from common.keys import VCODE_PREFIX

from django.core.cache import cache
from social import settings

# Create your views here.
from lib.sms import send_sms
from user.logics import upload_qiniu
from user.models import User

import logging
inf_log = logging.getLogger('inf')

# 先经过 Session 中间件 process_request 处理
def user_phone(request):
    '''提交手机号，发送验证码'''
    phone = request.POST.get('phone')
    # phone = request.GET.get('phone')
    print(phone)
    send_sms(phone)
    inf_log.info('vcode: ' + str(phone))

    # return 之后会经过 Session 中间件的 process_response 处理
    return render_json(None)


def user_vcode(request):
    '''验证验证码'''
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    print(f'phone: {phone}')
    print(f'vcode: {vcode}')

    return render_json(verify_vcode(phone, vcode, request))


def verify_vcode(phone, vcode, request):
    # 取出缓存里保存的 vcode
    VCODE = VCODE_PREFIX
    server_vcode = cache.get(f'{VCODE}{phone}')

    print(f'server_vcode type:{type(server_vcode)}')
    print(f'vcode type:{type(vcode)}')

    # 比对两个 vocde 是否一致
    if str(server_vcode) == str(vcode):
        # 一致则让用户登录
        # get_or_create 返回的结构是一个 tuple，我们为了解包，用了 user, _
        # 统计是否新用户
        user, is_new_user = User.objects.get_or_create(phone=phone, nickname=phone)

        request.session['uid'] = user.id

        if is_new_user:
            # log 记录新用户
            inf_log.info('verify_new: ' + str(user.id))
        else:
            # log 记录登录用户
            inf_log.info('verify_old: ' + str(user.id))
        return user.to_dict()
    else:
        inf_log.info('verify_err: ' + str(phone))
        # 不一致则让用户重新登录:
        return {'vcode':10001}


def user_profile(request):
    return render_json(request.user.to_dict())


def user_avatar(request):
    # 上传后保存的文件名
    file_name = f'avatar-{request.user.id}'

    # 上传后保存的全路径
    file_path = f'{settings.BASE_DIR}/static/{file_name}'

    # 取得用户上传得图片
    f = request.FILES['avatar']

    # with 上下文管理器
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    print('save ok.')

    user_id = request.user.id
    # 将图片上传到七牛云
    # upload_qiniu(file_name, file_path, user_id)

    # 使用celery异步操作
    upload_qiniu.delay(file_name, file_path, user_id)

    return render_json(None)


