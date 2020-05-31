import json
import time

from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from rest_framework import exceptions
# Create your views here.
from rest_framework.views import APIView

from demo import models


def md5(user):
    import hashlib
    import time
    ctime = time.time()
    m = hashlib.md5()
    m.update(bytes(user.encode(encoding='UTF-8')))
    # 加盐
    m.update(bytes(int(ctime)))
    return m.hexdigest()


class MyAuth(object):
    def authenticate(self, request, *args, **kwargs):
        # 从被加工过的request对象中的原生request对象中取出token
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed("认证失败")

    def authenticate_header(self, arg):
        pass


class RestView(APIView):
    # authentication_classes = [MyAuth]

    def get(self, request):
        data = {"name": "haha"}
        return HttpResponse(json.dumps(data))

    def post(self, request):
        ret = {'code': "xxxx"}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['msg'] = "用户名密码错误"
            ret['code'] = 1000
            # 创建token
            token = make_password(user, salt='test', hasher='md5')

            # 存在就更新，不存在就创建，第一个参数为用户对象，第二个参数为key value形式的字典
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token.replace('md5','')
        except Exception as e:
            ret['code'] = 1002
        return JsonResponse(ret)
