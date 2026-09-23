
'''
___________________________________________________________
|                                                         |
|                        Imports                          |
|_________________________________________________________|

'''
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import PySide6 as Py
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 300, 750, 500)
        self.initUI()

    def initUI(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        graph = QLabel("graph", self)
        graph.setStyleSheet("backround-color: green;")
        inputs = QLabel("inputs",self)
        inputs.setStyleSheet("background-color: blue;")
        controls = QLabel("controls",self)
        controls.setStyleSheet("background-color: red;")

        vbox = QVBoxLayout()
        left_side = QHBoxLayout()
        left_side.addWidget(inputs)
        left_side.addWidget(controls)
        vbox.addWidget(left_side)
        vbox.addWidget(graph)

        central_widget.setLayout(vbox)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
