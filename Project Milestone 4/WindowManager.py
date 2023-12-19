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
        self.startMenuWidth = 60
        self.titleBarHeight = 20
        self.taskBarHeight = 40
        self.taskBarIconWidth = 120
        self.taskBarOffset = 5
        self.taskBar = [] #self.windowSystem.screen.childWindows.copy()

    # Checks if decoration on window is hit
    def hitDecorationTest(self, window, x, y):
        if window.x < x < window.x + window.width and window.y < y < window.y + self.titleBarHeight:
            return True
        else:
            return False
    # Checks if the resize tab is hit for top level window
    def hitResizeTest(self, window, x, y):
        if window.x + window.width - 10 < x < window.x + window.width and window.y + window.height - 10 < y < window.y + window.height:
            return True
        else:
            return False

    # Checks if minimize button is hit on the decoration
    def hitMinimizeTest(self, window, x, y):
        if window.x + window.width - 60 < x < window.x + window.width - 48 and window.y < y < window.y + self.titleBarHeight:
            return True
        else:
            return False

    # Checks if close button is hit on the decoration
    def hitCloseTest(self, window, x, y):
        if window.x + window.width - 20 < x < window.x + window.width - 8 and window.y < y < window.y + self.titleBarHeight:
            self.taskBar.remove(window)
            return True
        else:
            return False

    # Checks if start menu is hit on the taskbar
    def hitStartMenu(self, x, y):
        if self.windowSystem.screen.x < x < self.windowSystem.screen.x + self.startMenuWidth and self.windowSystem.screen.y + self.windowSystem.screen.height - self.taskBarHeight < y < self.windowSystem.screen.y + self.windowSystem.screen.height:
            return True
        else:
            return False

    # Checks if the taskbar is hit
    def hitTaskbar(self, x, y):
        if self.windowSystem.screen.x < x < self.windowSystem.screen.x + self.windowSystem.screen.width and self.windowSystem.screen.y + self.windowSystem.screen.height - self.taskBarHeight < y < self.windowSystem.screen.y + self.windowSystem.screen.height:
            return True
        else:
            return False

    # Checks if an app on taskbar is hit
    def hitAppInTaskbarTest(self, appIndex, app, x, y):
        if self.startMenuWidth + self.windowSystem.screen.x + self.taskBarOffset + appIndex * self.taskBarIconWidth < x < self.startMenuWidth + self.windowSystem.screen.x + self.taskBarIconWidth + appIndex * self.taskBarIconWidth and self.windowSystem.screen.y + self.windowSystem.screen.height - self.taskBarHeight + self.taskBarOffset < y < self.windowSystem.screen.y + self.windowSystem.screen.height - self.taskBarOffset:
            #app.isHidden = not app.isHidden
            return True
        else:
            return False

    # Checks to see if point is inside the screen
    def checkPointInScreen(self, px, py, screen):
        if screen.x < px < screen.x + screen.width and screen.y < py < screen.y + screen.height:
            return True
        else:
            return False

    # Checks window posiiton to make sure window decoration is always clickable
    def checkWindowPosition(self, window, x, y):
        titleBarX1 = x + self.titleBarHeight
        titleBarX2 = x + window.width - self.titleBarHeight
        titleBarY1 = y
        titleBarY2 = y + self.titleBarHeight
        #Top Left Point: titleBarX1, titleBarY1
        #Top Right Point: titleBarX2, titleBarY1
        #Bottom Left Point: titleBarX1, titleBarY2
        #Bottom Right Point: titleBarX2, titleBarY2
        if (not self.checkPointInScreen(titleBarX1, titleBarY1, self.windowSystem.screen) and
            not self.checkPointInScreen(titleBarX2, titleBarY1, self.windowSystem.screen) and
            not self.checkPointInScreen(titleBarX1, titleBarY2, self.windowSystem.screen) and
            not self.checkPointInScreen(titleBarX2, titleBarY2, self.windowSystem.screen)) or \
                titleBarY1 < self.windowSystem.screen.y or titleBarY2 > self.windowSystem.screen.y + self.windowSystem.screen.height:
            return False
        else:
            return True
    
    # Window Decoration Drawing
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
        #Draw resize indicator on bottom right
        ctx.drawLine(window.x + window.width - 10, window.y + window.height, window.x + window.width,
                     window.y + window.height - 10)
        ctx.drawLine(window.x + window.width - 6, window.y + window.height, window.x + window.width,
                     window.y + window.height - 6)
        if window.isResizing:
            ctx.drawLine(window.x + window.width - 12, window.y + window.height - 12, window.x + window.width, window.y + window.height)


    def drawDesktop(self, ctx):
        ctx.setOrigin(0, 0)
        ctx.setFillColor(COLOR_BLUE)
        ctx.fillRect(0, 0, self.windowSystem.width, self.windowSystem.height)

    def drawTaskbar(self, ctx):
        # Draw the taskbar rect
        ctx.setFillColor(COLOR_WHITE)
        ctx.fillRect(self.windowSystem.screen.x, self.windowSystem.screen.y + self.windowSystem.screen.height - self.taskBarHeight,
                     self.windowSystem.screen.x + self.windowSystem.screen.width, self.windowSystem.screen.y + self.windowSystem.screen.height)
        # Draw the start menu
        ctx.setFillColor(COLOR_DARK_BLUE)
        ctx.fillRect(self.windowSystem.screen.x,
                     self.windowSystem.screen.y + self.windowSystem.screen.height - self.taskBarHeight,
                     self.windowSystem.screen.x + self.startMenuWidth,
                     self.windowSystem.screen.y + self.windowSystem.screen.height)
        # Draw the start menu text
        ctx.setStrokeColor(COLOR_LIGHT_GRAY)
        ctx.drawString("Menu",
                       self.windowSystem.screen.x + self.taskBarOffset,
                       self.windowSystem.screen.y + self.windowSystem.screen.height - 0.75 * self.taskBarHeight)

        # Draw the task bar app icons
        for appIndex, app in enumerate(self.taskBar):
            # Default app color
            ctx.setFillColor(COLOR_LIGHT_BLUE)
            # If the window is front window and is not hidden, change color to dark blue
            if app is self.windowSystem.screen.childWindows[-1] and not app.isHidden:
                ctx.setFillColor(COLOR_BLUE)
            ctx.fillRect(self.startMenuWidth + self.windowSystem.screen.x + self.taskBarOffset + appIndex * self.taskBarIconWidth,
                         self.windowSystem.screen.y + self.windowSystem.screen.height - self.taskBarHeight + self.taskBarOffset,
                         self.startMenuWidth + self.windowSystem.screen.x + self.taskBarIconWidth + appIndex * self.taskBarIconWidth,
                         self.windowSystem.screen.y + self.windowSystem.screen.height - self.taskBarOffset)
            # Draw the app text
            ctx.setStrokeColor(COLOR_LIGHT_GRAY)
            ctx.drawString(app.identifier, self.startMenuWidth + self.windowSystem.screen.x + self.taskBarIconWidth / 5 + appIndex * self.taskBarIconWidth, self.windowSystem.screen.y + self.windowSystem.screen.height - 0.75 * self.taskBarHeight)