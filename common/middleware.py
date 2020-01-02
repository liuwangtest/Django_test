
from django.utils.deprecation import MiddlewareMixin

from lib.http import render_json
from common import errors
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    # 这两个地址不做检查
    URL_WHITE_LIST = [
        '/api/user/phone',
        '/api/user/vcode',
    ]

    def process_request(self, request):
        # 如果当前 url 在白名单内，直接忽略
        if request.path in self.URL_WHITE_LIST:
            return

        # 检查用户是否登录
        uid = request.session.get('uid')
        if uid:
            try:
                request.user = User.objects.get(id=uid)
            except User.DoesNotExist:
                return render_json('用户不存在', errors.USER_NOT_EXIST)
        else:
            return render_json('用户未登录', errors.LOGIN_REQUIRED)
