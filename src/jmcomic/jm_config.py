from common import time_stamp, str_to_list, field_cache, ProxyBuilder


def default_jm_logging(topic: str, msg: str):
    from common import format_ts
    print(f'{format_ts()}:【{topic}】{msg}')


def default_raise_exception_executor(msg, _extra):
    raise JmModuleConfig.CLASS_EXCEPTION(msg)


class JmcomicException(Exception):
    pass


# 禁漫常量
class JmMagicConstants:
    # 搜索参数-排序
    ORDER_BY_LATEST = 'mr'
    ORDER_BY_VIEW = 'mv'
    ORDER_BY_PICTURE = 'mp'
    ORDER_BY_LIKE = 'tf'

    ORDER_MONTH_RANKING = 'mv_m'
    ORDER_WEEK_RANKING = 'mv_w'
    ORDER_DAY_RANKING = 'mv_t'

    # 搜索参数-时间段
    TIME_TODAY = 't'
    TIME_WEEK = 'w'
    TIME_MONTH = 'm'
    TIME_ALL = 'a'

    # 全部, 同人, 单本, 短篇, 其他, 韩漫, 美漫, cosplay, 3D
    # category = ["0", "doujin", "single", "short", "another", "hanman", "meiman", "doujin_cosplay", "3D"]
    CATEGORY_ALL = '0'
    CATEGORY_DOUJIN = 'doujin'
    CATEGORY_SINGLE = 'single'
    CATEGORY_SHORT = 'short'
    CATEGORY_ANOTHER = 'another'
    CATEGORY_HANMAN = 'hanman'
    CATEGORY_MEIMAN = 'meiman'
    CATEGORY_DOUJIN_COSPLAY = 'doujin_cosplay'
    CATEGORY_3D = '3D'

    # 分页大小
    PAGE_SIZE_SEARCH = 80
    PAGE_SIZE_FAVORITE = 20

    # 图片分割参数
    SCRAMBLE_220980 = 220980
    SCRAMBLE_268850 = 268850
    SCRAMBLE_421926 = 421926  # 2023-02-08后改了图片切割算法

    # 当本子没有作者名字时，顶替作者名字
    DEFAULT_AUTHOR = 'default_author'

    # 移动端API密钥
    APP_TOKEN_SECRET = '18comicAPP'
    APP_TOKEN_SECRET_2 = '18comicAPPContent'
    APP_DATA_SECRET = '185Hcomic3PAPP7R'
    APP_VERSION = '1.6.4'
    APP_HEADERS_TEMPLATE = {
        'Accept-Encoding': 'gzip',
        'user-agent': 'Mozilla/5.0 (Linux; Android 9; V1938CT Build/PQ3A.190705.09211555; wv) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36',
    }

    # 网页端headers
    HTML_HEADERS_TEMPLATE = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                      'Safari/537.36',
    }


