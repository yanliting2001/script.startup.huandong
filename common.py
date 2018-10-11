#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import xbmc
import xbmcaddon
import xbmcgui
import traceback
import time
from functools import wraps
try:
    import simplejson
except Exception:
    import json as simplejson

ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')


def run_async(func):
    """
    Decorator to run a function in a separate thread
    """
    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = threading.Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


def notify(msg='', title='欢动影院', delay=2000, image=''):
    '''Displays a temporary notification message to the user. If
    title is not provided, the plugin name will be used. To have a
    blank title, pass '' for the title argument. The delay argument
    is in milliseconds.
    '''
    xbmc.executebuiltin('XBMC.Notification("%s", "%s", "%s", "%s")' %
                        (title, str(msg), delay, image))


def print_exc():
    traceback.print_exc()


def prettyprint(string):
    xbmc.log(simplejson.dumps(string, sort_keys=True, indent=4, separators=(',', ': ')))


def okDialog(line1='获取数据失败，请检查网络', title='提示', line2=None, line3=None):
    dialog = xbmcgui.Dialog()
    dialog.ok(title, line1, line2, line3)


def log(txt):
    try:
        message = '%s: %s' % (ADDON_NAME, txt.encode('ascii', 'ignore'))
        xbmc.log(msg=message, level=xbmc.LOGDEBUG)
    except Exception:
        print_exc()


def busy_dialog(func):
    """
    Decorator to show busy dialog while function is running
    Only one of the decorated functions may run simultaniously
    """

    def decorator(*args, **kwargs):
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        try:
            result = func(*args, **kwargs)
        except Exception:
            result = None
            print_exc()
        finally:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
        return result

    return decorator


def check_multiclick(f):
    """
    Decorator to avoid multiple keypresses for onClick / whatever
    """
    def wrapper(*args):
        if args[0].multiclick > 0:
            if time.time() - args[0].multiclick <= 1:
                return
        args[0].multiclick = time.time()
        return f(*args)
    return wrapper
