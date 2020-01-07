import logging

from common.errors import CODE_DISABLE_LIKE_SELF
from lib.http import render_json

from user.models import User
from swiper.models import Swiper
from swiper.models import Friend

inf_log = logging.getLogger('inf')


def swiper_users(request):
    # 准备一个要排除的用户id列表
    swipered_users = []

    # 拿到一组用户数据
    # swipered = Swiper.objects.filter(source_id=request.user.id).only('target_id')
    # print('+++++++++++++++', swipered)
    # print(type(swipered))
    # for swp in swipered:
    #     swipered_users.append(swp.target_id)
    swipered_users = Swiper.liked_me(request.user.id)
    # 把我自己放进去
    # swipered_users.append(request.user.id)

    # 暂时未使用推荐算法
    # users = User.objects.filter().exclude(id__in=swipered_users)[:20]
    users = User.objects.filter(id__in=swipered_users)
    # TODO:
    # 未来用 suprise 库做推荐算法。
    age_test = User.objects.filter(id=request.user.id)[0].age
    print('*****************', age_test)
    print(type(age_test))
    res_user = []
    for user in users:
        res_user.append(user.to_dict())

    return render_json(res_user)


# 喜欢的接口
def swiper_like(request):
    target_id = int(request.POST.get('target_id'))
    # source_id = int(request.POST.get('source_id'))
    source_id = request.user.id

    if target_id == source_id:
        return render_json({}, '禁止喜欢自己', CODE_DISABLE_LIKE_SELF)
    Swiper.swipe('like', source_id=source_id, target_id=target_id)

    # 检查被滑动者，是否喜欢过滑动者
    if Swiper.is_liked_someone(source_id=target_id, target_id=source_id):
        Friend.make_friends(target_id, source_id)

    return render_json(None)


# 超级喜欢的接口
def swiper_super_like(request):
    target_id = int(request.POST.get('target_id'))
    # source_id = int(request.POST.get('source_id'))
    source_id = request.user.id

    if target_id == source_id:
        return render_json({}, '禁止喜欢自己', CODE_DISABLE_LIKE_SELF)
    Swiper.swipe('superlike', source_id=source_id, target_id=target_id)

    # 检查被滑动者，是否喜欢过滑动者
    if Swiper.is_liked_someone(source_id=target_id, target_id=source_id):
        Friend.make_friends(target_id, source_id)

    return render_json(None)


# 不喜欢的接口
def swiper_unlike(request):
    target_id = int(request.POST.get('target_id'))
    # source_id = int(request.POST.get('source_id'))
    source_id = request.user.id

    if target_id == source_id:
        return render_json({}, '禁止操作自己', CODE_DISABLE_LIKE_SELF)
    Swiper.swipe('unlike', source_id=source_id, target_id=target_id)
    #
    # # 检查被滑动者，是否喜欢过滑动者
    # if Swiper.is_liked_someone(source_id=target_id, target_id=source_id):
    #     Friend.make_friends(target_id, source_id)

    return render_json(None)
