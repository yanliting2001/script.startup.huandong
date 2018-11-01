# -*- coding: utf8 -*-

import xbmcgui
import xbmcaddon
from BaseClasses import *
from dialogs.DialogBaseInfo import DialogBaseInfo
from OnClickHandler import OnClickHandler
from common import *
from follow import fc
from WindowManager import wm

ch = OnClickHandler()
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")
MOVIE_DATA_PATH = "/storage/udisk0/part1/"
HOME = xbmcgui.Window(10000)
C_LIST_FOLLOW = 5000
C_BUTTON_DEL = 200


class WindowFollow(WindowXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(WindowFollow, self).__init__(*args, **kwargs)
        self.isLaunched = False

    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        if not self.isLaunched:
            self.parse_follow_list()
            self.isLaunched = True
        elif HOME.getProperty("FollowUpdate"):
            self.parse_follow_list()
            HOME.clearProperty("FollowUpdate")

    def onAction(self, action):
        super(WindowFollow, self).onAction(action)
        ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(WindowFollow, self).onClick(control_id)
        ch.serve(control_id, self)

    @ch.click(C_LIST_FOLLOW)
    def open_movie_info_window(self):
        title = self.listitem.getProperty("label")
        icon = self.listitem.getProperty("icon")
        resource_type = self.listitem.getProperty("type")
        path = self.listitem.getProperty("path")
        if resource_type == "local":
            icon = icon.replace(MOVIE_DATA_PATH, "")
            path = path.replace(MOVIE_DATA_PATH, "")
        vid = self.listitem.getProperty("vid")
        HOME.setProperty("FollowToVideoDetail", "1")
        wm.open_movie_detail(prev_window=None, title=title, icon=icon, video_id=vid, resource_type=resource_type, path=path)

    @ch.click(C_BUTTON_DEL)
    def del_all(self):
        fc.reset_follow()
        self.getControl(C_LIST_FOLLOW).reset()

    def parse_follow_list(self):
        data = fc.get_follow()
        follow_list = data.get("vidlist")
        if not follow_list:
            self.getControl(C_LIST_FOLLOW).reset()
            return
        items = []
        for item in follow_list:
            liz = {"label": item["title"],
                   "icon": MOVIE_DATA_PATH + item["imgUrl"],
                   "vid": item["cid"],
                   "path": MOVIE_DATA_PATH + item["path"],
                   "type": item["type"]}
            items.append(liz)
        self.set_container(C_LIST_FOLLOW, items, True)
