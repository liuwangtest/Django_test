import os

from celery import Celery

from worker import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social.settings")

# 创建 celery 的实例
celery_app = Celery('social')

# 配置来自 worker.config
celery_app.config_from_object(config)

# 自动发现任务
celery_app.autodiscover_tasks()