# 模块级别共用配置
class JmModuleConfig:
    # 网站相关
    PROT = "https://"
    JM_REDIRECT_URL = f'{PROT}jm365.work/3YeBdF'  # 永久網域，怕走失的小伙伴收藏起来
    JM_PUB_URL = f'{PROT}jmcomic.ltd'
    JM_CDN_IMAGE_URL_TEMPLATE = PROT + 'cdn-msp.{domain}/media/photos/{photo_id}/{index:05}{suffix}'  # index 从1开始
    JM_IMAGE_SUFFIX = ['.jpg', '.webp', '.png', '.gif']

    # JM的异常网页内容
    JM_ERROR_RESPONSE_TEXT = {
        "Could not connect to mysql! Please check your database settings!": "禁漫服务器内部报错",
        "Restricted Access!": "禁漫拒绝你所在ip地区的访问，你可以选择: 换域名/换代理",
    }

    # JM的异常网页code
    JM_ERROR_STATUS_CODE = {
        403: 'ip地区禁止访问/爬虫被识别',
        520: '520: Web server is returning an unknown error (禁漫服务器内部报错)',
        524: '524: The origin web server timed out responding to this request. (禁漫服务器处理超时)',
    }

    # 图片分隔相关
    SCRAMBLE_CACHE = {}

    # cookies，目前只在移动端使用，因为移动端请求接口须携带，但不会校验cookies的内容。
    APP_COOKIES = None

    # 移动端图片域名
    DOMAIN_IMAGE_LIST = str_to_list('''
    cdn-msp.jmapiproxy1.monster
    cdn-msp2.jmapiproxy1.monster
    cdn-msp.jmapiproxy1.cc
    cdn-msp.jmapiproxy2.cc
    cdn-msp.jmapiproxy3.cc
    cdn-msp.jmapiproxy4.cc

    ''')

    # 移动端API域名
    DOMAIN_API_LIST = str_to_list('''
    www.jmapinode1.top
    www.jmapinode2.top
    www.jmapinode3.top
    www.jmapinode.biz
    www.jmapinode.top
    
    ''')

    # 网页端域名配置
    # 无需配置，默认为None，需要的时候会发起请求获得
    # 使用优先级:
    # 1. DOMAIN_HTML_LIST
    # 2. [DOMAIN_HTML]
    DOMAIN_HTML = None
    DOMAIN_HTML_LIST = None

    # 模块级别的可重写类配置
    CLASS_DOWNLOADER = None
    CLASS_OPTION = None
    CLASS_ALBUM = None
    CLASS_PHOTO = None
    CLASS_IMAGE = None
    CLASS_EXCEPTION = JmcomicException
    # 客户端注册表
    REGISTRY_CLIENT = {}
    # 插件注册表
    REGISTRY_PLUGIN = {}

    # 执行log的函数
    executor_log = default_jm_logging
    # 网页正则表达式解析失败时，执行抛出异常的函数，可以替换掉用于log
    executor_raise_exception = default_raise_exception_executor

    # 使用固定时间戳
    flag_use_fix_timestamp = True
    # 移动端Client初始化cookies
    flag_api_client_require_cookies = True
    # log开关标记
    flag_enable_jm_log = True
    # log时解码url
    flag_decode_url_when_logging = True
    # 当内置的版本号落后时，使用最新的禁漫app版本号
    flag_use_version_newer_if_behind = False

    # 关联dir_rule的自定义字段与对应的处理函数
    # 例如:
    # Amyname -> JmModuleConfig.AFIELD_ADVICE['myname'] = lambda album: "自定义名称"
    AFIELD_ADVICE = dict()
    PFIELD_ADVICE = dict()

    @classmethod
    def downloader_class(cls):
        if cls.CLASS_DOWNLOADER is not None:
            return cls.CLASS_DOWNLOADER

        from .jm_downloader import JmDownloader
        return JmDownloader

    @classmethod
    def option_class(cls):
        if cls.CLASS_OPTION is not None:
            return cls.CLASS_OPTION

        from .jm_option import JmOption
        return JmOption

    @classmethod
    def album_class(cls):
        if cls.CLASS_ALBUM is not None:
            return cls.CLASS_ALBUM

        from .jm_entity import JmAlbumDetail
        return JmAlbumDetail

    @classmethod
    def photo_class(cls):
        if cls.CLASS_PHOTO is not None:
            return cls.CLASS_PHOTO

        from .jm_entity import JmPhotoDetail
        return JmPhotoDetail

    @classmethod
    def image_class(cls):
        if cls.CLASS_IMAGE is not None:
            return cls.CLASS_IMAGE

        from .jm_entity import JmImageDetail
        return JmImageDetail

    @classmethod
    def client_impl_class(cls, client_key: str):
        clazz_dict = cls.REGISTRY_CLIENT

        clazz = clazz_dict.get(client_key, None)
        if clazz is None:
            from .jm_toolkit import ExceptionTool
            ExceptionTool.raises(f'not found client impl class for key: "{client_key}"')

        return clazz

    @classmethod
    @field_cache("DOMAIN_HTML")
    def get_html_domain(cls, postman=None):
        """
        由于禁漫的域名经常变化，调用此方法可以获取一个当前可用的最新的域名 domain，
        并且设置把 domain 设置为禁漫模块的默认域名。
        这样一来，配置文件也不用配置域名了，一切都在运行时动态获取。
        """
        from .jm_toolkit import JmcomicText
        return JmcomicText.parse_to_jm_domain(cls.get_html_url(postman))

    @classmethod
    def get_html_url(cls, postman=None):
        """
        访问禁漫的永久网域，从而得到一个可用的禁漫网址
        :returns: https://jm-comic2.cc
        """
        postman = postman or cls.new_postman(session=True)

        url = postman.with_redirect_catching().get(cls.JM_REDIRECT_URL)
        cls.jm_log('module.html_url', f'获取禁漫网页URL: [{cls.JM_REDIRECT_URL}] → [{url}]')
        return url

    @classmethod
    @field_cache("DOMAIN_HTML_LIST")
    def get_html_domain_all(cls, postman=None):
        """
        访问禁漫发布页，得到所有的禁漫网页域名

        :returns: ['18comic.vip', ..., 'jm365.xyz/ZNPJam'], 最后一个是【APP軟件下載】
        """
        postman = postman or cls.new_postman(session=True)

        resp = postman.get(cls.JM_PUB_URL)
        if resp.status_code != 200:
            from .jm_toolkit import ExceptionTool
            ExceptionTool.raises_resp(f'请求失败，访问禁漫发布页获取所有域名，HTTP状态码为: {resp.status_code}', resp)

        from .jm_toolkit import JmcomicText
        domain_list = JmcomicText.analyse_jm_pub_html(resp.text)

        cls.jm_log('module.html_domain_all', f'获取禁漫网页全部域名: [{resp.url}] → {domain_list}')
        return domain_list

    @classmethod
    def new_html_headers(cls, domain='18comic.vip'):
        """
        网页端的headers
        """
        headers = JmMagicConstants.HTML_HEADERS_TEMPLATE.copy()
        headers.update({
            'authority': domain,
            'origin': f'https://{domain}',
            'referer': f'https://{domain}',
        })
        return headers

    @classmethod
    @field_cache()
    def get_fix_ts_token_tokenparam(cls):
        ts = time_stamp()
        from .jm_toolkit import JmCryptoTool
        token, tokenparam = JmCryptoTool.token_and_tokenparam(ts)
        return ts, token, tokenparam

    # noinspection PyUnusedLocal
    @classmethod
    def jm_log(cls, topic: str, msg: str):
        if cls.flag_enable_jm_log is True:
            cls.executor_log(topic, msg)

    @classmethod
    def disable_jm_log(cls):
        cls.flag_enable_jm_log = False

    @classmethod
    def new_postman(cls, session=False, **kwargs):
        kwargs.setdefault('impersonate', 'chrome110')
        kwargs.setdefault('headers', JmModuleConfig.new_html_headers())
        kwargs.setdefault('proxies', JmModuleConfig.DEFAULT_PROXIES)

        from common import Postmans

        if session is True:
            return Postmans.new_session(**kwargs)

        return Postmans.new_postman(**kwargs)

    # option 相关的默认配置
    # 一般情况下，建议使用option配置文件来定制配置
    # 而如果只想修改几个简单常用的配置，也可以下方的DEFAULT_XXX属性
    JM_OPTION_VER = '2.1'
    DEFAULT_CLIENT_IMPL = 'api'  # 默认Client实现类型为网页端
    DEFAULT_CLIENT_CACHE = True  # 默认开启Client缓存，缓存级别是level_option，详见CacheRegistry
    DEFAULT_PROXIES = ProxyBuilder.system_proxy()  # 默认使用系统代理

    default_option_dict: dict = {
        'log': None,
        'dir_rule': {'rule': 'Bd_Pname', 'base_dir': None},
        'download': {
            'cache': True,
            'image': {'decode': True, 'suffix': None},
            'threading': {
                'image': 30,
                'photo': None,
            },
        },
        'client': {
            'cache': None,  # see CacheRegistry
            'domain': [],
            'postman': {
                'type': 'cffi',
                'meta_data': {
                    'impersonate': 'chrome110',
                    'headers': None,
                    'proxies': None,
                }
            },
            'impl': None,
            'retry_times': 5,
        },
        'plugins': {
            # 如果插件抛出参数校验异常，只log。（全局配置，可以被插件的局部配置覆盖）
            # 可选值：ignore（忽略），log（打印日志），raise（抛异常）。
            'valid': 'log',
        },
    }

    @classmethod
    def option_default_dict(cls) -> dict:
        """
        返回JmOption.default()的默认配置字典。
        这样做是为了支持外界自行覆盖option默认配置字典
        """
        from copy import deepcopy

        option_dict = deepcopy(cls.default_option_dict)

        # log
        if option_dict['log'] is None:
            option_dict['log'] = cls.flag_enable_jm_log

        # dir_rule.base_dir
        dir_rule = option_dict['dir_rule']
        if dir_rule['base_dir'] is None:
            import os
            dir_rule['base_dir'] = os.getcwd()

        # client cache
        client = option_dict['client']
        if client['cache'] is None:
            client['cache'] = cls.DEFAULT_CLIENT_CACHE

        # client impl
        if client['impl'] is None:
            client['impl'] = cls.DEFAULT_CLIENT_IMPL

        # postman proxies
        meta_data = client['postman']['meta_data']
        if meta_data['proxies'] is None:
            # use system proxy by default
            meta_data['proxies'] = cls.DEFAULT_PROXIES

        # threading photo
        dt = option_dict['download']['threading']
        if dt['photo'] is None:
            import os
            dt['photo'] = os.cpu_count()

        return option_dict

    @classmethod
    def register_plugin(cls, plugin_class):
        from .jm_toolkit import ExceptionTool
        ExceptionTool.require_true(getattr(plugin_class, 'plugin_key', None) is not None,
                                   f'未配置plugin_key, class: {plugin_class}')
        cls.REGISTRY_PLUGIN[plugin_class.plugin_key] = plugin_class

    @classmethod
    def register_client(cls, client_class):
        from .jm_toolkit import ExceptionTool
        ExceptionTool.require_true(getattr(client_class, 'client_key', None) is not None,
                                   f'未配置client_key, class: {client_class}')
        cls.REGISTRY_CLIENT[client_class.client_key] = client_class


jm_log = JmModuleConfig.jm_log
disable_jm_log = JmModuleConfig.disable_jm_log
