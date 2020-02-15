# -*- coding:utf-8 -*-
from importlib import import_module


def load_object(path):
    """Load an object given its absolute object path, and return it.

    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """

    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj


def create_instance(objcls, settings, crawler, *args, **kwargs):
    """Construct a class instance using its ``from_crawler`` or
    ``from_settings`` constructors, if available.

    At least one of ``settings`` and ``crawler`` needs to be different from
    ``None``. If ``settings `` is ``None``, ``crawler.settings`` will be used.
    If ``crawler`` is ``None``, only the ``from_settings`` constructor will be
    tried.

    ``*args`` and ``**kwargs`` are forwarded to the constructors.

    Raises ``ValueError`` if both ``settings`` and ``crawler`` are ``None``.
    """
    if settings is None:
        if crawler is None:
            raise ValueError("Specify at least one of settings and crawler.")
        settings = crawler.settings
    if crawler and hasattr(objcls, 'from_crawler'):
        return objcls.from_crawler(crawler, *args, **kwargs)
    elif hasattr(objcls, 'from_settings'):
        return objcls.from_settings(settings, *args, **kwargs)
    else:
        return objcls(*args, **kwargs)


async def call_func(func, callback=None, errback=None, *args, **kwargs):
    """
    :param func:
    :param errback:
    :param callback:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        result = await func(*args, **kwargs)
    except Exception as exc:
        #     # 异常回调函数
        if errback:
            result = await errback(exc)
    else:
        if callback:
            result = await callback(result)
        return result
