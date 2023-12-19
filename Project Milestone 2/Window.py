#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Samuel Kwong (#430273)
and Filiz Günal (#431174)
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
        self.childWindows.append(window)
        window.parentWindow = self
        
    def removeFromParentWindow(self):
        self.parentWindow.childWindows.remove(self)
        self.parentWindow = None
        
    def childWindowAtLocation(self, x, y):
        #Deepest visible descendant window
        deepestWindow = None
        for childWindow in self.childWindows:
            if childWindow.hitTest(x,y):
                deepestWindow = childWindow
        return deepestWindow

    
    def hitTest(self, x, y):
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        else:
            return False
    
    def convertPositionToScreen(self, x, y):
        pos_x = x
        pos_y = y
        currentWindow = self

        #Check if the current window is a top level window
        not_top_level_window = True
        if currentWindow.parentWindow.identifier == "SCREEN_1":
            not_top_level_window = False

        # While the window is not a top level window, go to parent window and get its x and y
        while not_top_level_window:
            # Update the current window to the parent window
            currentWindow = currentWindow.parentWindow
            pos_x += currentWindow.x
            pos_y += currentWindow.y
            # Check if the new current window is a top level window or not, if it is then we do not go back into loop next iteration
            if currentWindow.parentWindow.identifier == "SCREEN_1":
                not_top_level_window = False

        return (pos_x,pos_y)
    
    def convertPositionFromScreen(self, x, y):
        pos_x = x
        pos_y = y
        currentWindow = self

        # Check if the current window is a top level window
        not_top_level_window = True
        if currentWindow.parentWindow.identifier == "SCREEN_1":
            not_top_level_window = False

        # While the window is not a top level window, go to parent window and get its x and y
        while not_top_level_window:
            # Update the current window to the parent window
            currentWindow = currentWindow.parentWindow
            pos_x -= currentWindow.x
            pos_y -= currentWindow.y
            # Check if the new current window is a top level window or not, if it is then we do not go back into loop next iteration
            if currentWindow.parentWindow.identifier == "SCREEN_1":
                not_top_level_window = False

        return (pos_x, pos_y)
    
    
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
    