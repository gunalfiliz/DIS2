#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Samuel Kwong (#430273)
and Filiz Günal (#431174)
"""
from collections import deque

from GraphicsEventSystem import *
from Window import *
from WindowManager import *
from UITK import *
from Apps import *
import sys

class WindowSystem(GraphicsEventSystem):
    def start(self):
        self.savedMovedButton = None
        self.deepestVisibleWindow = None
        self.isButton = False
        self.isSlider = False
        self.hitTaskbar = False
        self.firstDrag = True
        self.handleMouseDiff = 0

        # Initialize window manager
        self.windowManager = WindowManager(self)

        # Initialize Screen
        self.screen = Screen(self)

        # Set up the start menu and it's child windows
        self.startMenu = Container(0, self.screen.height - self.windowManager.taskBarHeight - 160, 120, 160,
                                   "StartMenu")
        self.startMenu.isHidden = True
        self.screen.addChildWindow(self.startMenu)

        self.helloWorldButton = Button(0, 0, 120, 40, "HelloWorldButton")
        self.helloWorldButton.text = "Hello World"
        self.helloWorldButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.helloWorldButton.action = lambda l=self.helloWorldButton.identifier: self.open_app(l)
        self.colorsButton = Button(0, 40, 120, 40, "ColorsButton")
        self.colorsButton.text = "Colors"
        self.colorsButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.colorsButton.action = lambda l=self.colorsButton.identifier: self.open_app(l)
        self.calculatorButton = Button(0, 80, 120, 40, "CalculatorButton")
        self.calculatorButton.text = "Calculator"
        self.calculatorButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.calculatorButton.action = lambda l=self.calculatorButton.identifier: self.open_app(l)
        self.shutdownButton = Button(0, 120, 120, 40, "ShutdownButton")
        self.shutdownButton.text = "Shutdown"
        self.shutdownButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.shutdownButton.action = lambda l=self.shutdownButton.identifier: self.shutdown()
        self.startMenu.addChildWindow(self.helloWorldButton)
        self.startMenu.addChildWindow(self.colorsButton)
        self.startMenu.addChildWindow(self.calculatorButton)
        self.startMenu.addChildWindow(self.shutdownButton)
        self.toggleHiddenChildren(self.startMenu, self.startMenu.isHidden)


    
    """
    WINDOW MANAGEMENT
    """

    # Called when an app is clicked on in the start menu
    def open_app(self, identifier):
        new_app = None
        existingApp = None
        if identifier == "HelloWorldButton":
            new_app = HelloWorld(100, 100, 304, 420, "HelloWorld", self)
        elif identifier == "ColorsButton":
            new_app = Colors(400, 20, 304, 420, "Colors")
        elif identifier == "CalculatorButton":
            new_app = Calculator(300, 50, 304, 420, "Calculator")

        # Checks to see if the app is already open
        for app in self.screen.childWindows:
            if app.identifier == new_app.identifier:
                existingApp = app

        # Hides the Start Menu after an action is completed in the start menu
        self.startMenu.isHidden = True
        self.toggleHiddenChildren(self.startMenu, self.startMenu.isHidden)

        # If the app is already open, then bring it to the front
        if existingApp:
            if existingApp.isHidden:
                existingApp.isHidden = False
                self.toggleHiddenChildren(existingApp, existingApp.isHidden)
            self.bringWindowToFront(existingApp)
        # Otherwise, open the app and bring it to the front
        else:
            self.screen.addChildWindow(new_app)
            self.windowManager.taskBar.append(new_app)
            self.bringWindowToFront(new_app)

    # Exit the application if shutdown button is called
    def shutdown(self):
        sys.exit()

    def createWindowOnScreen(self, x, y, width, height, identifier):
        window = Window(x, y, width, height, identifier)
        self.screen.childWindows.append(window)
        return window

    def bringWindowToFront(self, window):
        currentWindow = window

        # Check if the current window is a top level window
        is_top_level_window = False
        if currentWindow.parentWindow.identifier == "SCREEN_1":
            is_top_level_window = True

        # While the window is not a top level window, go to parent window and get its x and y
        while not is_top_level_window:
            # Update the current window to the parent window
            currentWindow = currentWindow.parentWindow
            # Check if the new current window is a top level window or not, if it is then we do not go back into loop next iteration
            if currentWindow.parentWindow.identifier == "SCREEN_1":
                is_top_level_window = True

        self.screen.childWindows.append(self.screen.childWindows.pop(self.screen.childWindows.index(currentWindow)))
        self.requestRepaint()

    # When hiding a top level window, this is also called to hide all child windows
    def toggleHiddenChildren(self, window, flag):
        windowStack = deque([])
        preordered_windows = []
        preordered_windows.append(window.identifier)
        windowStack.append(window)
        while len(windowStack) > 0:
            visited = False
            # Window at the top of the stack has no children
            if len((windowStack[len(windowStack) - 1]).childWindows) == 0:
                windowStack.pop()
            # Window at the top of the stack has children
            else:
                parentWindow = windowStack[len(windowStack) - 1]
            # If child window has not been visited, then push to stack and to the preordered windows list
            if len(windowStack) > 0:
                for i in range(0, len(parentWindow.childWindows)):
                    if parentWindow.childWindows[i].identifier not in preordered_windows:
                        visited = True
                        windowStack.append(parentWindow.childWindows[i])
                        preordered_windows.append(parentWindow.childWindows[i].identifier)
                        parentWindow.childWindows[i].isHidden = flag
                        break
                if not visited:
                    windowStack.pop()


    
    
    """
    DRAWING
    """

    def handlePaint(self):
        self.screen.draw(self.graphicsContext)
        windowStack = deque([])
        preordered_windows = []
        preordered_windows.append(self.screen.identifier)
        windowStack.append(self.screen)
        while len(windowStack) > 0:
            visited = False
            # Window at the top of the stack has no children
            if len((windowStack[len(windowStack) - 1]).childWindows) == 0:
                windowStack.pop()
            # Window at the top of the stack has children
            else:
                parentWindow = windowStack[len(windowStack) - 1]
            # If child window has not been visited, then push to stack and to the preordered windows list
            # Paint it on the screen, relative to the parent window, break out of loop and
            if len(windowStack) > 0:
                for i in range(0, len(parentWindow.childWindows)):
                    if parentWindow.childWindows[i].identifier not in preordered_windows:
                        visited = True
                        windowStack.append(parentWindow.childWindows[i])
                        preordered_windows.append(parentWindow.childWindows[i].identifier)
                        # Draw the window if it is visible
                        if not parentWindow.childWindows[i].isHidden:
                            parentWindow.childWindows[i].draw(self.graphicsContext)
                            # if top level window, also draw decoration
                            if parentWindow is self.screen:
                                self.windowManager.decorateWindow(parentWindow.childWindows[i], self.graphicsContext)
                        break
                if not visited:
                    windowStack.pop()

    
    """
    INPUT EVENTS
    """



    def handleMousePressed(self, x, y):
        self.initialMousePosX = x
        self.mousePosX = x
        self.initialMousePosY = y
        self.mousePosY = y
        # Get the deepest visible window
        self.deepestVisibleWindow = self.screen.childWindowAtLocation(x,y)
        if self.deepestVisibleWindow:
            self.initialDeepestVisibleWindowX = self.deepestVisibleWindow.x
            self.initialDeepestVisibleWindowY = self.deepestVisibleWindow.y
            # Check if the mouse pointer press is on a button
            if type(self.deepestVisibleWindow) is Button:
                self.isButton = True
                self.deepestVisibleWindow.ButtonState = ButtonState.PRESSED
                self.requestRepaint()
            # Check if the mouse pointer press is on the slider handle
            elif type(self.deepestVisibleWindow) is Slider:
                self.isSlider = True
                self.deepestVisibleWindow.SliderState = SliderState.PRESSED
                self.requestRepaint()
            # Check if the mouse pointer press is on the window decoration
            elif self.windowManager.hitDecorationTest(self.deepestVisibleWindow, x, y):
                self.deepestVisibleWindow.isDraggable = True
            # Check if mouse pointer press is on the resize
            elif self.windowManager.hitResizeTest(self.deepestVisibleWindow, x, y):
                self.deepestVisibleWindow.isResizing = True
            # Bring window to front
            self.bringWindowToFront(self.deepestVisibleWindow)
        elif self.windowManager.hitTaskbar(x,y):
           self.hitTaskbar = True

        
    def handleMouseReleased(self, x, y):
        # Check if a window was clicked
        if self.deepestVisibleWindow:
            # if initial mouse pos and current mouse position is same
            if self.initialMousePosX == self.mousePosX and self.initialMousePosY == self.mousePosY:
                self.deepestVisibleWindow.handleMouseClicked(x, y)
                # if button is clicked, perform action
                if self.isButton:
                    self.deepestVisibleWindow.action()
                # if the decoration bar is clicked
                if self.deepestVisibleWindow.isDraggable:
                    # if minimize button is pressed
                    if self.windowManager.hitMinimizeTest(self.deepestVisibleWindow, x, y):
                        self.deepestVisibleWindow.isHidden = True
                        self.toggleHiddenChildren(self.deepestVisibleWindow, self.deepestVisibleWindow.isHidden)
                    # if close button is pressed
                    elif self.windowManager.hitCloseTest(self.deepestVisibleWindow, x, y):
                        self.deepestVisibleWindow.removeFromParentWindow()
            # Slider is being dragged
            elif self.isSlider:
                self.deepestVisibleWindow.value = (self.deepestVisibleWindow.handleX) / (self.deepestVisibleWindow.width - self.deepestVisibleWindow.handleWidth)
                self.deepestVisibleWindow.action(self.deepestVisibleWindow.value)
                self.firstDrag = True
            # Reset buttons and sliders
            if self.isButton:
                self.deepestVisibleWindow.ButtonState = ButtonState.NORMAL
            if self.isSlider:
                self.deepestVisibleWindow.SliderState = SliderState.NORMAL
            self.requestRepaint()
            if self.deepestVisibleWindow:
                self.deepestVisibleWindow.isDraggable = False
                self.deepestVisibleWindow.isResizing = False
            self.deepestVisibleWindow = None
            self.isButton = False
            self.isSlider = False
        # initial mouse press was on the task bar
        elif self.hitTaskbar:
            # mouse was released on the task bar
            if self.initialMousePosX == self.mousePosX and self.initialMousePosY == self.mousePosY:
                # Check if mouse clicked on start menu
                if self.windowManager.hitStartMenu(x, y):
                    self.startMenu.isHidden = not self.startMenu.isHidden
                    self.toggleHiddenChildren(self.startMenu, self.startMenu.isHidden)
                    if not self.startMenu.isHidden:
                        self.bringWindowToFront(self.startMenu)
                else:
                    # check if mouse clicked on an app icon
                    for appIndex, app in enumerate(self.windowManager.taskBar):
                        if self.windowManager.hitAppInTaskbarTest(appIndex, app, x, y):
                            appWindowIdx = self.screen.childWindows.index(app)
                            appWindow = self.screen.childWindows[appWindowIdx]
                            # if window is in background and not hidden, then bring to foreground
                            # if window is hidden, make it not hidden and bring to foreground
                            if appWindow.isHidden:
                                appWindow.isHidden = False
                                self.toggleHiddenChildren(appWindow, appWindow.isHidden)
                            self.bringWindowToFront(appWindow)
                self.requestRepaint()
            self.hitTaskbar = False


        
    def handleMouseMoved(self, x, y):
        self.deepestVisibleWindow = self.screen.childWindowAtLocation(x, y)
        # Reset the most recent button that was hovered over to its normal state if it is no longer being hovered over
        if self.savedMovedButton:
            if self.savedMovedButton is not self.deepestVisibleWindow:
                self.savedMovedButton.ButtonState = ButtonState.NORMAL
        if self.deepestVisibleWindow:
            # Save the most recent button that is being hovered over to later reset it when it is out of scope
            if type(self.deepestVisibleWindow) is Button:
                self.deepestVisibleWindow.ButtonState = ButtonState.HOVERING
                self.savedMovedButton = self.deepestVisibleWindow
            # The cursor is over the resize tab, set flag to window manager can draw the select marker
            if self.windowManager.hitResizeTest(self.deepestVisibleWindow, x, y):
                self.deepestVisibleWindow.isResizing = True
            else:
                self.deepestVisibleWindow.isResizing = False
        #else:
           #self.isResizing = False
        self.requestRepaint()
        
    def handleMouseDragged(self, x, y):
        if self.deepestVisibleWindow:
            cursorDiffX = x - self.mousePosX
            cursorDiffY = y - self.mousePosY
            # Check if the mouse is dragging a slider
            if self.isSlider:
                localX, localY = self.deepestVisibleWindow.convertPositionFromScreen(x, y)
                # For the first drag, add the offset between the handle of the slider and the pointer of the mouse cursor so they match
                if self.firstDrag:
                    localMousePosX, localMousePosY = self.deepestVisibleWindow.convertPositionFromScreen(self.mousePosX, self.mousePosY)
                    self.handleMouseDiff = localMousePosX - self.deepestVisibleWindow.handleX
                    self.firstDrag = False
                # If the handle of the slider exceeds the slider box, prevent it from going further
                if localX - self.handleMouseDiff >= self.deepestVisibleWindow.x + self.deepestVisibleWindow.width - self.deepestVisibleWindow.handleWidth:
                    self.deepestVisibleWindow.handleX = self.deepestVisibleWindow.x + self.deepestVisibleWindow.width - self.deepestVisibleWindow.handleWidth
                elif localX - self.handleMouseDiff <= self.deepestVisibleWindow.x + self.deepestVisibleWindow.handleOffset:
                    self.deepestVisibleWindow.handleX = self.deepestVisibleWindow.x
                # otherwise, update the position of the slider handle real time with the mouse cursor
                else:
                    self.deepestVisibleWindow.handleX = localX - self.handleMouseDiff
                # Update the value of the slider dependent on the handle position
                self.deepestVisibleWindow.value = (self.deepestVisibleWindow.handleX) / (self.deepestVisibleWindow.width - self.deepestVisibleWindow.handleWidth)
                # Perform action with the slider
                self.deepestVisibleWindow.action(self.deepestVisibleWindow.value)
                self.requestRepaint()
            # Check if the top level window is being dragged or resized
            elif self.deepestVisibleWindow.isDraggable or self.deepestVisibleWindow.isResizing:
                newWindowX = self.deepestVisibleWindow.x
                newWindowY = self.deepestVisibleWindow.y
                newWindowWidth = self.deepestVisibleWindow.width
                newWindowHeight = self.deepestVisibleWindow.height
                # If top level window is being dragged, update it's new position
                if self.deepestVisibleWindow.isDraggable:
                    newWindowX = self.deepestVisibleWindow.x + cursorDiffX
                    newWindowY = self.deepestVisibleWindow.y + cursorDiffY
                    # Make sure the new position is valid
                    if self.windowManager.checkWindowPosition(self.deepestVisibleWindow, newWindowX, newWindowY):
                        self.deepestVisibleWindow.x = newWindowX
                        self.deepestVisibleWindow.y = newWindowY
                        self.requestRepaint()
                # if top level window is being resized, update it's position and size
                elif self.deepestVisibleWindow.isResizing:
                    newWindowWidth = self.deepestVisibleWindow.width + cursorDiffX
                    newWindowHeight = self.deepestVisibleWindow.height + cursorDiffY
                    self.deepestVisibleWindow.resize(newWindowX, newWindowY, newWindowWidth, newWindowHeight)
                    self.requestRepaint()

            self.mousePosX = x
            self.mousePosY = y


    # Used to detect keys for the Calculator App
    def handleKeyPressed(self, char):
        if self.screen.childWindows:
            if self.screen.childWindows[-1]:
                app = self.screen.childWindows[-1]
                if app.identifier == "Calculator" and not app.isHidden:
                    match char:
                        case '0':
                            app.zeroButton.action()
                            self.requestRepaint()
                        case '1':
                            app.oneButton.action()
                            self.requestRepaint()
                        case '2':
                            app.twoButton.action()
                            self.requestRepaint()
                        case '3':
                            app.threeButton.action()
                            self.requestRepaint()
                        case '4':
                            app.fourButton.action()
                            self.requestRepaint()
                        case '5':
                            app.fiveButton.action()
                            self.requestRepaint()
                        case '6':
                            app.sixButton.action()
                            self.requestRepaint()
                        case '7':
                            app.sevenButton.action()
                            self.requestRepaint()
                        case '8':
                            app.eightButton.action()
                            self.requestRepaint()
                        case '9':
                            app.nineButton.action()
                            self.requestRepaint()
                        case '-':
                            app.subButton.action()
                            self.requestRepaint()
                        case '+':
                            app.addButton.action()
                            self.requestRepaint()
                        case '*':
                            app.mulButton.action()
                            self.requestRepaint()
                        case '/':
                            app.divButton.action()
                            self.requestRepaint()
                        case '.':
                            app.decButton.action()
                            self.requestRepaint()
                        case '%':
                            app.modButton.action()
                            self.requestRepaint()
        
    
    
        
    
# Let's start your window system!
w = WindowSystem(800,600)