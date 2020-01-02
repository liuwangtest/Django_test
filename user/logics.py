from qiniu import Auth, put_file

from worker import celery_app

from user.models import User


@celery_app.task
def upload_qiniu(file_name, file_path, user_id):
    # 调用七牛云的 SDK 上传
    access_key = 'cqxGEzAS6TSU_996r3svOLytJu1hQWU3Eb7oT3PM'
    secret_key = 'udaYEEpShey2UdioqDQuA9nACCKIeSqvQNccaja0'
    bucket_name = 'joker123'
    bucket_domain = 'q3h2ql4e2.bkt.clouddn.com'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, file_name, 3600)

    # 上传文件
    ret, info = put_file(token, file_name, file_path)
    print('upload ok.')

    # 更新用户的 avatar 字段
    avatar_url = f'{bucket_domain}/{file_name}'

    user = User.objects.get(id=user_id)
    user.avatar = avatar_url
    user.save()

    print('all done.')

    return True
