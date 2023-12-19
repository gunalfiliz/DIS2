#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Samuel Kwong (#430273)
and Filiz Günal (#431174)
"""

from GraphicsEventSystem import *
from Window import *

class WindowManager:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        self.titleBarHeight = 20
        self.taskBarHeight = 40
        #self.taskBar = self.
        self.taskBar = self.windowSystem.screen.childWindows.copy()

    def hitDecorationTest(self, window, x, y):
        if window.x < x < window.x + window.width and window.y < y < window.y + self.titleBarHeight:
            return True
        else:
            return False

    def hitMinimizeTest(self, window, x, y):
        if window.x + window.width - 60 < x < window.x + window.width - 48 and window.y < y < window.y + self.titleBarHeight:
            return True
        else:
            return False

    def hitCloseTest(self, window, x, y):
        if window.x + window.width - 20 < x < window.x + window.width - 8 and window.y < y < window.y + self.titleBarHeight:
            return True
        else:
            return False

    def checkPointInScreen(self, px, py, screen):
        if screen.x < px < screen.x + screen.width and screen.y < py < screen.y + screen.height:
            return True
        else:
            return False

    def checkWindowPosition(self, window, x, y):
        titleBarX1 = x
        titleBarX2 = x + window.width
        titleBarY1 = y
        titleBarY2 = y + self.titleBarHeight
        #Top Left Point: titleBarX1, titleBarY1
        #Top Right Point: titleBarX2, titleBarY1
        #Bottom Left Point: titleBarX1, titleBarY2
        #Bottom Right Point: titleBarX2, titleBarY2
        if (self.checkPointInScreen(titleBarX1, titleBarY1, self.windowSystem.screen) or
            self.checkPointInScreen(titleBarX2, titleBarY1, self.windowSystem.screen) or
            self.checkPointInScreen(titleBarX1, titleBarY2, self.windowSystem.screen) or
            self.checkPointInScreen(titleBarX2, titleBarY2, self.windowSystem.screen)):
            return True
        else:
            return False
    
    
    def decorateWindow(self, window, ctx):
        #Draw the title bar rect
        ctx.setFillColor(COLOR_LIGHT_BLUE)
        # If the window is front window, change color to dark blue
        if window is self.windowSystem.screen.childWindows[-1]:
            ctx.setFillColor(COLOR_BLUE)
        ctx.fillRect(window.x, window.y, window.x + window.width, window.y + self.titleBarHeight)
        #Draw the title bar text
        ctx.setStrokeColor(COLOR_WHITE)
        ctx.drawString(window.identifier, window.x + 2, window.y + 2)
        #Draw the minimze button
        ctx.drawLine(window.x + window.width - 60, window.y + 10, window.x + window.width - 48, window.y + 10)
        #Draw the Maximize button
        ctx.drawLine(window.x + window.width - 40, window.y + 4, window.x + window.width - 28, window.y + 4)
        ctx.drawLine(window.x + window.width - 40, window.y + 16, window.x + window.width - 28, window.y + 16)
        ctx.drawLine(window.x + window.width - 40, window.y + 4, window.x + window.width - 40, window.y + 16)
        ctx.drawLine(window.x + window.width - 28, window.y + 4, window.x + window.width - 28, window.y + 16)
        #Draw the exit button
        ctx.drawLine(window.x + window.width - 20, window.y + 4, window.x + window.width - 8, window.y + 16)
        ctx.drawLine(window.x + window.width - 20, window.y + 16, window.x + window.width - 8, window.y + 4)
        #Draw border last
        ctx.setStrokeColor(COLOR_GRAY)
        ctx.strokeRect(window.x, window.y, window.x + window.width, window.y + window.height)

    
    def drawDesktop(self, ctx):
        ctx.setOrigin(0, 0)
        ctx.setFillColor(COLOR_BLUE)
        ctx.fillRect(0, 0, self.windowSystem.width, self.windowSystem.height)
    
    
    def drawTaskbar(self, ctx):
        # Draw the taskbar rect
        ctx.setFillColor(COLOR_WHITE)
        ctx.fillRect(self.windowSystem.screen.x, self.windowSystem.screen.y + self.windowSystem.screen.height - self.taskBarHeight,
                     self.windowSystem.screen.x + self.windowSystem.screen.width, self.windowSystem.screen.y + self.windowSystem.screen.height)
        for appIndex, app in enumerate(self.taskBar):
            # Default app color
            ctx.setFillColor(COLOR_LIGHT_BLUE)
            # If the window is front window, change color to dark blue
            if app is self.windowSystem.screen.childWindows[-1]:
                ctx.setFillColor(COLOR_BLUE)
            ctx.fillRect(self.windowSystem.screen.x + 5 + appIndex * 40,
                         self.windowSystem.screen.y + self.windowSystem.screen.height - 35,
                         self.windowSystem.screen.x + 40 + appIndex * 40,
                         self.windowSystem.screen.y + self.windowSystem.screen.height - 5)
            # Draw the app text
            ctx.setStrokeColor(COLOR_LIGHT_GRAY)
            ctx.drawString(app.identifier[0], self.windowSystem.screen.x + 18 + appIndex * 40, self.windowSystem.screen.y + self.windowSystem.screen.height - 30)