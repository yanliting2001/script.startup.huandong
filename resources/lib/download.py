# -*- coding: utf8 -*-

try:
    import StorageServer2
except Exception:
    import storageserverdummy as StorageServer2
from common import *


class DownloadClass(object):

    def __init__(self):
        pass

    def add_download(self, viewInfo):
        self._add(viewInfo)

    def remove_download(self, cid):
        self._remove([{"cid": "{cid}".format(cid=cid)}])

    def reset_download(self):
        self._reset()

    def get_all_download(self):
        return self._get_all()

    def get_one_download(self, cid):
        return self._get_one(cid)

    def _add(self, viewInfo):
        cache = StorageServer2.TimedStorage("download")
        try:
            cidlist = cache["list"]
            result = cache["downloaddata"]
        except Exception:
            cache["list"] = []
            cidlist = cache["list"]
            result = {}
            cache["downloaddata"] = result
        try:
            cid = viewInfo[0]["cid"]
            if cid:
                result = cache["downloaddata"]
                result[cid] = {}
                result[cid]["vid"] = viewInfo[0]["vid"]
                result[cid]["title"] = viewInfo[0]["title"]
                result[cid]["percent"] = viewInfo[0]["percent"]
                cache["downloaddata"] = result
                try:
                    del cidlist[cidlist.index(cid)]
                except Exception:
                    pass
                cidlist.insert(0, cid)
                cache["list"] = cidlist
        except Exception:
            log("fetch detail to save download failed")
            print_exc()

    def _remove(self, viewInfo):
        cache = StorageServer2.TimedStorage("download")
        try:
            cidlist = cache["list"]
            del cidlist[cidlist.index(viewInfo[0]["cid"])]
            cache["list"] = cidlist
        except Exception:
            print_exc()
        try:
            cachedata = cache["downloaddata"]
            del cachedata[viewInfo[0]["cid"]]
            cache["downloaddata"] = cachedata
        except Exception:
            print_exc()

    def _reset(self):
        cache = StorageServer2.TimedStorage("download")
        cache["list"] = []
        cache["downloaddata"] = {}

    def _get_all(self):
        cache = StorageServer2.TimedStorage("download")
        try:
            result = cache["downloaddata"]
            cidlist = cache["list"]
        except Exception:
            cidlist = []
            result = {}
            cache["list"] = cidlist
            cache["downloaddata"] = result
        viewInfo = []
        data = None
        for element in cidlist:
            try:
                vid = result[element]["vid"]
                cid = vid
                percent = result[element]["percent"]
                title = result[element]["title"]
                viewInfo.append({"cid": cid, "vid": vid, "percent": percent, "title": title})
            except Exception:
                print_exc()
        data = {"errcode": 0, "errmsg": "", "ret": 0, "viewInfo": viewInfo}
        return data

    def _get_one(self, cid):
        cache = StorageServer2.TimedStorage("download")
        viewInfo = []
        data = None
        try:
            result = cache["downloaddata"]
            if result[cid]:
                vid = result[cid]["vid"]
                percent = result[cid]["percent"]
                title = result[cid]["title"]
                viewInfo.append({"cid": cid, "vid": vid, "percent": percent, "title": title})
        except Exception:
            print_exc()
        if len(viewInfo) > 0:
            data = {"errcode": 0, "errmsg": "", "ret": 0, "viewInfo": viewInfo}
        return data


dc = DownloadClass()
