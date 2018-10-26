#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcaddon
from common import *

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")
sys.path.append(xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib')))
from WindowManager import wm


class Main:

    def __init__(self):
        pass


log('script version %s started' % ADDON_VERSION)

if sys.argv[1] == "home":
    wm.open_home()
elif sys.argv[1] == "follow":
    wm.open_follow()
elif sys.argv[1] == "history":
    wm.open_history()

log('script version %s stopped' % ADDON_VERSION)
