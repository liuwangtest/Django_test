from django.db import models
from django.db.models import Q

# Create your models here.

from django.db import models


class Swiper(models.Model):
    '''滑动模型'''
    TYPE = (
        ('like', '左滑喜欢'),
        ('superlike', '右滑超级喜欢'),
        ('unlike', '上滑不喜欢'),
    )

    source_id = models.IntegerField(verbose_name='滑动者')
    target_id = models.IntegerField(verbose_name='被滑者')
    type = models.CharField(max_length=20, choices=TYPE, verbose_name='滑动类型')
    s_time = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    @classmethod
    def swipe(cls, type, source_id, target_id):
        '''添加滑动记录'''
        # source_id 滑动者，target_id 被滑者
        return cls.objects.create(type=type, source_id=source_id, target_id=target_id)

    @classmethod
    def is_liked_someone(cls, source_id, target_id):
        '''检查是否喜欢过某人'''
        return cls.objects.filter(source_id=source_id, target_id=target_id,
                                  type__in=['like', 'superlike']).exists()

    # 喜欢我的用户列表
    @classmethod
    def liked_me(cls, target_id):
        uid_list = []
        # 找出所有划过我的人（且类型为 like 和 superlike），只取出他们的 uid
        swiped = cls.objects.filter(target_id=target_id, type__in=['like', 'superlike']).only('source_id')
        for swp in swiped:
            uid_list.append(swp.source_id)
        return uid_list


class Friend(models.Model):
    '''好友关系表'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''创建好友关系'''
        # 为了防止重复添加对 uid 排序：永远保证小的在前面，大的在后面
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        return cls.objects.get_or_create(uid1=uid1, uid2=uid2)

    @classmethod
    def friends_id_list(cls, uid):
        '''获取所有好友的 uid'''
        fid_list = []
        relations = cls.objects.filter(Q(uid1=uid) | Q(uid2=uid))
        for relation in relations:
            # 找出好友的 uid
            fid = relation.uid1 if relation.uid2 == uid else relation.uid2
            # 追加到好友的 fid_list 后边
            fid_list.append(fid)
        return fid_list

    @classmethod
    def break_off(cls, uid1, uid2):
        '''断交'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()
