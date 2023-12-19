from GraphicsEventSystem import *
from Window import *
from WindowManager import *
from UITK import *
import re

"""
Apps - Submission
by  Samuel Kwong (#430273)
and Filiz Günal (#431174)
"""

class HelloWorld(Window):
    def __init__(self, originX, originY, width, height, identifier, windowSystem):
        super().__init__(originX, originY, width, height, identifier)
        self.language_dict = {
            'Deutsch': 'Guten Tag',
            'English': 'Hello',
            'Français': 'Bonjour',
        }

        # Initialize Langauge Options
        self.language_options = ['Deutsch', 'English', 'Français']
        self.windowSystem = windowSystem
        self.backgroundColor = COLOR_LIGHT_GRAY
        self.language_string = "Please select a language."

        # Set up UI
        self.container = Container(width/6, 40, 200, 200, "Hello World Container")
        # Greeting Lable
        self.greetingLabel = Label(0, 0, 200, 40, self.language_string)
        self.greetingLabel.text = self.language_string
        self.greetingLabel.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        # German Button
        self.deutschButton = Button(0, 50, 200, 40, self.language_options[0])
        self.deutschButton.text = self.language_options[0]
        self.deutschButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.deutschButton.action = lambda l=self.deutschButton.text: self.change_label(l)
        # English Button
        self.englishButton = Button(0, 100, 200, 40, self.language_options[1])
        self.englishButton.text = self.language_options[1]
        self.englishButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.englishButton.action = lambda l=self.englishButton.text: self.change_label(l)
        # French Button
        self.frenchButton = Button(0, 150, 200, 40, self.language_options[2])
        self.frenchButton.text = self.language_options[2]
        self.frenchButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.frenchButton.action = lambda l=self.frenchButton.text: self.change_label(l)
        # Quit Button
        self.quitButton = Button(self.width - 50, self.height - 40, 40, 30, "Quit")
        self.quitButton.text = "Quit"
        self.quitButton.layoutAnchors = LayoutAnchor.bottom | LayoutAnchor.right
        self.quitButton.action = lambda l=1: self.quit_window()

        self.addChildWindow(self.container)
        self.addChildWindow(self.quitButton)
        self.container.addChildWindow(self.greetingLabel)
        self.container.addChildWindow(self.deutschButton)
        self.container.addChildWindow(self.englishButton)
        self.container.addChildWindow(self.frenchButton)


    # Function to change the greeting label when a language is selected
    def change_label(self, language_option):
        self.language_string = self.language_dict[language_option]
        self.greetingLabel.text = self.language_string

    # Function to quit window when quit button is clicked
    def quit_window(self):
        self.removeFromParentWindow()
        self.windowSystem.windowManager.taskBar.remove(self)

    def draw(self, ctx):
        super().draw(ctx)

class Colors(Window):
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_LIGHT_GRAY

        # Slider Container
        self.container = Container(width / 6, 40, 200, 200, "Slider Container")
        self.r_value = 0
        self.b_value = 0
        self.g_value = 0
        self.hexString = "#000000"

        # Color label that is updated by the sliders
        self.colorLabel = Label(0, 0, 200, 40, "Color Label")
        self.colorLabel.text = self.hexString
        self.colorLabel.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.colorLabel.textColor = "#FFFFFF"
        self.colorLabel.font_size = 22
        self.colorLabel.backgroundColor = "#000000"

        # Initialize Color Sliders
        self.rSlider = Slider(0, 50, 200, 40, "R")
        self.rSlider.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.rSlider.action = lambda x: self.change_r_value(x)
        self.gSlider = Slider(0, 100, 200, 40, "G")
        self.gSlider.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.gSlider.action = lambda x: self.change_g_value(x)
        self.bSlider = Slider(0, 150, 200, 40, "B")
        self.bSlider.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.bSlider.action = lambda x: self.change_b_value(x)
        self.addChildWindow(self.container)
        self.container.addChildWindow(self.colorLabel)
        self.container.addChildWindow(self.rSlider)
        self.container.addChildWindow(self.gSlider)
        self.container.addChildWindow(self.bSlider)

    def rgb_to_hex(self, r, g, b):
        return '#{:02X}{:02X}{:02X}'.format(r, g, b)

    def change_r_value(self, value):
        self.r_value = int(value * 255.0)
        self.hexString = self.rgb_to_hex(self.r_value, self.g_value, self.b_value)
        self.update_color()

    def change_g_value(self, value):
        self.g_value = int(value * 255.0)
        self.hexString = self.rgb_to_hex(self.r_value, self.g_value, self.b_value)
        self.update_color()

    def change_b_value(self, value):
        self.b_value = int(value * 255.0)
        self.hexString = self.rgb_to_hex(self.r_value, self.g_value, self.b_value)
        self.update_color()

    def update_color(self):
        if not self.r_value < 122.5 or not self.g_value < 122.5 or not self.b_value < 122.5:
            self.colorLabel.textColor = "#000000"
        else:
            self.colorLabel.textColor = "#FFFFFF"
        self.colorLabel.text = self.hexString
        self.colorLabel.backgroundColor = self.hexString

    def draw(self, ctx):
        super().draw(ctx)


