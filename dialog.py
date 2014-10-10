#!python3

import sys
from os.path import join
from PyQt4 import uic
from PyQt4.QtGui import QWidget, QApplication, QHBoxLayout, QDateEdit, QPushButton

class Exclude(QHBoxLayout):
    def __init__(self, parent = None):
        QHBoxLayout.__init__(self)
        
        # self.start = QDateEdit()
        self.addWidget(QDateEdit())
        self.addWidget(QDateEdit())


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(join('tools', 'dialog.ui'), self)
        
        self.init = dict()
        self.init['excludes'] = []
        
        self.btn.clicked.connect(self.clk)
        self.btnAddExclude.clicked.connect(self.clkAddExcludes)
        self.btnClearExcludes.clicked.connect(self.clearExcludes)
        
        
    def clk(self):
        # self.dateYearStart.text(), self.dateYearFinish.text()
        self.init['year'] = self.dateYearStart.date(), self.dateYearFinish.date()
        
        print(self.init)

    def clkAddExcludes(self):
        self.init['excludes'].append((
                                    tuple(self.dateExcludeStart.text().split('.')),
                                    tuple(self.dateExcludeFinish.text().split('.'))
                                ))
        
        self.Excludes.addItem('{} - {}'.format(self.dateExcludeStart.text(), self.dateExcludeFinish.text()))
        
        print(self.init)
        
    def clearExcludes(self):
        self.init['excludes'] = []
        self.Excludes.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())