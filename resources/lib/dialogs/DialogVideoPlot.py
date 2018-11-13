# -*- coding: utf8 -*-

from DialogBaseInfo import DialogBaseInfo
from BaseClasses import DialogXML
from OnClickHandler import OnClickHandler

ch = OnClickHandler()
C_TEXTBOX_PLOT = 40000


class DialogVideoPlot(DialogXML, DialogBaseInfo):

    def __init__(self, *args, **kwargs):
        super(DialogVideoPlot, self).__init__()
        self.plot = kwargs.get("plot")

    def onInit(self):
        # super(DialogVideoPlot, self).onInit()
        self.getControl(C_TEXTBOX_PLOT).setText(self.plot)

    def onAction(self, action):
        super(DialogVideoPlot, self).onAction(action)
        ch.serve_action(action, self.getFocusId(), self)

    def onClick(self, control_id):
        super(DialogVideoPlot, self).onClick(control_id)
        ch.serve(control_id, self)
