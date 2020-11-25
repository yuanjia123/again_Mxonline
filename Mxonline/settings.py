

import os
#系统模块
#8

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print("-----------------",BASE_DIR)   打印----------------- D:\django框架\Message\muke_web_django\Mxonline  项目的当前位置

#表单验证的 SECRET_KEY
SECRET_KEY = 'wz5i)smd#9$5f9fo$^)&tc(%!!30@+2fz39ucu9%ewtfl9&_*@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #自己的app
    'apps.users.apps.UsersConfig',
    'apps.courses.apps.CoursesConfig',
    'apps.organizations.apps.OrganizationsConfig',
    'apps.operation.apps.OperationConfig',
    #xadmin 需要注册的app
    'crispy_forms',
    'xadmin.apps.XAdminConfig',
     #验证码需要注册的app
    'captcha',
    #分页
    'pure_pagination',
]

#中间键
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#路由
ROOT_URLCONF = 'Mxonline.urls'

#配置模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',

                #request.user.is_authenticated  这个主页里面、判断是否登录的上下文处理器、在任何模板页面当中都可以进行访问、（类似于flask）
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #这个是类似于flask上下文处理器的东西(把media的路径传递到每个模板 )  按住ctrl点击 'django.template.context_processors.media'的media里面会返回一个settings.MEDIA_URL
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'Mxonline.wsgi.application'


# 数据库连接信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "muke_web_mxonline",
        "USER":"root",
        "PASSWORD":"123456",
        "HOST":"127.0.0.1"
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    #用户输入密码的时候，作为验证
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


#继承django自带的用户类  第二步
AUTH_USER_MODEL = "users.UserProfile"

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

#staticfile 把静态文件(CSS、JS)拿出来、需要配置路径
STATICFILES_DIRS = [
    #"D:\django框架\message_third\static"
    os.path.join(BASE_DIR, 'static')
]


#云片网相关设置
yp_apikey = '92201394a24e2e320e7922eeaa76e498'

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

#把上传文件访问的Url前面都应该加上 这个/media/
MEDIA_URL = "/media/"
#上传的文件应该放在media文件下面
MEDIA_ROOT = os.path.join(BASE_DIR,"media")

#分页设置
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}