# -*- coding: utf8 -*-

import xbmcgui
from OnClickHandler import OnClickHandler
from dialogs.DialogBaseInfo import DialogBaseInfo

ch = OnClickHandler()
C_LIST_NAVIGATION = 9000


class WindowHome(xbmcgui.WindowXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(WindowHome, self).__init__(*args, **kwargs)

    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())

    def onAction(self, action):
        if (action.getId() == 10 or action.getId() == 92):
            self.setFocus(self.getControl(C_LIST_NAVIGATION))
        else:
            super(WindowHome, self).onAction(action)
            ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(WindowHome, self).onClick(control_id)
        ch.serve(control_id, self)
