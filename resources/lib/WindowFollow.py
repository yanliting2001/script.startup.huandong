# -*- coding: utf8 -*-

import xbmcgui
import xbmcaddon
from BaseClasses import *
from dialogs.DialogBaseInfo import DialogBaseInfo
from OnClickHandler import OnClickHandler
from common import *

ch = OnClickHandler()
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")
C_LIST_FOLLOW = 5000


class WindowFollow(WindowXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(WindowFollow, self).__init__(*args, **kwargs)

    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        self.parse_follow_list()

    def onAction(self, action):
        super(WindowFollow, self).onAction(action)
        ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(WindowMovieDetail, self).onClick(control_id)
        ch.serve(control_id, self)

    def parse_follow_list(self):
        data = self.get_local_movie_list_all()
        if not data:
            return
        videos = data['videos']
        items = []
        for video in videos:
            item = {"label": video['title'],
                    "icon": video['imgurl'],
                    "vid": video['vid']}
            items.append(item)
        self.set_container(C_LIST_FOLLOW, items, True)

    def get_local_movie_list_all(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_all.json")
