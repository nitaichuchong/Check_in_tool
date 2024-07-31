# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolbox.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(539, 439)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 511, 421))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_generate = QtWidgets.QPushButton(self.tab)
        self.pushButton_generate.setGeometry(QtCore.QRect(350, 170, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_generate.setFont(font)
        self.pushButton_generate.setObjectName("pushButton_generate")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(30, 170, 191, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(30, 210, 261, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(30, 290, 471, 21))
        self.label_4.setObjectName("label_4")
        self.dateTimeEdit_start = QtWidgets.QDateTimeEdit(self.tab)
        self.dateTimeEdit_start.setGeometry(QtCore.QRect(30, 240, 194, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dateTimeEdit_start.setFont(font)
        self.dateTimeEdit_start.setObjectName("dateTimeEdit_start")
        self.dateTimeEdit_end = QtWidgets.QDateTimeEdit(self.tab)
        self.dateTimeEdit_end.setGeometry(QtCore.QRect(240, 240, 194, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dateTimeEdit_end.setFont(font)
        self.dateTimeEdit_end.setObjectName("dateTimeEdit_end")
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        self.checkBox.setGeometry(QtCore.QRect(30, 40, 421, 19))
        self.checkBox.setObjectName("checkBox")
        self.comboBox_random = QtWidgets.QComboBox(self.tab)
        self.comboBox_random.setEnabled(False)
        self.comboBox_random.setGeometry(QtCore.QRect(30, 80, 87, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_random.setFont(font)
        self.comboBox_random.setObjectName("comboBox_random")
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.comboBox_random.addItem("")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(30, 110, 441, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.textEdit = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 471, 311))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_update = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_update.setGeometry(QtCore.QRect(200, 350, 93, 28))
        self.pushButton_update.setObjectName("pushButton_update")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.comboBox_delete = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_delete.setGeometry(QtCore.QRect(30, 170, 211, 41))
        self.comboBox_delete.setObjectName("comboBox_delete")
        self.pushButton_delete = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_delete.setGeometry(QtCore.QRect(310, 180, 93, 28))
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.tabWidget.addTab(self.tab_3, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "测试工具箱"))
        self.pushButton_generate.setText(_translate("Form", "生成测试数据"))
        self.label_2.setText(_translate("Form", "请设置测试数据的时间范围"))
        self.label_3.setText(_translate("Form", "左为起始时间，右为终止时间"))
        self.label_4.setText(_translate("Form", "请尽量遵循合理操作，目前误操作处理未完善，请勿乱改导致未知错误"))
        self.checkBox.setText(_translate("Form", "是否需要随机中断？若你想保持测试数据连续则请勿勾选！"))
        self.comboBox_random.setItemText(0, _translate("Form", "1"))
        self.comboBox_random.setItemText(1, _translate("Form", "2"))
        self.comboBox_random.setItemText(2, _translate("Form", "3"))
        self.comboBox_random.setItemText(3, _translate("Form", "4"))
        self.comboBox_random.setItemText(4, _translate("Form", "5"))
        self.comboBox_random.setItemText(5, _translate("Form", "6"))
        self.comboBox_random.setItemText(6, _translate("Form", "7"))
        self.comboBox_random.setItemText(7, _translate("Form", "8"))
        self.comboBox_random.setItemText(8, _translate("Form", "9"))
        self.comboBox_random.setItemText(9, _translate("Form", "10"))
        self.label.setText(_translate("Form", "从 1 到 10 表示随机强度，1 强度最低，10 强度最高"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "生成测试数据"))
        self.pushButton_update.setText(_translate("Form", "更新展示"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "展示解码后的数据"))
        self.pushButton_delete.setText(_translate("Form", "删除选中表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "整表删除"))
