# -*- coding: utf-8 -*-

import os
import xbmc
import xbmcaddon
from common import log

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_DATA_PATH = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID))


class Main:

    def __init__(self):
        pass

    def _init_vars(self):
        pass


class Widgets_Monitor(xbmc.Monitor):

    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)


class Widgets_Player(xbmc.Player):

    def __init_(self, *args, **kwargs):
        xbmc.Player.__init_(self)

    def onPlayBackStarted(self):
        pass

    def onPlayBackStopped(self):
        pass


log('service version %s started' % ADDON_VERSION)
Main()
log('service version %s stopped' % ADDON_VERSION)
