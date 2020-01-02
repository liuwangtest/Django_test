from qiniu import Auth, put_file

from worker import celery_app

from user.models import User


@celery_app.task
def upload_qiniu(file_name, file_path, user_id):
    # 调用七牛云的 SDK 上传
    access_key = 'H-nVN0se7wqWSO1ek2CbVkwfTjQ8JIqFY8tFsU2x'
    secret_key = '6HlyNprKRMfN3wrW6zmg91Tltf0XMVNuUCWd7GOC'
    bucket_name = '202001'
    bucket_domain = 'q3glfqe07.bkt.clouddn.com'

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