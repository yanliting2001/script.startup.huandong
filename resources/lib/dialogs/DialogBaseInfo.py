# -*- coding: utf8 -*-

import xbmc
import xbmcgui
from OnClickHandler import OnClickHandler
from common import *

ch = OnClickHandler()


class DialogBaseInfo(object):
    ACTION_PREVIOUS_MENU = [92, 9]
    ACTION_EXIT_SCRIPT = [13, 10]

    def __init__(self, *args, **kwargs):
        super(DialogBaseInfo, self).__init__(*args, **kwargs)

    def onInit(self, *args, **kwargs):
        super(DialogBaseInfo, self).onInit()
        self.window = xbmcgui.Window(self.window_id)

    def onAction(self, action):
        ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        ch.serve(control_id, self)

    def onFocus(self, control_id):
        pass

    @run_async
    def bounce(self, identifier):
        self.bouncing = True
        self.window.setProperty("Bounce.%s" % identifier, "true")
        xbmc.sleep(200)
        self.window.clearProperty("Bounce.%s" % identifier)
        self.bouncing = False

    def fill_lists(self):
        for container_id, listitems in self.listitems:
            try:
                self.getControl(container_id).reset()
                self.getControl(container_id).addItems(create_listitems(listitems))
            except Exception:
                log("Notice: No container with id %i available" % container_id)

    @ch.action("parentdir", "*")
    @ch.action("parentfolder", "*")
    def previous_menu(self):
        print "previous menu"
        self.close()
        wm.pop_stack()

    @ch.action("previousmenu", "*")
    def exit_script(self):
        self.close()
