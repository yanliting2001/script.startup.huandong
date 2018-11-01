# -*- coding: utf8 -*-

import xbmcgui
import xbmcaddon
from BaseClasses import *
from dialogs.DialogBaseInfo import DialogBaseInfo
from OnClickHandler import OnClickHandler
from common import *
from history import hc
from WindowManager import wm

ch = OnClickHandler()
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")
MOVIE_DATA_PATH = "/storage/udisk0/part1/"
HOME = xbmcgui.Window(10000)
C_LIST_HISTORY = 5000
C_BUTTON_DEL = 200


class WindowHistory(WindowXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(WindowHistory, self).__init__(*args, **kwargs)
        self.isLaunched = False

    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        if not self.isLaunched:
            self.parse_history_list()
            self.isLaunched = True
        elif HOME.getProperty("HistoryUpdate"):
            self.parse_history_list()
            HOME.clearProperty("HistoryUpdate")

    def onAction(self, action):
        super(WindowHistory, self).onAction(action)
        ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(WindowHistory, self).onClick(control_id)
        ch.serve(control_id, self)

    @ch.click(C_LIST_HISTORY)
    def open_movie_info_window(self):
        title = self.listitem.getProperty("label")
        icon = self.listitem.getProperty("icon")
        resource_type = self.listitem.getProperty("type")
        path = self.listitem.getProperty("path")
        if resource_type == "local":
            icon = icon.replace(MOVIE_DATA_PATH, "")
            path = path.replace(MOVIE_DATA_PATH, "")
        vid = self.listitem.getProperty("vid")
        wm.open_movie_detail(prev_window=None, title=title, icon=icon, video_id=vid, resource_type=resource_type, path=path)

    @ch.click(C_BUTTON_DEL)
    def del_all(self):
        hc.reset_history()
        self.getControl(C_LIST_HISTORY).reset()

    def parse_history_list(self):
        data = hc.get_all_history()
        history_list = data.get("viewInfo")
        if not history_list:
            self.getControl(C_LIST_HISTORY).reset()
            return
        items = []
        for item in history_list:
            liz = {"label": item["title"],
                   "icon": MOVIE_DATA_PATH + item["imgUrl"],
                   "vid": item["vid"],
                   "path": MOVIE_DATA_PATH + item["path"],
                   "type": item["type"]}
            items.append(liz)
        self.set_container(C_LIST_HISTORY, items, True)