class Calculator(Window):
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_LIGHT_GRAY

        # Create the grid Container, vertical container with horizontal containers
        self.grid = Container(0, 20, 304, 380, "Grid")
        self.grid.axis = ContainerAxis.VERTICAL

        # All input shows up here
        self.calcLabel = Label(0, 0, 304, 80, "CalculatorInput")
        self.calcLabel.text = ""
        self.calcLabel.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.grid.addChildWindow(self.calcLabel)

        # Clear Button
        self.clearButton = Button(0, 0, 76, 60, "C Button")
        self.clearButton.text = "C"
        self.clearButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.clearButton.action = lambda l=1: self.clear()

        # Sign Button
        self.signButton = Button(76, 0, 76, 60, "+/- Button")
        self.signButton.text = "+/-"
        self.signButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.signButton.action = lambda l=1: self.changeSign()

        # Mod Button
        self.modButton = Button(152, 0, 76, 60, "% Button")
        self.modButton.text = "%"
        self.modButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.modButton.action = lambda l=self.modButton.text: self.input(l)

        # Div Button
        self.divButton = Button(228, 0, 76, 60, "/ Button")
        self.divButton.text = "/"
        self.divButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.divButton.action = lambda l=self.divButton.text: self.input(l)

        # Layout these buttons in the first row
        self.row1 = Container(0, 80, 304, 60, "Row 1")
        self.row1.axis = ContainerAxis.HORIZONTAL
        self.row1.addChildWindow(self.clearButton)
        self.row1.addChildWindow(self.signButton)
        self.row1.addChildWindow(self.modButton)
        self.row1.addChildWindow(self.divButton)

        # 7 Button
        self.sevenButton = Button(0, 0, 76, 60, "7 Button")
        self.sevenButton.text = "7"
        self.sevenButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.sevenButton.action = lambda l=self.sevenButton.text: self.input(l)

        # 8 Button
        self.eightButton = Button(76, 0, 76, 60, "8 Button")
        self.eightButton.text = "8"
        self.eightButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.eightButton.action = lambda l=self.eightButton.text: self.input(l)

        # 9 Button
        self.nineButton = Button(152, 0, 76, 60, "9 Button")
        self.nineButton.text = "9"
        self.nineButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.nineButton.action = lambda l=self.nineButton.text: self.input(l)

        # * Button
        self.mulButton = Button(228, 0, 76, 60, "* Button")
        self.mulButton.text = "*"
        self.mulButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.mulButton.action = lambda l=self.mulButton.text: self.input(l)

        # Layout these buttons in the second row
        self.row2 = Container(0, 140, 304, 60, "Row 2")
        self.row2.axis = ContainerAxis.HORIZONTAL
        self.row2.addChildWindow(self.sevenButton)
        self.row2.addChildWindow(self.eightButton)
        self.row2.addChildWindow(self.nineButton)
        self.row2.addChildWindow(self.mulButton)

        # 4 button
        self.fourButton = Button(0, 0, 76, 60, "4 Button")
        self.fourButton.text = "4"
        self.fourButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.fourButton.action = lambda l=self.fourButton.text: self.input(l)

        # 5 Button
        self.fiveButton = Button(76, 0, 76, 60, "5 Button")
        self.fiveButton.text = "5"
        self.fiveButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.fiveButton.action = lambda l=self.fiveButton.text: self.input(l)

        # 6 Button
        self.sixButton = Button(152, 0, 76, 60, "6 Button")
        self.sixButton.text = "6"
        self.sixButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.sixButton.action = lambda l=self.sixButton.text: self.input(l)

        # 7 Button
        self.subButton = Button(228, 0, 76, 60, "- Button")
        self.subButton.text = "-"
        self.subButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.subButton.action = lambda l=self.subButton.text: self.input(l)

        # Layout these buttons in the third row
        self.row3 = Container(0, 200, 304, 60, "Row 3")
        self.row3.axis = ContainerAxis.HORIZONTAL
        self.row3.addChildWindow(self.fourButton)
        self.row3.addChildWindow(self.fiveButton)
        self.row3.addChildWindow(self.sixButton)
        self.row3.addChildWindow(self.subButton)

        # 1 Button
        self.oneButton = Button(0, 0, 76, 60, "1 Button")
        self.oneButton.text = "1"
        self.oneButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.oneButton.action = lambda l=self.oneButton.text: self.input(l)

        # 2 Button
        self.twoButton = Button(76, 0, 76, 60, "2 Button")
        self.twoButton.text = "2"
        self.twoButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.twoButton.action = lambda l=self.twoButton.text: self.input(l)

        # 3 Button
        self.threeButton = Button(152, 0, 76, 60, "3 Button")
        self.threeButton.text = "3"
        self.threeButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.threeButton.action = lambda l=self.threeButton.text: self.input(l)

        # + Button
        self.addButton = Button(228, 0, 76, 60, "+ Button")
        self.addButton.text = "+"
        self.addButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.addButton.action = lambda l=self.addButton.text: self.input(l)

        # Layout these buttons in the fourth row
        self.row4 = Container(0, 260, 304, 60, "Row 4")
        self.row4.axis = ContainerAxis.HORIZONTAL
        self.row4.addChildWindow(self.oneButton)
        self.row4.addChildWindow(self.twoButton)
        self.row4.addChildWindow(self.threeButton)
        self.row4.addChildWindow(self.addButton)

        # Filler label
        self.emptyLabel = Label(0, 0, 76, 60, "empty")
        self.emptyLabel.text = ""
        self.emptyLabel.backgroundColor = COLOR_GRAY
        self.emptyLabel.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right

        # 0 Button
        self.zeroButton = Button(76, 0, 76, 60, "0 Button")
        self.zeroButton.text = "0"
        self.zeroButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.zeroButton.action = lambda l=self.zeroButton.text: self.input(l)

        # Dec Button
        self.decButton = Button(152, 0, 76, 60, ". Button")
        self.decButton.text = "."
        self.decButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.decButton.action = lambda l=self.decButton.text: self.input(l)

        # Equal Button, calls function to evaluate the expression
        self.equalButton = Button(228, 0, 76, 60, "= Button")
        self.equalButton.text = "="
        self.equalButton.layoutAnchors = LayoutAnchor.top | LayoutAnchor.bottom | LayoutAnchor.left | LayoutAnchor.right
        self.equalButton.action = lambda l=1: self.equal()

        # Layout these buttons in the fifth row
        self.row5 = Container(0, 320, 304, 60, "Row 5")
        self.row5.axis = ContainerAxis.HORIZONTAL
        self.row5.addChildWindow(self.emptyLabel)
        self.row5.addChildWindow(self.zeroButton)
        self.row5.addChildWindow(self.decButton)
        self.row5.addChildWindow(self.equalButton)

        self.grid.addChildWindow(self.row1)
        self.grid.addChildWindow(self.row2)
        self.grid.addChildWindow(self.row3)
        self.grid.addChildWindow(self.row4)
        self.grid.addChildWindow(self.row5)
        self.addChildWindow(self.grid)

    # Updates the expression that will be evaluated
    def input(self, number):
        self.calcLabel.text += number

    # the +/- button changes sign of the last number in the expression
    def changeSign(self):
        if len(self.calcLabel.text) > 0:
            if self.calcLabel.text[-1].isdigit():
                m = re.search(r'[0-9]*[.]{0,1}[0-9]*$', self.calcLabel.text)
                print(m.group())
                # if the string ends in digits m will be a Match object, or None otherwise.
                if m is not None:
                    index = self.calcLabel.text.rindex(m.group())
                    # if the char before the last number is a - sign then remove it from the last number in the string
                    if self.calcLabel.text[index - 1] == '-':
                        # if there is a digit before the - sign, then it is a subtract symbol and do not remove it
                        if self.calcLabel.text[index - 2].isdigit():
                            return
                        self.calcLabel.text = self.calcLabel.text[:index-1] + self.calcLabel.text[index:]
                    # otherwise, add a - sign before the last number in the string
                    else:
                        self.calcLabel.text = self.calcLabel.text[:index] + '-' + self.calcLabel.text[index:]


    # Try to evaluate teh expression but if it does not evaluate, return syntax error to the user
    def equal(self):
        try:
            result = str(eval(self.calcLabel.text))
            self.calcLabel.text = result
        except:
            self.calcLabel.text = "SYNTAX ERROR"

    # Clear the input label
    def clear(self):
        self.calcLabel.text = ""
    def draw(self, ctx):
        super().draw(ctx)