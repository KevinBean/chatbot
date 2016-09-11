# -*- coding=utf-8 -*-
from flask import Blueprint

main = Blueprint('main', __name__)
# 通过实例化一个 Blueprint 类对象可以创建蓝本。 这个构造函数有两个必须指定的参数:
#  蓝本的名字和蓝本所在的包或模块。和程序一样,大多数情况下第二个参数使用 Python 的 __name__ 变量即可。

from . import views, errors
from ..models import Permission

# 这是定义模板上下文处理器(context processor), 这样你在模板中就可以访问 Permission 了.
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
