# -*- coding: utf8 -*-

import xbmc
import xbmcaddon
import xbmcgui
from OnClickHandler import OnClickHandler
from dialogs.DialogBaseInfo import DialogBaseInfo
from BaseClasses import *
from common import *
from WindowManager import wm
from follow import fc
from download import dc
import VideoPlayer

ch = OnClickHandler()
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")
MOVIE_DATA_PATH = "D:/"
HOME = xbmcgui.Window(10000)
PLAYER = VideoPlayer.VideoPlayer()
C_LIST_ACTORS = 3001
C_LIST_RECOMMEMD = 6000
C_BUTTON_PLAY = 201
C_BUTTON_FOLLOW = 202
C_BUTTON_DEL = 203
C_PROGRESS_DOWNLOAD = 9001
C_BUTTON_PLOT = 4001


class WindowMovieDetail(WindowXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(WindowMovieDetail, self).__init__(*args, **kwargs)
        self.title = kwargs.get("title")
        self.imgUrl = kwargs.get("icon")
        self.vid = kwargs.get("video_id")
        self.type = kwargs.get("resource_type")
        self.path = MOVIE_DATA_PATH + kwargs.get("path")
        self.file_path = ""
        self.detaildata = {}
        self.downloadStatusData = None

    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        self.downloadStatusData = self.get_download_status_list()
        self.parse_local_movie_info(self.path)

    def onAction(self, action):
        super(WindowMovieDetail, self).onAction(action)
        ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(WindowMovieDetail, self).onClick(control_id)
        ch.serve(control_id, self)

    @check_multiclick
    @ch.click(C_BUTTON_PLAY)
    def video_action(self):
        button_label = self.getControl(C_BUTTON_PLAY).getLabel()
        if button_label == u"播  放":
            PLAYER.play(self.file_path, self.vid, self.detaildata)
        if button_label == u"下  载":
            percent = "8"
            self.window.setProperty("IsDownloading", "1")
            self.window.setProperty("DownloadPercentInt", percent)
            self.download_progress()
            dc.add_download([{"cid": self.vid, "vid": self.vid, "percent": percent, "title": self.title}])

    @check_multiclick
    @ch.click(C_BUTTON_FOLLOW)
    def video_follow(self):
        if not self.window.getProperty("Movie.IsFollow"):
            fc.add_follow(self.vid, self.detaildata)
        else:
            fc.remove_follow(self.vid)
        self.check_follow(self.vid)
        if HOME.getProperty("FollowToVideoDetail"):
            HOME.setProperty("FollowUpdate", "1")

    @check_multiclick
    @ch.click(C_BUTTON_DEL)
    def del_local_movie(self):
        self.getControl(C_BUTTON_PLAY).setLabel(u"下  载")
        self.control.setVisible(False)
        self.setFocusId(C_BUTTON_PLAY)
        dc.remove_download(self.vid)
        self.update_movie_download_status(self.vid, "0")
        HOME.setProperty("LocalMovieUpdated", "1")

    @check_multiclick
    @ch.click(C_LIST_RECOMMEMD)
    def open_new_detail(self):
        title = self.listitem.getProperty("label")
        icon = self.listitem.getProperty("icon")
        resource_type = self.listitem.getProperty("type")
        path = self.listitem.getProperty("path")
        icon = icon.replace(MOVIE_DATA_PATH, "")
        path = path.replace(MOVIE_DATA_PATH, "")
        vid = self.listitem.getProperty("vid")
        wm.open_movie_detail(prev_window=None, title=title, icon=icon, video_id=vid, resource_type=resource_type, path=path)

    @check_multiclick
    @ch.click(C_BUTTON_PLOT)
    def open_plot_dialog(self):
        plot = self.window.getProperty("MoviePlot")
        wm.open_video_plot(prev_window=None, plot=plot)

    def parse_local_movie_info(self, path):
        data = self.get_local_movie_detail_json(path)
        poster_path = data["movie"]["poster"]
        score = data["movie"]["score"]
        directors = data["movie"]["director"]
        actors = data["movie"]["actors"]
        self.file_path = path + data["movie"]["url"]
        stars = self.get_stars_from_score(str(int(score) * 2))
        self.check_download(self.vid)
        self.check_follow(self.vid)
        self.parse_local_recommend_list()
        self.window.setProperty("PosterImage", path + poster_path)
        self.window.setProperty("MovieStars", stars)
        self.window.setProperty("MovieTitle", self.title)
        self.window.setProperty("MovieDirector", directors.replace(",", u"、"))
        actors = actors.split(",")
        if actors:
            self.set_actor_list(actors)
        self.window.setProperty("MoviePlot", data["movie"]["description"])
        self.detaildata = self.set_detail_data(data["movie"], "local")

    def parse_cloud_movie_info(self, name):
        data = self.get_cloud_movie_detail_json(name)
        poster_path = ADDON_PATH + data["v"]["fanart"]
        recommend_list = data["recommend"]
        mark = data["v"]["mark"]
        stars = self.get_stars_from_score(mark)
        self.check_follow(self.vid)
        self.parse_cloud_recommend_list(recommend_list[:6])
        self.window.setProperty("PosterImage", poster_path)
        self.window.setProperty("MovieStars", stars)
        self.window.setProperty("MovieTitle", self.title)
        self.window.setProperty("MovieDirector", data["v"]["director"])
        actors = data["v"]["actors"]
        if actors:
            self.set_actor_list(actors)
        self.window.setProperty("MoviePlot", data["v"]["content"])
        self.detaildata = self.set_detail_data(data["v"], "cloud")

    @run_async
    def parse_local_recommend_list(self):
        data = self.get_local_movie_relate_json(self.path)
        listitems = []
        for item in data["relateList"]:
            liz = {"label": item["name"],
                   "icon": MOVIE_DATA_PATH + item["imgUrl"],
                   "path": MOVIE_DATA_PATH + item["url"],
                   "vid": item["url"].replace("/", ""),
                   "type": "local"}
            listitems.append(liz)
        self.set_container(C_LIST_RECOMMEMD, listitems)

    @run_async
    def parse_cloud_recommend_list(self, lists):
        listitems = []
        for item in lists:
            liz = {"label": item["title"],
                   "vid": item["id"],
                   "icon": "http://img24.pplive.cn/sp423/" + item["extraData"]["coverPic"]}
            listitems.append(liz)
        self.set_container(C_LIST_RECOMMEMD, listitems)

    @run_async
    def check_follow(self, cid):
        if (fc.verify_follow(cid)):
            self.window.setProperty("Movie.IsFollow", "1")
            self.getControl(C_BUTTON_FOLLOW).setLabel(u"已收藏")
        else:
            self.window.clearProperty("Movie.IsFollow")
            self.getControl(C_BUTTON_FOLLOW).setLabel(u"收  藏")

    def check_download(self, cid):
        data = dc.get_one_download(cid)
        if data:
            percent = data["viewInfo"][0]["percent"]
            if percent != "100":
                self.window.setProperty("IsDownloading", "1")
                self.window.setProperty("DownloadPercentInt", percent)
                self.getControl(C_PROGRESS_DOWNLOAD).setPercent(float(int(percent)))
                self.download_progress()
        elif cid in ["htpy", "mtyj"]:
            self.getControl(C_BUTTON_PLAY).setLabel(u"播  放")
            self.getControl(C_BUTTON_FOLLOW).setVisible(False)
            self.getControl(C_BUTTON_DEL).setVisible(False)
        else:
            status = self.get_movie_download_status(cid)
            if status == "1":
                self.getControl(C_BUTTON_PLAY).setLabel(u"播  放")
                self.getControl(C_BUTTON_DEL).setVisible(True)
            elif status == "0":
                self.getControl(C_BUTTON_PLAY).setLabel(u"下  载")
                self.getControl(C_BUTTON_DEL).setVisible(False)

    @run_async
    def download_progress(self):
        count = int(self.window.getProperty("DownloadPercentInt"))
        control_progress = self.getControl(C_PROGRESS_DOWNLOAD)
        while True:
            xbmc.sleep(5000)
            count += 2
            if count > 100:
                count = 100
                break
            control_progress.setPercent(float(count))
            self.window.setProperty("DownloadPercentInt", str(count))
            dc.add_download([{"cid": self.vid, "vid": self.vid, "percent": str(count), "title": self.title}])
        self.window.clearProperty("IsDownloading")
        self.getControl(C_BUTTON_PLAY).setLabel(u"播  放")
        self.getControl(C_BUTTON_DEL).setVisible(True)
        self.setFocusId(C_BUTTON_PLAY)
        dc.add_download([{"cid": self.vid, "vid": self.vid, "percent": str(count), "title": self.title}])
        self.update_movie_download_status(self.vid, "1")
        HOME.setProperty("LocalMovieUpdated", "1")

    def set_actor_list(self, lists):
        listitems = []
        for (count, item) in enumerate(lists):
            if count == len(lists) - 1:
                liz = {"label": item}
            else:
                liz = {"label": item + u"、"}
            listitems.append(liz)
        self.set_container(C_LIST_ACTORS, listitems)

    def set_detail_data(self, json_query, video_type):
        if not json_query:
            return None
        result = {}
        result["title"] = json_query["title"]
        if video_type == "local":
            result["imgUrl"] = self.imgUrl
            result["path"] = self.vid + "/"
        else:
            result["imgUrl"] = json_query["imgurl"]
            result["path"] = ""
        result["type"] = video_type
        return result

    def get_movie_download_status(self, cid):
        data = self.downloadStatusData
        status = data["data"][cid]["status"]
        return status

    def update_movie_download_status(self, cid, status):
        data = self.downloadStatusData
        data["data"][cid]["status"] = status
        path = ADDON_PATH + "/data/download_list.json"
        write_json_file(path, data)

    def get_stars_from_score(self, score):
        if not score:
            return "0"
        f_score = float(score) / 2.0
        if f_score < 0.3:
            stars = "0"
        elif f_score < 0.8:
            stars = "0.5"
        elif f_score < 1.3:
            stars = "1"
        elif f_score < 1.8:
            stars = "1.5"
        elif f_score < 2.3:
            stars = "2"
        elif f_score < 2.8:
            stars = "2.5"
        elif f_score < 3.3:
            stars = "3"
        elif f_score < 3.8:
            stars = "3.5"
        elif f_score < 4.3:
            stars = "4"
        elif f_score < 4.8:
            stars = "4.5"
        else:
            stars = "5"
        return stars

    def get_local_movie_detail_json(self, path):
        return get_json_file(path + "desc.json")

    def get_local_movie_relate_json(self, path):
        return get_json_file(path + "relatelist.json")

    def get_cloud_movie_detail_json(self, name):
        return get_json_file(ADDON_PATH + "/data/" + name + "/desc.json")

    def get_download_status_list(self):
        return get_json_file(ADDON_PATH + "/data/download_list.json")
