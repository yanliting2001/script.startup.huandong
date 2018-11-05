# -*- coding: utf8 -*-

import xbmc
import xbmcaddon
import xbmcgui
from OnClickHandler import OnClickHandler
from dialogs.DialogBaseInfo import DialogBaseInfo
from BaseClasses import *
from common import *
from WindowManager import wm
try:
    import simplejson
except Exception:
    import json as simplejson

ch = OnClickHandler()
C_LIST_NAVIGATION = 9000
C_LEFTLIST_LOCAL_CATEGORIES = 200104
C_LEFTLIST_CLOUD_CATEGORIES = 300102
C_LEFTLIST_DOWNLOAD_APP = 400101
C_LEFTLIST_PAY_ABOUT = 400102
C_LIST_LOCAL_MOVIE = 200002
C_LIST_CLOUD_MOVIE = 300001
C_LIST_ACCOUNT_DOWNLOAD = 400001
C_LIST_DOWNLOAD_STATUS = 400002
C_LIST_DOWNLOAD_DEL = 400003
C_LABEL_ACCOUNT_CONTENT = 6000
C_BUTTON_SEARCH = 200102
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")
MOVIE_DATA_PATH = "D:/"


class WindowHome(WindowXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(WindowHome, self).__init__(*args, **kwargs)
        self.isLaunched = False
        self.local_filter = "new"
        self.cloud_filter = "new"
        self.local_filter_pos = 0
        self.cloud_filter_pos = 0

    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        if not self.isLaunched:
            self.set_local_movie_categories()
            self.set_local_movie_list()
            self.set_cloud_movie_categories()
            self.set_cloud_movie_list()
            self.set_account_categories()
            self.isLaunched = True
        self.set_download_list_progress()
        self.set_download_manager_list()

    def onAction(self, action):
        if (action.getId() == 10 or action.getId() == 92):
            self.setFocus(self.getControl(C_LIST_NAVIGATION))
        else:
            super(WindowHome, self).onAction(action)
            ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(WindowHome, self).onClick(control_id)
        ch.serve(control_id, self)

    def onFocus(self, control_id):
        super(WindowHome, self).onFocus(control_id)
        ch.serve_focus(control_id, self)

    @check_multiclick
    @ch.action("up", str(C_LEFTLIST_LOCAL_CATEGORIES))
    @ch.action("down", str(C_LEFTLIST_LOCAL_CATEGORIES))
    def refresh_local_movie_list(self):
        xbmc.sleep(500)
        if self.getFocusId() != C_LEFTLIST_LOCAL_CATEGORIES:
            return
        filter_container = self.getControl(C_LEFTLIST_LOCAL_CATEGORIES)
        pos = filter_container.getSelectedPosition()
        if self.local_filter_pos != pos:
            self.local_filter_pos = pos
            item = filter_container.getSelectedItem()
            self.local_filter_up_down(item)

    @check_multiclick
    @ch.action("up", str(C_LEFTLIST_CLOUD_CATEGORIES))
    @ch.action("down", str(C_LEFTLIST_CLOUD_CATEGORIES))
    def refresh_cloud_movie_list(self):
        xbmc.sleep(500)
        if self.getFocusId() != C_LEFTLIST_CLOUD_CATEGORIES:
            return
        filter_container = self.getControl(C_LEFTLIST_CLOUD_CATEGORIES)
        pos = filter_container.getSelectedPosition()
        if self.cloud_filter_pos != pos:
            self.cloud_filter_pos = pos
            item = filter_container.getSelectedItem()
            self.cloud_filter_up_down(item)

    @ch.action("up", str(C_LIST_DOWNLOAD_STATUS))
    def download_status_list_move_up(self):
        status = self.listitem.getProperty("DownloadStatus")
        pos = self.control.getSelectedPosition()
        if status == "done":
            if pos == 0:
                xbmc.executebuiltin('Control.Move({0},1)'.format(C_LIST_DOWNLOAD_STATUS))
            else:
                xbmc.executebuiltin('Control.Move({0},-1)'.format(C_LIST_DOWNLOAD_STATUS))

    @ch.action("down", str(C_LIST_DOWNLOAD_STATUS))
    def download_status_list_move_down(self):
        status = self.listitem.getProperty("DownloadStatus")
        max_pos = self.control.size() - 1
        pos = self.control.getSelectedPosition()
        if status == "done":
            if pos == max_pos:
                xbmc.executebuiltin('Control.Move({0},-1)'.format(C_LIST_DOWNLOAD_STATUS))
            else:
                xbmc.executebuiltin('Control.Move({0},1)'.format(C_LIST_DOWNLOAD_STATUS))

    @ch.action("up", str(C_LIST_DOWNLOAD_DEL))
    def download_del_list_move_up(self):
        status = self.listitem.getProperty("DownloadStatus")
        pos = self.control.getSelectedPosition()
        if status == "done":
            if pos == 0:
                xbmc.executebuiltin('Control.Move({0},1)'.format(C_LIST_DOWNLOAD_DEL))
            else:
                xbmc.executebuiltin('Control.Move({0},-1)'.format(C_LIST_DOWNLOAD_DEL))

    @ch.action("down", str(C_LIST_DOWNLOAD_DEL))
    def download_del_list_move_down(self):
        status = self.listitem.getProperty("DownloadStatus")
        max_pos = self.control.size() - 1
        pos = self.control.getSelectedPosition()
        if status == "done":
            if pos == max_pos:
                xbmc.executebuiltin('Control.Move({0},-1)'.format(C_LIST_DOWNLOAD_DEL))
            else:
                xbmc.executebuiltin('Control.Move({0},1)'.format(C_LIST_DOWNLOAD_DEL))

    @ch.action("up", str(C_LEFTLIST_DOWNLOAD_APP))
    @ch.action("down", str(C_LEFTLIST_DOWNLOAD_APP))
    def download_app_up_down(self):
        pos = self.listitem.getProperty("CurrentItem")
        if pos == "1":
            self.window.setProperty("AccountContent", "download")
            self.getControl(C_LABEL_ACCOUNT_CONTENT).setLabel(u"下载管理")
        elif pos == "2":
            self.window.setProperty("AccountContent", "app")
            self.getControl(C_LABEL_ACCOUNT_CONTENT).setLabel(u"手机端APP")

    @ch.action("up", str(C_LEFTLIST_PAY_ABOUT))
    @ch.action("down", str(C_LEFTLIST_PAY_ABOUT))
    def pay_about_up_down(self):
        pos = self.listitem.getProperty("CurrentItem")
        if pos == "1":
            self.window.setProperty("AccountContent", "pay")
            self.getControl(C_LABEL_ACCOUNT_CONTENT).setLabel(u"续费缴费")
        elif pos == "2":
            self.window.setProperty("AccountContent", "about")
            self.getControl(C_LABEL_ACCOUNT_CONTENT).setLabel(u"关于我们")

    @ch.click([C_LIST_LOCAL_MOVIE, C_LIST_CLOUD_MOVIE])
    def open_movie_info_window(self):
        title = self.listitem.getProperty("label")
        icon = self.listitem.getProperty("icon")
        resource_type = self.listitem.getProperty("type")
        path = self.listitem.getProperty("path")
        icon = icon.replace(MOVIE_DATA_PATH, "")
        path = path.replace(MOVIE_DATA_PATH, "")
        vid = self.listitem.getProperty("vid")
        wm.open_movie_detail(prev_window=None, title=title, icon=icon, video_id=vid, resource_type=resource_type, path=path)

    @ch.click(C_LIST_DOWNLOAD_STATUS)
    def switch_download_status(self):
        status = self.listitem.getProperty("DownloadStatus")
        if status == "ing":
            self.listitem.setProperty("DownloadStatus", "pause")
        elif status == "pause":
            self.listitem.setProperty("DownloadStatus", "ing")

    @ch.focus(C_LIST_DOWNLOAD_STATUS)
    def status_list_change_pos(self):
        control = self.getControl(C_LIST_DOWNLOAD_DEL)
        pos = control.getSelectedPosition()
        self.control.selectItem(pos)

    @ch.focus(C_LIST_DOWNLOAD_DEL)
    def del_list_change_pos(self):
        control = self.getControl(C_LIST_DOWNLOAD_STATUS)
        pos = control.getSelectedPosition()
        self.control.selectItem(pos)

    def local_filter_up_down(self, item):
        self.local_filter = item.getProperty("key")
        self.set_local_movie_list(self.local_filter)

    def cloud_filter_up_down(self, item):
        self.cloud_filter = item.getProperty("key")
        self.set_cloud_movie_list(self.cloud_filter)

    def set_local_movie_categories(self):
        data = self.get_local_movie_categories()
        category_list = data['localCategories']
        items = []
        for category in category_list:
            item = {"label": category['name'],
                    "key": category['key']}
            items.append(item)
        self.set_container(C_LEFTLIST_LOCAL_CATEGORIES, items, True)

    def set_local_movie_list(self, strFilter="new"):
        data = self.get_local_movie_list(strFilter)
        items = []
        videos = data['localList']
        for video in videos:
            video_path = video['url']
            item = {"label": video['name'],
                    "icon": MOVIE_DATA_PATH + video['imgUrl'],
                    "vid": video_path.replace("/", ""),
                    "path": MOVIE_DATA_PATH + video['url'],
                    "type": "local"}
            items.append(item)
        self.set_container(C_LIST_LOCAL_MOVIE, items)

    def set_cloud_movie_categories(self):
        data = self.get_local_movie_categories()
        category_list = data["localCategories"]
        items = []
        for category in category_list:
            item = {"label": category['name'],
                    "key": category['key']}
            items.append(item)
        self.set_container(C_LEFTLIST_CLOUD_CATEGORIES, items)

    def set_cloud_movie_list(self, strFilter="new"):
        data = self.get_local_movie_list(strFilter)
        items = []
        videos = data["localList"]
        for video in videos:
            video_path = video['url']
            item = {"label": video['name'],
                    "icon": MOVIE_DATA_PATH + video['imgUrl'],
                    "vid": video_path.replace("/", ""),
                    "path": MOVIE_DATA_PATH + video['url'],
                    "type": "cloud"}
            items.append(item)
        self.set_container(C_LIST_CLOUD_MOVIE, items)

    def set_account_categories(self):
        items = [
            {"label": u"下载管理",
             "CurrentItem": "1"},
            {"label": u"手机端APP",
             "CurrentItem": "2"},
            {"label": u"续费缴费",
             "CurrentItem": "1"},
            {"label": u"关于我们",
             "CurrentItem": "2"}]
        self.set_container(C_LEFTLIST_DOWNLOAD_APP, items[:2])
        self.set_container(C_LEFTLIST_PAY_ABOUT, items[2:])

    @run_async
    def set_download_list_progress(self):
        items = [
            {"label": u"侏罗纪公园",
             "ProgressPercent": "75"},
            {"label": u"侏罗纪公园",
             "ProgressPercent": "60"},
            {"label": u"侏罗纪公园",
             "ProgressPercent": "100"},
            {"label": u"侏罗纪公园",
             "ProgressPercent": "98"},
            {"label": u"侏罗纪公园",
             "ProgressPercent": "30"},
            {"label": u"侏罗纪公园",
             "ProgressPercent": "80"},
            {"label": u"侏罗纪公园",
             "ProgressPercent": "98"}]
        self.set_container(C_LIST_ACCOUNT_DOWNLOAD, items)
        self.window.setProperty("AccountContent", "download")

    @run_async
    def set_download_manager_list(self):
        items = [
            {"label": "75%",
             "DownloadStatus": "ing"},
            {"label": "60%",
             "DownloadStatus": "ing"},
            {"label": "100%",
             "DownloadStatus": "done"},
            {"label": "98%",
             "DownloadStatus": "ing"},
            {"label": "30%",
             "DownloadStatus": "ing"},
            {"label": "80%",
             "DownloadStatus": "ing"},
            {"label": "98%",
             "DownloadStatus": "ing"}]
        self.set_container(C_LIST_DOWNLOAD_STATUS, items)
        self.set_container(C_LIST_DOWNLOAD_DEL, items)

    def get_local_movie_list(self, strFilter):
        if strFilter == "new":
            return self.get_local_movie_list_new()
        elif strFilter == "coming":
            return self.get_local_movie_list_coming()
        elif strFilter == "best":
            return self.get_local_movie_list_best()
        elif strFilter == "rank":
            return self.get_local_movie_list_rank()
        elif strFilter == "hotstar":
            return self.get_local_movie_list_star()
        elif strFilter == "action":
            return self.get_local_movie_list_action()
        elif strFilter == "city":
            return self.get_local_movie_list_city()
        elif strFilter == "scream":
            return self.get_local_movie_list_scream()
        elif strFilter == "detect":
            return self.get_local_movie_list_detect()

    def get_cloud_movie_list(self, strFilter):
        if strFilter == "":
            return self.get_cloud_movie_list_all()
        elif strFilter == "AREA=美国":
            return self.get_cloud_movie_list_hollywood()
        elif strFilter == "cataid=211280,157":
            return self.get_cloud_movie_list_cinema()
        elif strFilter == "AREA=大陆,香港,澳门,台湾":
            return self.get_cloud_movie_list_chinese()
        elif strFilter == "cataid=101,132,133,134":
            return self.get_cloud_movie_list_love()
        elif strFilter == "cataid=124":
            return self.get_cloud_movie_list_comedy()
        elif strFilter == "cataid=125,128":
            return self.get_cloud_movie_list_crime()
        elif strFilter == "cataid=102,103,129,131":
            return self.get_cloud_movie_list_scream()
        elif strFilter == "cataid=100,127":
            return self.get_cloud_movie_list_action()
        elif strFilter == "cataid=104,126":
            return self.get_cloud_movie_list_fiction()
        elif strFilter == "cataid=130":
            return self.get_cloud_movie_list_animation()
        elif strFilter == "cataid=75281,211334":
            return self.get_cloud_movie_list_network()

    def get_local_movie_categories(self):
        return get_json_file(MOVIE_DATA_PATH + "local_category.json")

    def get_local_movie_list_new(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist.json")

    def get_local_movie_list_coming(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist_coming.json")

    def get_local_movie_list_best(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist_best.json")

    def get_local_movie_list_rank(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist_rank.json")

    def get_local_movie_list_star(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist_hotstar.json")

    def get_local_movie_list_action(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist_action.json")

    def get_local_movie_list_city(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist_city.json")

    def get_local_movie_list_scream(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist_scream.json")

    def get_local_movie_list_detect(self):
        return get_json_file(MOVIE_DATA_PATH + "locallist_detect.json")

    def get_cloud_movie_categories(self):
        return get_json_file(ADDON_PATH + "/data/movie_categories.json")

    def get_cloud_movie_list_all(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_all.json")

    def get_cloud_movie_list_hollywood(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_hollywood.json")

    def get_cloud_movie_list_cinema(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_cinema.json")

    def get_cloud_movie_list_chinese(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_chinese.json")

    def get_cloud_movie_list_love(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_love.json")

    def get_cloud_movie_list_comedy(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_comedy.json")

    def get_cloud_movie_list_crime(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_crime.json")

    def get_cloud_movie_list_scream(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_scream.json")

    def get_cloud_movie_list_action(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_action.json")

    def get_cloud_movie_list_animation(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_animation.json")

    def get_cloud_movie_list_fiction(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_fiction.json")

    def get_cloud_movie_list_network(self):
        return get_json_file(ADDON_PATH + "/data/movie_list_network.json")
