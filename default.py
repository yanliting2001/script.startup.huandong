#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcaddon
from common import *

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')


class Main:

    def __init__(self):
        pass


log('script version %s started' % ADDON_VERSION)

if sys.argv[1] == "home":
    pass
