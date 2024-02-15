import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import Qt

from_class = uic.loadUiType("source/calculator.ui")[0] #경로설정!

#find operator function
def find_last_operator_index(expression):
    operators = {'+', '-', '*', '/'}
    for i in range(len(expression) - 1, -1, -1): #search backwards 
        if expression[i] in operators:
            return i
    return 0

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("calculator")

        self.result = 0
        self.label.setText(str(self.result))

        self.num1.clicked.connect(self.buttonClicked)
        self.num2.clicked.connect(self.buttonClicked)
        self.num3.clicked.connect(self.buttonClicked)
        self.num4.clicked.connect(self.buttonClicked)
        self.num5.clicked.connect(self.buttonClicked)
        self.num6.clicked.connect(self.buttonClicked)
        self.num7.clicked.connect(self.buttonClicked)
        self.num8.clicked.connect(self.buttonClicked)
        self.num9.clicked.connect(self.buttonClicked)
        self.num0.clicked.connect(self.buttonClicked)
        self.num_.clicked.connect(self.buttonClicked)
        self.ce.clicked.connect(self.buttonClicked)

        self.ac.clicked.connect(self.clear)

        self.minus.clicked.connect(self.minus_cal)

        self.sum.clicked.connect(self.cal)
        self.sub.clicked.connect(self.cal)
        self.prod.clicked.connect(self.cal)
        self.div.clicked.connect(self.cal)
        self.enter.clicked.connect(self.cal)

        self.percent.clicked.connect(self.per)

        self.setFocusPolicy(Qt.StrongFocus)
        self.keyPressEvent = self.on_key_press #press keyboard

    #keyboard setting
    def on_key_press(self, event):
        key = event.key()
        if 48 <= key <= 57:  # 0~9 keyboard
            button_text = str(key - 48) 
            self.buttonClickedByText(button_text) #number
        elif key == Qt.Key_Period:
            self.buttonClickedByText(".")
        elif key == Qt.Key_Backspace:
            self.buttonClickedByText("CE")
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.cal_enter("=")
        elif key == Qt.Key_Plus:
            self.buttonClickedByText("+")
        elif key == Qt.Key_Minus:
            self.buttonClickedByText("-")
        elif key == Qt.Key_Asterisk:
            self.buttonClickedByText("*")
        elif key == Qt.Key_Slash:
            self.buttonClickedByText("/")
        elif key == Qt.Key_Percent:
            self.per()

    #keybard input
    def buttonClickedByText(self, key):
        current_text = self.label.text()

        if (key == "."):  
            if (current_text == '0'): # 0.~
                new_text = '0'+ key
            elif (current_text[-1] in ['+','-','*','/']): # after the operator
                new_text = current_text+'0' + key
            elif (current_text[-1]=='.'): #if '.' exists
                new_text = current_text
            elif ('.' in current_text[find_last_operator_index(current_text):]): #If '.' exists after the operator
                new_text = current_text
            else:
                new_text = current_text + key # input '.'

        elif (key == "CE"):
            if (len(current_text) == 1):
                new_text = "0"  #set 0
            else:
                new_text = current_text[:-1] #delete last one

        elif (current_text == "0"):
            new_text = key

        elif (current_text[-1] in ['+','-','*','/']): #Operator not possible twice
            if (key in ['+','-','*','/']):
                new_text=current_text[:-1]+key
            else:
                new_text = current_text + key

        else:
            new_text = current_text + key
        self.label.setText(new_text)
        self.result = new_text

    #mouse input
    def buttonClicked(self): ###Similar to the above function
        sender = self.sender()  
        button_text = sender.text() #clicked button
        current_text = self.label.text()

        if (button_text == "."):
            if (current_text == '0'):
                new_text = '0'+ button_text
            elif (current_text[-1] in ['+','-','*','/']):
                new_text = current_text+'0' + button_text
            elif (current_text[-1]=='.'):
                new_text = current_text
            elif ('.' in current_text[find_last_operator_index(current_text):]):
                new_text = current_text
            else:
                new_text = current_text + button_text

        elif (button_text == "CE"):
            if (len(current_text) == 1):
                new_text = "0"
            else:
                new_text = current_text[:-1]

        elif (current_text == "0"):
            new_text = button_text

        else :
            new_text = current_text + button_text  
        self.label.setText(new_text)
        self.result = new_text

    # AC
    def clear(self):
        self.label.setText("0")

    # change +/-
    def minus_cal(self):
        current_text = self.label.text()
        
        if (current_text == "0"): 
            new_text = "-"
            
        elif (current_text == "-"): 
            new_text = "0"

        elif (current_text[-1]==")"): #if (-n)
            last_operator_index = find_last_operator_index(current_text) 
            new_text=current_text[:last_operator_index-1]+current_text[last_operator_index+1:-1] # (-n) -> n

        elif find_last_operator_index(current_text): #if change '+/-' after operator
            last_operator_index = find_last_operator_index(current_text)
            new_text = current_text[:last_operator_index + 1] + "(-" + current_text[last_operator_index + 1:] + ")" # n -> (-n)
        
        elif (current_text[0] == "-"): # '-' -> '+'
            new_text = current_text[1:]
        
        else:
            new_text = "-" + current_text # '+' -> '-'
        
        self.label.setText(new_text)
        self.result = new_text

    #calculation
    def cal(self):
        sender = self.sender()  
        button_text = sender.text()
        current_text = self.label.text()

        if (button_text == "="): 
            try:
                result = eval(current_text) #calculation current formula
                self.result = '{:.4f}'.format(result).rstrip('0').rstrip('.') # Maximum decimal places is 4
                self.label.setText(self.result)

            except Exception as e:
                self.label.setText(current_text) 

        else:
            try:
                new_text = self.result + button_text
                self.label.setText(new_text)
            except Exception as e:
                self.label.setText(current_text)
    # press 'Enter' key
    def cal_enter(self,key):  ###Similar to the above function
        current_text = self.label.text()

        if (key == "="):
            try:
                result = eval(current_text)
                self.result = '{:.4f}'.format(result).rstrip('0').rstrip('.')
                self.label.setText(self.result)

            except Exception as e:
                self.label.setText(current_text)

        else:
            try:
                new_text = self.result + key
                self.label.setText(new_text)

            except Exception as e:
                self.label.setText(current_text)

    # calcullation precent
    def per(self):
        current_text = self.label.text()
        p = float(current_text) / 100
        self.label.setText(str(p))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    myWindows.show()
    
    sys.exit(app.exec_())