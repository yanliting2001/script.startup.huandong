# -*- coding: utf8 -*-

import xbmc
import xbmcgui
from history import hc
try:
    import simplejson
except Exception:
    import json as simplejson
from common import time_format_number


class VideoPlayer(xbmc.Player):

    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        self.stopped = False

    def onPlayBackEnded(self):
        self.stopped = True

    def onPlayBackStopped(self):
        self.stopped = True

    def onPlayBackStarted(self):
        self.stopped = False
        xbmc.executebuiltin("ActivateWindow(fullscreenvideo)")

    def play(self, url, cid="", detaildata=None):
        if not detaildata:
            super(VideoPlayer, self).play(item=url)
        else:
            historydata = hc.get_one_history(cid)
            if historydata and historydata["errcode"] == 0:
                datatime = historydata["viewInfo"][0]["strTime"]
            else:
                datatime = "00:00"
            title = detaildata["title"]
            data_mpaa = {"imgUrl": detaildata["imgUrl"],
                         "path": detaildata["path"],
                         "type": detaildata["type"]}
            mpaa = simplejson.dumps(data_mpaa).encode("base64")
            startTime = self.continue_play_time(datatime)
            listitem = xbmcgui.ListItem(title)
            listitem.setInfo("video", {"Title": title})
            listitem.setInfo("video", {"Genre": cid})
            listitem.setInfo("video", {"Mpaa": mpaa})
            listitem.setProperty("startoffset", str(startTime))
            super(VideoPlayer, self).play(item=url,
                                          listitem=listitem,
                                          windowed=False,
                                          startpos=-1)

    def stop(self, cid, data):
        title = xbmc.getInfoLabel("VideoPlayer.Title")
        strTime = time_format_number(xbmc.getInfoLabel("VideoPlayer.Time"))
        vid = cid
        hc.add_history([{"cid": cid, "vid": vid, "strTime": strTime, "title": title.decode("utf8"), "imgUrl": data["imgUrl"], "path": data["path"], "type": data["type"]}])
        xbmcgui.Window(10000).setProperty("HistoryUpdate", "1")
        xbmc.Player.stop(self)

    def continue_play_time(self, datatime):
        head_time = 0
        tail_time = 0
        if datatime and datatime != "0":
            try:
                intTime = int(datatime)
            except Exception:
                intTime = int(time_format_number(datatime))
            return max(intTime, head_time)
        else:
            return head_time


def stop_play():
    if xbmc.Player().isPlaying():
        if not xbmc.Player.isPlayingVideo(VideoPlayer()):
            xbmc.Player().stop()
            return
        cid = xbmc.getInfoLabel("VideoPlayer.Genre")
        mpaa = xbmc.getInfoLabel("VideoPlayer.Mpaa")
        if cid and mpaa:
            data_mpaa = simplejson.loads(mpaa.decode("base64"))
            VideoPlayer().stop(cid, data_mpaa)
        else:
            xbmc.Player().stop()
