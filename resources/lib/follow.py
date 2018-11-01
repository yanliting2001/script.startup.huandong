# -*- coding: utf8 -*-

try:
    import StorageServer2
except Exception:
    import storageserverdummy as StorageServer2
try:
    import simplejson
except Exception:
    import json as simplejson
from common import *


class FollowClass(object):

    def __init__(self):
        pass

    def add_follow(self, cid, detaildata):
        errcode = self._add([{"cid": "{cid}".format(cid=cid)}], detaildata)
        if errcode == 0:
            return True
        return False

    def remove_follow(self, cid):
        errcode = self._remove([{"cid": "{cid}".format(cid=cid)}])
        if errcode == 0:
            return True
        return False

    def reset_follow(self):
        try:
            self._reset()
            return True
        except Exception:
            print_exc()
        return False

    def verify_follow(self, cid):
        json_query = self._verify([{"cid": "{cid}".format(cid=cid)}])
        try:
            data = simplejson.loads(json_query)
            if data["vidlist"][0]["isfollow"] == 1:
                return True
        except Exception:
            log("%s verify follow failed" % cid)
        return False

    def get_follow(self):
        return simplejson.loads(self._get())

    def _add(self, vidlist, detaildata):
        cache = StorageServer2.TimedStorage("follow")
        try:
            cidlist = cache["list"]
            result = cache["followdata"]
        except Exception:
            cache["list"] = []
            cidlist = cache["list"]
            result = {}
            cache["followdata"] = result
        try:
            cid = vidlist[0]["cid"]
            if cid != '':
                result[cid] = {}
                result[cid]["cid"] = vidlist[0]["cid"]
                result[cid]["title"] = detaildata["title"]
                result[cid]["imgUrl"] = detaildata["imgUrl"]
                result[cid]["path"] = detaildata["path"]
                result[cid]["type"] = detaildata["type"]
                cache["followdata"] = result
                try:
                    del cidlist[cidlist.index(cid)]
                except Exception:
                    pass
                cidlist.insert(0, cid)
                cache["list"] = cidlist
            errcode = 0
        except Exception:
            print_exc()
            errcode = 1
        return errcode

    def _remove(self, vidlist):
        cache = StorageServer2.TimedStorage("follow")
        try:
            cidlist = cache["list"]
            del cidlist[cidlist.index(vidlist[0]["cid"])]
            cache["list"] = cidlist
        except Exception:
            print_exc()
            cache["list"] = []
        try:
            cachedata = cache["followdata"]
            del cachedata[vidlist[0]["cid"]]
            cache["followdata"] = cachedata
            errcode = 0
        except Exception:
            print_exc()
            cache["followdata"] = {}
            errcode = 1
        return errcode

    def _reset(self):
        cache = StorageServer2.TimedStorage("follow")
        cache["list"] = []
        cache["followdata"] = {}

    def _get(self):
        cache = StorageServer2.TimedStorage("follow")
        try:
            result = cache["followdata"]
            cidlist = cache["list"]
        except Exception:
            cidlist = []
            result = {}
            cache["list"] = cidlist
            cache["followdata"] = result
        vidlist = []
        for element in cidlist:
            try:
                cid = result[element]["cid"]
                if cid == "":
                    continue
                title = result[element]["title"]
                image = result[element]["imgUrl"]
                c_type = result[element]["type"]
                path = result[element]["path"]
                vidlist.append({"cid": cid,
                                "title": title,
                                "imgUrl": image,
                                "type": c_type,
                                "path": path})
            except Exception:
                print_exc()
        data = simplejson.dumps({
            "errcode": 0,
            "errmsg": "",
            "ret": 0,
            "vidlist": vidlist})
        return data

    def _verify(self, vidlist):
        cache = StorageServer2.TimedStorage("follow")
        data = {}
        cid = vidlist[0]["cid"]
        try:
            cidlist = cache["list"]
            if cid in cidlist:
                data["vidlist"] = [{"cid": cid, "isfollow": 1}]
            else:
                data["vidlist"] = [{"cid": cid, "isfollow": 0}]
        except Exception:
            data["vidlist"] = [{"cid": cid, "isfollow": 0}]
            print_exc()
        return simplejson.dumps(data)


fc = FollowClass()
