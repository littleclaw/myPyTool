# -*- coding: utf-8 -*-
import re
import subprocess
import sys

import xlwt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Ui_wifi_tool import Ui_MainWindow


class MyPyQT_Form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 设置 TableView
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['账号', '密码'])
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 宽度自适应
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格只读
        self.tableView.show()

        # 表格
        self.workbook = xlwt.Workbook(encoding='ascii')
        self.worksheet = self.workbook.add_sheet('data')

        self.getButton.clicked.connect(self.get_wifi_info_butt)
        self.saveButton.clicked.connect(self.save_wifi_info_butt)

    def get_wifi_info_butt(self):
        # 获取本机下存在的 profile
        profiles = subprocess.run(["netsh", "wlan", "show", "profiles"], shell=False,
                                  capture_output=True).stdout.decode('gbk')

        # 将 profile 中的 wifi 名取出
        wifi_names = (re.findall("所有用户配置文件 : (.*)\r", profiles))
        row = 0
        for wifi_name in wifi_names:
            column = 0
            item = QStandardItem('%s' % wifi_name)
            self.model.setItem(row, column, item)
            self.worksheet.write(row, column, wifi_name)

            # 获取 profile 中的密码
            profile_info = subprocess.run(["netsh", "wlan", "show", "profiles", wifi_name, "key=clear"], shell=False,
                                          capture_output=True).stdout.decode('gbk')

            # 将 profile 中的 wifi 密码取出
            key = (re.findall("关键内容            : (.*)\r", profile_info))
            column += 1
            if len(key) > 0:
                item = QStandardItem('%s' % str(key[0]))
                self.model.setItem(row, column, item)
                self.worksheet.write(row, column, str(key[0]))
            row += 1

    def save_wifi_info_butt(self):
        self.workbook.save('wifi_key.xls')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
