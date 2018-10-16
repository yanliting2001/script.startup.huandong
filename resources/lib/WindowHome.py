# -*- coding: utf8 -*-

import xbmc
import xbmcaddon
import xbmcgui
from OnClickHandler import OnClickHandler
from dialogs.DialogBaseInfo import DialogBaseInfo
from BaseClasses import *
from common import get_json_file
try:
    import simplejson
except Exception:
    import json as simplejson

ch = OnClickHandler()
C_LIST_NAVIGATION = 9000
C_LEFTLIST_LOCAL = 2001
C_LEFTLIST_MOVIE_CATEGORIES = 200104
C_LIST_MOVIE = 200002
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")


class WindowHome(WindowXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(WindowHome, self).__init__(*args, **kwargs)

    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        self.set_local_movie_categories()
        self.set_local_movie_list()

    def onAction(self, action):
        if (action.getId() == 10 or action.getId() == 92):
            self.setFocus(self.getControl(C_LIST_NAVIGATION))
        else:
            super(WindowHome, self).onAction(action)
            ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(WindowHome, self).onClick(control_id)
        ch.serve(control_id, self)

    def set_local_movie_categories(self):
        data = self.get_local_movie_categories()
        itemValues = data['items'][0]['itemValues']
        items = []
        for value in itemValues:
            item = {"label": value['key'],
                    "value": value['val']}
            items.append(item)
        self.set_container(C_LEFTLIST_MOVIE_CATEGORIES, items, True)

    def set_local_movie_list(self):
        data = self.get_local_movie_list_all()
        videos = data['videos']
        items = []
        for video in videos:
            item = {"label": video['title'],
                    "icon": video['imgurl'],
                    "vid": video['vid']}
            items.append(item)
        self.set_container(C_LIST_MOVIE, items)

    def get_local_movie_categories(self):
        return get_json_file(ADDON_PATH + "/data/movie_categories.json")

    def get_local_movie_list_all(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_all.json")
