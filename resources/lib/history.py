# -*- coding: utf8 -*-

try:
    import StorageServer2
except Exception:
    import storageserverdummy as StorageServer2
from common import *
try:
    import simplejson
except Exception:
    import json as simplejson


class HistoryClass(object):

    def __init__(self):
        pass

    def add_history(self, viewInfo):
        self._add(viewInfo)

    def remove_history(self, viewInfo):
        self._remove(viewInfo)

    def reset_history(self):
        self._reset()

    def get_all_history(self):
        return self._get_all()

    def get_one_history(self, cid):
        return self._get_one(cid)

    def _add(self, viewInfo):
        cache = StorageServer2.TimedStorage("history")
        try:
            cidlist = cache["list"]
            result = cache["historydata"]
        except Exception:
            cache["list"] = []
            cidlist = cache["list"]
            result = {}
            cache["historydata"] = result
        try:
            cid = viewInfo[0]["cid"]
            if cid:
                result = cache["historydata"]
                result[cid] = {}
                result[cid]["vid"] = viewInfo[0]["vid"]
                result[cid]["strTime"] = viewInfo[0]["strTime"]
                result[cid]["title"] = viewInfo[0]["title"]
                result[cid]["imgUrl"] = viewInfo[0]["imgUrl"]
                result[cid]["path"] = viewInfo[0]["path"]
                result[cid]["type"] = viewInfo[0]["type"]
                cache["historydata"] = result
                try:
                    del cidlist[cidlist.index(cid)]
                except Exception:
                    pass
                cidlist.insert(0, cid)
                cache["list"] = cidlist
        except Exception:
            log("fetch detail to save history failed")
            print_exc()

    def _remove(self, viewInfo):
        cache = StorageServer2.TimedStorage("history")
        try:
            cidlist = cache["list"]
            del cidlist[cidlist.index(viewInfo[0]["cid"])]
            cache["list"] = cidlist
        except Exception:
            cache["list"] = []
        try:
            cachedata = cache["historydata"]
            del cachedata[viewInfo[0]["cid"]]
            cache["historydata"] = cachedata
        except Exception:
            cache["historydata"] = {}

    def _reset(self):
        cache = StorageServer2.TimedStorage("history")
        cache["list"] = []
        cache["historydata"] = {}

    def _get_all(self):
        cache = StorageServer2.TimedStorage("history")
        try:
            result = cache["historydata"]
            cidlist = cache["list"]
        except Exception:
            cidlist = []
            result = {}
            cache["list"] = cidlist
            cache["historydata"] = result
        viewInfo = []
        data = None
        for element in cidlist:
            try:
                vid = result[element]["vid"]
                cid = vid
                strTime = result[element]["strTime"]
                title = result[element]["title"]
                imgUrl = result[element]["imgUrl"]
                path = result[element]["path"]
                c_type = result[element]["type"]
                viewInfo.append({"cid": cid, "vid": vid, "strTime": strTime, "title": title, "imgUrl": imgUrl, "path": path, "type": c_type})
            except Exception:
                print_exc()
        data = {"errcode": 0, "errmsg": "", "ret": 0, "viewInfo": viewInfo}
        return data

    def _get_one(self, cid):
        cache = StorageServer2.TimedStorage("history")
        viewInfo = []
        data = None
        try:
            result = cache["historydata"]
            if result[cid]:
                vid = result[cid]["vid"]
                strTime = result[cid]["strTime"]
                title = result[cid]["title"]
                imgUrl = result[cid]["imgUrl"]
                path = result[cid]["path"]
                c_type = result[cid]["type"]
                viewInfo.append({"cid": cid, "vid": vid, "strTime": strTime, "title": title, "imgUrl": imgUrl, "path": path, "type": c_type})
        except Exception:
            print_exc()
        if len(viewInfo) > 0:
            data = {"errcode": 0, "errmsg": "", "ret": 0, "viewInfo": viewInfo}
        return data


hc = HistoryClass()
