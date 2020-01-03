'''
生成假数据用于测试（fake库）
由于此文件不涉及Django项目的整体运行，只是作为脚本来产生假数据
所以在初始化此文件的时候，要配置好 此文件的Django环境
'''

import os
import sys
import random

import django

# 设置环境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social.settings")
django.setup()

from user.models import User
from faker import Faker

fake = Faker(locale='zh_CN')


def gen_user(n):
    for i in range(n):
        try:
            gender = random.choice(['male', 'female'])
            if gender == 'male':
                name = fake.name_male()
            else:
                name = fake.name_female()
            phone = fake.phone_number()
            city = fake.province()
            # 将生成的假数据保存在数据库中
            User.objects.create(nickname=name, gender=gender, phone=phone, location=city)
            print(f'gen_user: {name}')
        except:
            pass


if __name__ == "__main__":
    # 生成5000条假数据
    gen_user(5000)
