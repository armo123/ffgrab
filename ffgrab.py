#!/usr/bin/python2
# -*- encoding: utf-8 -*-
######################
# Author: armo       #
# Date:   15-10-17   #
# Module: ffgrab     #
######################

# Description: this is a simple gui wraper
# for ffmpeg to record desktop

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from subprocess import Popen


class mainW(QMainWindow):

    def __init__(self):
        super(mainW, self).__init__()
        self.centralWidget = QWidget()
        self.labelRes = QLabel('Resolution')
        self.comboRes = QComboBox()
        self.buttonRec = QPushButton("Record")
        self.buttonStop = QPushButton("Stop")
        self.sh = ['sh', 'resgrab.sh']
        Popen(self.sh)
        with open("res.txt", "r") as res:
            for line in res:
                self.comboRes.addItem(line)

        self.resLayout = QHBoxLayout()
        self.resLayout.addWidget(self.labelRes)
        self.resLayout.addWidget(self.comboRes)
        self.labelRate = QLabel("Frame Rate: ")
        self.spinRate = QSpinBox()
        self.spinRate.setValue(25)
        self.layoutRate = QHBoxLayout()
        self.layoutRate.addWidget(self.labelRate)
        self.layoutRate.addWidget(self.spinRate)
        self.checkAudio = QCheckBox()
        self.labelAudio = QLabel("Grab Audio")
        self.layoutAudio = QHBoxLayout()
        self.layoutAudio.addWidget(self.labelAudio)
        self.layoutAudio.addWidget(self.checkAudio)
        self.centralLayout = QVBoxLayout()
        self.centralLayout.addWidget(self.buttonRec)
        self.centralLayout.addWidget(self.buttonStop)
        self.centralLayout.addLayout(self.resLayout)
        self.centralLayout.addLayout(self.layoutRate)
        self.centralLayout.addWidget(self.audio)
        self.centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self.centralWidget)

        def record():
            res = str(self.comboRes.currentText()).rstrip('\n')
            rate = str(self.spinRate.value())
            grabAudio = [
                'ffmpeg', '-f',
                'x11grab', '-r',
                rate, '-s',
                res, '-i',
                ':0.0', '-f',
                'pulse',
                '-i', 'default',
                '/home/armo/capture/output.mkv']
            if self.audio.isChecked():
                Popen(grabAudio)
            else:
                # Remove unessary items to grab the video only
                grabAudio.pop(12)
                grabAudio.pop(11)
                grabAudio.pop(10)
                grabAudio.pop(9)
                defaultRecord = grabAudio
                Popen(defaultRecord)

        def stopRecord():
            kill = ['pkill', '-15', 'ffmpeg']
            Popen(kill)

        self.buttonStop.clicked.connect(stopRecord)
        self.buttonRec.clicked.connect(record)


def main():
    app = QApplication(sys.argv)
    window = mainW()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
