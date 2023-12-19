#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Student Name 1 (#999999)
and Student Name 2 (#999999)
"""

from GraphicsEventSystem import *

class Window:
    def __init__(self, originX, originY, width, height, identifier):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier
        self.backgroundColor = COLOR_LIGHT_GRAY
        
        self.childWindows = []
        self.parentWindow = None
    


        
    def addChildWindow(self, window):
        pass
        
    def removeFromParentWindow(self):
        pass
        
    def childWindowAtLocation(self, x, y):
        return None
    
    def hitTest(self, x, y):
        return False
    
    def convertPositionToScreen(self, x, y):
        return (0,0)
    
    def convertPositionFromScreen(self, x, y):
        return (0,0)
    
    
    def draw(self, ctx):
        pass
    
    
    
    def handleMouseClicked(self, x, y):
        print("Window " + self.identifier + " was clicked.")
        



class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1")
        self.windowSystem = windowSystem

        
    def draw(self, ctx):
        super().draw(ctx)
    