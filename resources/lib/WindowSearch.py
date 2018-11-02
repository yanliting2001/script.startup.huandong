# -*- coding: utf8 -*-

import xbmc
import xbmcgui
import xbmcaddon
from BaseClasses import *
from dialogs.DialogBaseInfo import DialogBaseInfo
from OnClickHandler import OnClickHandler
from common import *
from WindowManager import wm

ch = OnClickHandler()
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")
HOME = xbmcgui.Window(10000)
MOVIE_DATA_PATH = "/storage/udisk0/part1/"
C_PANEL_T9 = 9090
C_LIST_SEARCH_ONE = 9091
C_LIST_SEARCH_TWO = 9092
C_LABEL_KEYWORD = 312
C_BUTTON_CLEAR = 261
C_BUTTON_DEL = 262
LIST_BUTTONS = [60101, 60102, 60103, 60104, 60105]
ACTION_PREVIOUS_MENU = [9, 92, 10]
LIST_KEYBOARD = [201, 202, 203, 204, 205, 206,
                 211, 212, 213, 214, 215, 216,
                 221, 222, 223, 224, 225, 226,
                 231, 232, 233, 234, 235, 236,
                 241, 242, 243, 244, 245, 246,
                 251, 252, 253, 254, 255, 256]


class WindowSearch(WindowXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(WindowSearch, self).__init__(*args, **kwargs)
        self.searchKey = ""

    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())

    def onAction(self, action):
        if action.getId() in ACTION_PREVIOUS_MENU and self.getFocusId() in LIST_BUTTONS:
            HOME.clearProperty('T9')
            HOME.clearProperty('T9_Key')
            self.setFocusId(C_PANEL_T9)
        else:
            super(WindowSearch, self).onAction(action)
            ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(WindowSearch, self).onClick(control_id)
        ch.serve(control_id, self)

    @ch.click(LIST_KEYBOARD)
    def click_search_word(self):
        self.deal_keyboard(self.control_id)

    @ch.click(C_BUTTON_DEL)
    def del_search_word(self):
        control = self.getControl(C_LABEL_KEYWORD)
        self.searchKey = control.getLabel()
        self.searchKey = self.searchKey[0:-1]
        control.setLabel(self.searchKey)
        if self.searchKey != "":
            self.set_search_result(self.searchKey)
        else:
            self.getControl(C_LIST_SEARCH_ONE).reset()
            self.getControl(C_LIST_SEARCH_TWO).reset()

    @ch.click(C_BUTTON_CLEAR)
    def clear_search_word(self):
        self.getControl(C_LABEL_KEYWORD).setLabel("")
        self.searchKey = ""
        self.getControl(C_LIST_SEARCH_ONE).reset()
        self.getControl(C_LIST_SEARCH_TWO).reset()

    @ch.click([C_LIST_SEARCH_ONE, C_LIST_SEARCH_TWO])
    def open_movie_detail(self):
        title = self.listitem.getProperty("label")
        icon = self.listitem.getProperty("icon")
        resource_type = self.listitem.getProperty("type")
        path = self.listitem.getProperty("path")
        if resource_type == "local":
            icon = icon.replace(MOVIE_DATA_PATH, "")
            path = path.replace(MOVIE_DATA_PATH, "")
        vid = self.listitem.getProperty("vid")
        wm.open_movie_detail(prev_window=None, title=title, icon=icon, video_id=vid, resource_type=resource_type, path=path)

    def show_search_rank(self):
        data = self.get_local_movie_list_best()
        videos = data["localList"]
        items = []
        for video in videos:
            video_path = video['url']
            item = {"label": video['name'],
                    "icon": MOVIE_DATA_PATH + video['imgUrl'],
                    "vid": video_path.replace("/", ""),
                    "path": MOVIE_DATA_PATH + video['url'],
                    "type": "local"}
            items.append(item)
        self.set_container(C_LIST_SEARCH_ONE, items[:4])
        self.set_container(C_LIST_SEARCH_TWO, items[4:10])

    def deal_keyboard(self, control_id):
        letters = {
            "A": 201,
            "B": 202,
            "C": 203,
            "D": 204,
            "E": 205,
            "F": 206,
            "G": 211,
            "H": 212,
            "I": 213,
            "J": 214,
            "K": 215,
            "L": 216,
            "M": 221,
            "N": 222,
            "O": 223,
            "P": 224,
            "Q": 225,
            "R": 226,
            "S": 231,
            "T": 232,
            "U": 233,
            "V": 234,
            "W": 235,
            "X": 236,
            "Y": 241,
            "Z": 251,
            "0": 242,
            "1": 243,
            "2": 244,
            "3": 245,
            "4": 246,
            "5": 252,
            "6": 253,
            "7": 254,
            "8": 255,
            "9": 256
        }
        for letter, letter_id in letters.items():
            if control_id == letter_id:
                self.appendText(letter)

    def appendText(self, char):
        control = self.getControl(C_LABEL_KEYWORD)
        self.searchKey = control.getLabel() + char
        control.setLabel(self.searchKey)
        self.set_search_result(self.searchKey)

    def set_search_result(self, keyword):
        items = self.get_search_data(keyword)
        self.set_container(C_LIST_SEARCH_ONE, items[:4])
        self.set_container(C_LIST_SEARCH_TWO, items[4:10])

    def get_search_data(self, keyword):
        keyword_lower = keyword.lower()
        data = self.get_local_movie_list()
        videos = data["localList"]
        items = []
        for video in videos:
            video_path = video["url"]
            if keyword_lower not in video_path:
                continue
            item = {"label": video['name'],
                    "icon": MOVIE_DATA_PATH + video['imgUrl'],
                    "vid": video_path.replace("/", ""),
                    "path": MOVIE_DATA_PATH + video['url'],
                    "type": "local"}
            items.append(item)
        return items

    def get_local_movie_list(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist.json")

    def get_local_movie_list_best(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist_best.json")
