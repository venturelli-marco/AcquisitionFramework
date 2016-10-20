#!/usr/bin/python
import sys
import os
from PyQt4 import QtGui, uic # importiamo i moduli necessari
from app import mainwindowCtr


if __name__ == "__main__":
    uic.compileUiDir("gui")
    app = QtGui.QApplication(sys.argv)
    myapp = mainwindowCtr.applicationForm()
    myapp.show()
    sys.exit(app.exec_())


