# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1156, 945)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Tabs = QtGui.QTabWidget(self.centralwidget)
        self.Tabs.setObjectName(_fromUtf8("Tabs"))
        self.TimeScanTab = QtGui.QWidget()
        self.TimeScanTab.setObjectName(_fromUtf8("TimeScanTab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.TimeScanTab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.TStart = QtGui.QPushButton(self.TimeScanTab)
        self.TStart.setObjectName(_fromUtf8("TStart"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.TStart)
        self.TStop = QtGui.QPushButton(self.TimeScanTab)
        self.TStop.setObjectName(_fromUtf8("TStop"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.TStop)
        self.label = QtGui.QLabel(self.TimeScanTab)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.TScanStart = QtGui.QLineEdit(self.TimeScanTab)
        self.TScanStart.setObjectName(_fromUtf8("TScanStart"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.TScanStart)
        self.GoTScanStart = QtGui.QPushButton(self.TimeScanTab)
        self.GoTScanStart.setObjectName(_fromUtf8("GoTScanStart"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.GoTScanStart)
        self.label_2 = QtGui.QLabel(self.TimeScanTab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.TScanLength = QtGui.QLineEdit(self.TimeScanTab)
        self.TScanLength.setObjectName(_fromUtf8("TScanLength"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.FieldRole, self.TScanLength)
        self.GoTScanLength = QtGui.QPushButton(self.TimeScanTab)
        self.GoTScanLength.setObjectName(_fromUtf8("GoTScanLength"))
        self.formLayout_4.setWidget(4, QtGui.QFormLayout.FieldRole, self.GoTScanLength)
        self.label_3 = QtGui.QLabel(self.TimeScanTab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_4.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_3)
        self.TStep = QtGui.QLineEdit(self.TimeScanTab)
        self.TStep.setObjectName(_fromUtf8("TStep"))
        self.formLayout_4.setWidget(5, QtGui.QFormLayout.FieldRole, self.TStep)
        self.GoTStep = QtGui.QPushButton(self.TimeScanTab)
        self.GoTStep.setObjectName(_fromUtf8("GoTStep"))
        self.formLayout_4.setWidget(6, QtGui.QFormLayout.FieldRole, self.GoTStep)
        self.TDwell = QtGui.QLineEdit(self.TimeScanTab)
        self.TDwell.setObjectName(_fromUtf8("TDwell"))
        self.formLayout_4.setWidget(7, QtGui.QFormLayout.FieldRole, self.TDwell)
        self.label_4 = QtGui.QLabel(self.TimeScanTab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_4.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_4)
        self.GoTDwell = QtGui.QPushButton(self.TimeScanTab)
        self.GoTDwell.setObjectName(_fromUtf8("GoTDwell"))
        self.formLayout_4.setWidget(8, QtGui.QFormLayout.FieldRole, self.GoTDwell)
        self.TLockinR = QtGui.QRadioButton(self.TimeScanTab)
        self.TLockinR.setObjectName(_fromUtf8("TLockinR"))
        self.formLayout_4.setWidget(10, QtGui.QFormLayout.FieldRole, self.TLockinR)
        self.TLockinX = QtGui.QRadioButton(self.TimeScanTab)
        self.TLockinX.setObjectName(_fromUtf8("TLockinX"))
        self.formLayout_4.setWidget(9, QtGui.QFormLayout.FieldRole, self.TLockinX)
        self.label_22 = QtGui.QLabel(self.TimeScanTab)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.formLayout_4.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_22)
        self.horizontalLayout_2.addLayout(self.formLayout_4)
        self.TPlot = Canvas(self.TimeScanTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TPlot.sizePolicy().hasHeightForWidth())
        self.TPlot.setSizePolicy(sizePolicy)
        self.TPlot.setObjectName(_fromUtf8("TPlot"))
        self.horizontalLayout_2.addWidget(self.TPlot)
        self.Tabs.addTab(self.TimeScanTab, _fromUtf8(""))
        self.XTApTab = QtGui.QWidget()
        self.XTApTab.setObjectName(_fromUtf8("XTApTab"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.XTApTab)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setHorizontalSpacing(6)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.XTStartBut = QtGui.QPushButton(self.XTApTab)
        self.XTStartBut.setObjectName(_fromUtf8("XTStartBut"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.XTStartBut)
        self.XTStopBut = QtGui.QPushButton(self.XTApTab)
        self.XTStopBut.setObjectName(_fromUtf8("XTStopBut"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.XTStopBut)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout_3.setItem(1, QtGui.QFormLayout.SpanningRole, spacerItem)
        self.label_15 = QtGui.QLabel(self.XTApTab)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_15)
        self.ScanAlongY = QtGui.QRadioButton(self.XTApTab)
        self.ScanAlongY.setObjectName(_fromUtf8("ScanAlongY"))
        self.XTScanXorY = QtGui.QButtonGroup(MainWindow)
        self.XTScanXorY.setObjectName(_fromUtf8("XTScanXorY"))
        self.XTScanXorY.addButton(self.ScanAlongY)
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.ScanAlongY)
        self.ScanAlongX = QtGui.QRadioButton(self.XTApTab)
        self.ScanAlongX.setObjectName(_fromUtf8("ScanAlongX"))
        self.XTScanXorY.addButton(self.ScanAlongX)
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.ScanAlongX)
        self.label_14 = QtGui.QLabel(self.XTApTab)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_14)
        self.XTStartSpace = QtGui.QLineEdit(self.XTApTab)
        self.XTStartSpace.setObjectName(_fromUtf8("XTStartSpace"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.XTStartSpace)
        self.GoXTStartSpace = QtGui.QPushButton(self.XTApTab)
        self.GoXTStartSpace.setObjectName(_fromUtf8("GoXTStartSpace"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.FieldRole, self.GoXTStartSpace)
        self.label_16 = QtGui.QLabel(self.XTApTab)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_16)
        self.XTStepSpace = QtGui.QLineEdit(self.XTApTab)
        self.XTStepSpace.setObjectName(_fromUtf8("XTStepSpace"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.FieldRole, self.XTStepSpace)
        self.GoXTStepSpace = QtGui.QPushButton(self.XTApTab)
        self.GoXTStepSpace.setObjectName(_fromUtf8("GoXTStepSpace"))
        self.formLayout_3.setWidget(7, QtGui.QFormLayout.FieldRole, self.GoXTStepSpace)
        self.label_18 = QtGui.QLabel(self.XTApTab)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.formLayout_3.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_18)
        self.XTLengthSpace = QtGui.QLineEdit(self.XTApTab)
        self.XTLengthSpace.setObjectName(_fromUtf8("XTLengthSpace"))
        self.formLayout_3.setWidget(8, QtGui.QFormLayout.FieldRole, self.XTLengthSpace)
        self.GoXTLengthSpace = QtGui.QPushButton(self.XTApTab)
        self.GoXTLengthSpace.setObjectName(_fromUtf8("GoXTLengthSpace"))
        self.formLayout_3.setWidget(9, QtGui.QFormLayout.FieldRole, self.GoXTLengthSpace)
        self.label_19 = QtGui.QLabel(self.XTApTab)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.formLayout_3.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_19)
        self.XTStartTime = QtGui.QLineEdit(self.XTApTab)
        self.XTStartTime.setObjectName(_fromUtf8("XTStartTime"))
        self.formLayout_3.setWidget(10, QtGui.QFormLayout.FieldRole, self.XTStartTime)
        self.GoXTStartTime = QtGui.QPushButton(self.XTApTab)
        self.GoXTStartTime.setObjectName(_fromUtf8("GoXTStartTime"))
        self.formLayout_3.setWidget(11, QtGui.QFormLayout.FieldRole, self.GoXTStartTime)
        self.label_17 = QtGui.QLabel(self.XTApTab)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.formLayout_3.setWidget(12, QtGui.QFormLayout.LabelRole, self.label_17)
        self.XTStepTime = QtGui.QLineEdit(self.XTApTab)
        self.XTStepTime.setObjectName(_fromUtf8("XTStepTime"))
        self.formLayout_3.setWidget(12, QtGui.QFormLayout.FieldRole, self.XTStepTime)
        self.GoXTStepTime = QtGui.QPushButton(self.XTApTab)
        self.GoXTStepTime.setObjectName(_fromUtf8("GoXTStepTime"))
        self.formLayout_3.setWidget(13, QtGui.QFormLayout.FieldRole, self.GoXTStepTime)
        self.label_21 = QtGui.QLabel(self.XTApTab)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.formLayout_3.setWidget(14, QtGui.QFormLayout.LabelRole, self.label_21)
        self.XTLengthTime = QtGui.QLineEdit(self.XTApTab)
        self.XTLengthTime.setObjectName(_fromUtf8("XTLengthTime"))
        self.formLayout_3.setWidget(14, QtGui.QFormLayout.FieldRole, self.XTLengthTime)
        self.GoXTLengthTime = QtGui.QPushButton(self.XTApTab)
        self.GoXTLengthTime.setObjectName(_fromUtf8("GoXTLengthTime"))
        self.formLayout_3.setWidget(15, QtGui.QFormLayout.FieldRole, self.GoXTLengthTime)
        self.XTLockinX = QtGui.QRadioButton(self.XTApTab)
        self.XTLockinX.setObjectName(_fromUtf8("XTLockinX"))
        self.LockinXorR = QtGui.QButtonGroup(MainWindow)
        self.LockinXorR.setObjectName(_fromUtf8("LockinXorR"))
        self.LockinXorR.addButton(self.XTLockinX)
        self.formLayout_3.setWidget(16, QtGui.QFormLayout.FieldRole, self.XTLockinX)
        self.XTLockinR = QtGui.QRadioButton(self.XTApTab)
        self.XTLockinR.setObjectName(_fromUtf8("XTLockinR"))
        self.LockinXorR.addButton(self.XTLockinR)
        self.formLayout_3.setWidget(17, QtGui.QFormLayout.FieldRole, self.XTLockinR)
        self.label_20 = QtGui.QLabel(self.XTApTab)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.formLayout_3.setWidget(16, QtGui.QFormLayout.LabelRole, self.label_20)
        self.horizontalLayout.addLayout(self.formLayout_3)
        self.XTPlot = Canvas(self.XTApTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.XTPlot.sizePolicy().hasHeightForWidth())
        self.XTPlot.setSizePolicy(sizePolicy)
        self.XTPlot.setObjectName(_fromUtf8("XTPlot"))
        self.horizontalLayout.addWidget(self.XTPlot)
        self.Tabs.addTab(self.XTApTab, _fromUtf8(""))
        self.XYApTab = QtGui.QWidget()
        self.XYApTab.setObjectName(_fromUtf8("XYApTab"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.XYApTab)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setHorizontalSpacing(6)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.XYStartBut = QtGui.QPushButton(self.XYApTab)
        self.XYStartBut.setObjectName(_fromUtf8("XYStartBut"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.XYStartBut)
        self.XYStopBut = QtGui.QPushButton(self.XYApTab)
        self.XYStopBut.setObjectName(_fromUtf8("XYStopBut"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.XYStopBut)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout_2.setItem(1, QtGui.QFormLayout.SpanningRole, spacerItem1)
        self.label_6 = QtGui.QLabel(self.XYApTab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.XYStartX = QtGui.QLineEdit(self.XYApTab)
        self.XYStartX.setObjectName(_fromUtf8("XYStartX"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.XYStartX)
        self.GoXYStartX = QtGui.QPushButton(self.XYApTab)
        self.GoXYStartX.setObjectName(_fromUtf8("GoXYStartX"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.GoXYStartX)
        self.label_11 = QtGui.QLabel(self.XYApTab)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_11)
        self.XYStartY = QtGui.QLineEdit(self.XYApTab)
        self.XYStartY.setObjectName(_fromUtf8("XYStartY"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.XYStartY)
        self.GoXYStartY = QtGui.QPushButton(self.XYApTab)
        self.GoXYStartY.setObjectName(_fromUtf8("GoXYStartY"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.GoXYStartY)
        self.label_7 = QtGui.QLabel(self.XYApTab)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_7)
        self.XYStepX = QtGui.QLineEdit(self.XYApTab)
        self.XYStepX.setObjectName(_fromUtf8("XYStepX"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.XYStepX)
        self.GoXYStepX = QtGui.QPushButton(self.XYApTab)
        self.GoXYStepX.setObjectName(_fromUtf8("GoXYStepX"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.FieldRole, self.GoXYStepX)
        self.label_8 = QtGui.QLabel(self.XYApTab)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_2.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_8)
        self.XYStepY = QtGui.QLineEdit(self.XYApTab)
        self.XYStepY.setObjectName(_fromUtf8("XYStepY"))
        self.formLayout_2.setWidget(8, QtGui.QFormLayout.FieldRole, self.XYStepY)
        self.GoXYStepY = QtGui.QPushButton(self.XYApTab)
        self.GoXYStepY.setObjectName(_fromUtf8("GoXYStepY"))
        self.formLayout_2.setWidget(9, QtGui.QFormLayout.FieldRole, self.GoXYStepY)
        self.label_9 = QtGui.QLabel(self.XYApTab)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_2.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_9)
        self.XYLengthX = QtGui.QLineEdit(self.XYApTab)
        self.XYLengthX.setObjectName(_fromUtf8("XYLengthX"))
        self.formLayout_2.setWidget(10, QtGui.QFormLayout.FieldRole, self.XYLengthX)
        self.GoXYLengthX = QtGui.QPushButton(self.XYApTab)
        self.GoXYLengthX.setObjectName(_fromUtf8("GoXYLengthX"))
        self.formLayout_2.setWidget(11, QtGui.QFormLayout.FieldRole, self.GoXYLengthX)
        self.label_10 = QtGui.QLabel(self.XYApTab)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_2.setWidget(12, QtGui.QFormLayout.LabelRole, self.label_10)
        self.XYLengthY = QtGui.QLineEdit(self.XYApTab)
        self.XYLengthY.setObjectName(_fromUtf8("XYLengthY"))
        self.formLayout_2.setWidget(12, QtGui.QFormLayout.FieldRole, self.XYLengthY)
        self.GoXYLengthY = QtGui.QPushButton(self.XYApTab)
        self.GoXYLengthY.setObjectName(_fromUtf8("GoXYLengthY"))
        self.formLayout_2.setWidget(13, QtGui.QFormLayout.FieldRole, self.GoXYLengthY)
        self.label_12 = QtGui.QLabel(self.XYApTab)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_2.setWidget(14, QtGui.QFormLayout.LabelRole, self.label_12)
        self.XYLockinX = QtGui.QRadioButton(self.XYApTab)
        self.XYLockinX.setObjectName(_fromUtf8("XYLockinX"))
        self.formLayout_2.setWidget(14, QtGui.QFormLayout.FieldRole, self.XYLockinX)
        self.XYLockinR = QtGui.QRadioButton(self.XYApTab)
        self.XYLockinR.setObjectName(_fromUtf8("XYLockinR"))
        self.formLayout_2.setWidget(15, QtGui.QFormLayout.FieldRole, self.XYLockinR)
        self.horizontalLayout_3.addLayout(self.formLayout_2)
        self.XYPlot = Canvas(self.XYApTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.XYPlot.sizePolicy().hasHeightForWidth())
        self.XYPlot.setSizePolicy(sizePolicy)
        self.XYPlot.setObjectName(_fromUtf8("XYPlot"))
        self.horizontalLayout_3.addWidget(self.XYPlot)
        self.Tabs.addTab(self.XYApTab, _fromUtf8(""))
        self.gridLayout.addWidget(self.Tabs, 0, 0, 1, 1)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_6.addWidget(self.label_5, 0, 1, 1, 1)
        self.DelayPos = QtGui.QLineEdit(self.centralwidget)
        self.DelayPos.setObjectName(_fromUtf8("DelayPos"))
        self.gridLayout_6.addWidget(self.DelayPos, 0, 3, 1, 1)
        self.ZPos = QtGui.QLineEdit(self.centralwidget)
        self.ZPos.setObjectName(_fromUtf8("ZPos"))
        self.gridLayout_6.addWidget(self.ZPos, 0, 6, 1, 1)
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_6.addWidget(self.label_13, 0, 5, 1, 1)
        self.GoZPos = QtGui.QPushButton(self.centralwidget)
        self.GoZPos.setObjectName(_fromUtf8("GoZPos"))
        self.gridLayout_6.addWidget(self.GoZPos, 0, 7, 1, 1)
        self.GoDelayPos = QtGui.QPushButton(self.centralwidget)
        self.GoDelayPos.setObjectName(_fromUtf8("GoDelayPos"))
        self.gridLayout_6.addWidget(self.GoDelayPos, 0, 4, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_6, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1156, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.Tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Lab Control Software", None))
        self.TStart.setText(_translate("MainWindow", "Start", None))
        self.TStop.setText(_translate("MainWindow", "Stop", None))
        self.label.setText(_translate("MainWindow", "Scan start (stage)", None))
        self.GoTScanStart.setText(_translate("MainWindow", "Go", None))
        self.label_2.setText(_translate("MainWindow", "Scan length (stage)", None))
        self.GoTScanLength.setText(_translate("MainWindow", "Set", None))
        self.label_3.setText(_translate("MainWindow", "Step (stage)", None))
        self.GoTStep.setText(_translate("MainWindow", "Set", None))
        self.label_4.setText(_translate("MainWindow", "Dwell (s)", None))
        self.GoTDwell.setText(_translate("MainWindow", "Set", None))
        self.TLockinR.setText(_translate("MainWindow", "Magnitude", None))
        self.TLockinX.setText(_translate("MainWindow", "X", None))
        self.label_22.setText(_translate("MainWindow", "Lock-in output", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.TimeScanTab), _translate("MainWindow", "Time", None))
        self.XTStartBut.setText(_translate("MainWindow", "GO!", None))
        self.XTStopBut.setText(_translate("MainWindow", "STOP!", None))
        self.label_15.setText(_translate("MainWindow", "Scan along", None))
        self.ScanAlongY.setText(_translate("MainWindow", "Y", None))
        self.ScanAlongX.setText(_translate("MainWindow", "X", None))
        self.label_14.setText(_translate("MainWindow", "Start (space) (um)", None))
        self.GoXTStartSpace.setText(_translate("MainWindow", "Go", None))
        self.label_16.setText(_translate("MainWindow", "Step (space) (um):", None))
        self.GoXTStepSpace.setText(_translate("MainWindow", "Set", None))
        self.label_18.setText(_translate("MainWindow", "Length (space) (um):", None))
        self.GoXTLengthSpace.setText(_translate("MainWindow", "Set", None))
        self.label_19.setText(_translate("MainWindow", "Start (time)", None))
        self.GoXTStartTime.setText(_translate("MainWindow", "Go", None))
        self.label_17.setText(_translate("MainWindow", "Step (time)", None))
        self.GoXTStepTime.setText(_translate("MainWindow", "Set", None))
        self.label_21.setText(_translate("MainWindow", "Length (time)", None))
        self.GoXTLengthTime.setText(_translate("MainWindow", "Set", None))
        self.XTLockinX.setText(_translate("MainWindow", "X", None))
        self.XTLockinR.setText(_translate("MainWindow", "Magnitude", None))
        self.label_20.setText(_translate("MainWindow", "Lock-in output", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.XTApTab), _translate("MainWindow", "XT (aperture)", None))
        self.XYStartBut.setText(_translate("MainWindow", "GO!", None))
        self.XYStopBut.setText(_translate("MainWindow", "STOP!", None))
        self.label_6.setText(_translate("MainWindow", "Scan start (X) (um):", None))
        self.GoXYStartX.setText(_translate("MainWindow", "Go", None))
        self.label_11.setText(_translate("MainWindow", "Scan start (Y) (um):", None))
        self.GoXYStartY.setText(_translate("MainWindow", "Go", None))
        self.label_7.setText(_translate("MainWindow", "Step (X) (um):", None))
        self.GoXYStepX.setText(_translate("MainWindow", "Set", None))
        self.label_8.setText(_translate("MainWindow", "Step (Y) (um):", None))
        self.GoXYStepY.setText(_translate("MainWindow", "Set", None))
        self.label_9.setText(_translate("MainWindow", "Length (X) (um):", None))
        self.GoXYLengthX.setText(_translate("MainWindow", "Set", None))
        self.label_10.setText(_translate("MainWindow", "Length (Y) (um):", None))
        self.GoXYLengthY.setText(_translate("MainWindow", "Set", None))
        self.label_12.setText(_translate("MainWindow", "Lock-in output", None))
        self.XYLockinX.setText(_translate("MainWindow", "X", None))
        self.XYLockinR.setText(_translate("MainWindow", "Magnitude", None))
        self.Tabs.setTabText(self.Tabs.indexOf(self.XYApTab), _translate("MainWindow", "XY (aperture)", None))
        self.label_5.setText(_translate("MainWindow", "Move delay stage to:", None))
        self.label_13.setText(_translate("MainWindow", "Move Z (aperture) to", None))
        self.GoZPos.setText(_translate("MainWindow", "Go", None))
        self.GoDelayPos.setText(_translate("MainWindow", "Go", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit..", None))

from canvas import Canvas

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

