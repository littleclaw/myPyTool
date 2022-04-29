# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(432, 270)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(20, 60, 391, 192))
        self.tableView.setObjectName("tableView")
        self.getButton = QtWidgets.QPushButton(self.centralwidget)
        self.getButton.setGeometry(QtCore.QRect(20, 20, 75, 23))
        self.getButton.setObjectName("getButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(340, 20, 75, 23))
        self.saveButton.setObjectName("saveButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "wifi tool"))
        self.getButton.setText(_translate("MainWindow", "获取"))
        self.saveButton.setText(_translate("MainWindow", "保存"))
