# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget, QWizard, QWizardPage)

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.resize(542, 428)
        self.wizardPage1 = QWizardPage()
        self.wizardPage1.setObjectName(u"wizardPage1")
        self.lineEdit = QLineEdit(self.wizardPage1)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(140, 90, 301, 41))
        self.lineEdit_2 = QLineEdit(self.wizardPage1)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(140, 160, 301, 41))
        self.label = QLabel(self.wizardPage1)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 100, 81, 16))
        self.label_2 = QLabel(self.wizardPage1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 170, 81, 16))
        self.label_3 = QLabel(self.wizardPage1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(240, 40, 49, 16))
        self.pushButton = QPushButton(self.wizardPage1)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(220, 240, 81, 26))
        Wizard.addPage(self.wizardPage1)
        self.wizardPage2 = QWizardPage()
        self.wizardPage2.setObjectName(u"wizardPage2")
        Wizard.addPage(self.wizardPage2)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"Wizard", None))
        self.label.setText(QCoreApplication.translate("Wizard", u"USERNAME : ", None))
        self.label_2.setText(QCoreApplication.translate("Wizard", u"PASSWORD :", None))
        self.label_3.setText(QCoreApplication.translate("Wizard", u"LOGIN", None))
        self.pushButton.setText(QCoreApplication.translate("Wizard", u"Login", None))
    # retranslateUi

