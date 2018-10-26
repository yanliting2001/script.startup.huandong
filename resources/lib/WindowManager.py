# -*- coding: utf8 -*-

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
HOME_XML = "script-Home.xml"
MOVIE_DETAIL_XML = "script-DialogVideoDetail.xml"
FOLLOW_XML = "script-DialogFollow.xml"


class WindowManager(object):

    def __init__(self):
        self.window_stack = []

    def add_to_stack(self, window):
        """
        add window / dialog to global window stack
        """
        self.window_stack.append(window)

    def pop_stack(self):
        """
        get newest item from global window stack
        """
        if self.window_stack:
            dialog = self.window_stack.pop()
            xbmc.sleep(300)
            dialog.doModal()

    def open_home(self, prev_window=None):
        """
        open home, deal with window stack
        """
        from WindowHome import WindowHome
        dialog = WindowHome(HOME_XML, ADDON_PATH)
        self.open_dialog(dialog, prev_window)

    def open_movie_detail(self, prev_window=None, title=None, video_id=None):
        """
        open movie detail, deal with window stack
        """
        from WindowMovieDetail import WindowMovieDetail
        dialog = WindowMovieDetail(MOVIE_DETAIL_XML, ADDON_PATH, title=title, video_id=video_id)
        self.open_dialog(dialog, prev_window)

    def open_follow(self, prev_window=None):
        """
        open follow, deal with window stack
        """
        from WindowFollow import WindowFollow
        dialog = WindowFollow(FOLLOW_XML, ADDON_PATH)
        self.open_dialog(dialog, prev_window)

    def open_dialog(self, dialog, prev_window):
        if dialog:
            if prev_window:
                self.add_to_stack(prev_window)
                prev_window.close()
            dialog.doModal()
            self.pop_stack()
        else:
            pass


wm = WindowManager()
