#!/usr/bin/python2
# -*- encoding: utf-8 -*-
######################
# Author: armo       #
# Date:   15-10-17   #
# Module: ffgrab     #
######################

# Description: this is a simple gui wrapper
# for ffmpeg to record desktop

from PyQt4.QtGui import QApplication, QWidget, QLabel, QMainWindow, QComboBox
from PyQt4.QtGui import QPushButton, QHBoxLayout, QVBoxLayout,\
    QCheckBox, QIcon, QSpinBox
import sys
from subprocess import Popen


class mainW(QMainWindow):

    def __init__(self):
        super(mainW, self).__init__()
        self.centralWidget = QWidget()
        self.labelRes = QLabel('Resolution')
        self.comboRes = QComboBox()
        self.buttonRec = QPushButton("Record")
        self.buttonRec.setIcon(QIcon("icons/player_record.png"))
        self.buttonStop = QPushButton("Stop")
        self.buttonStop.setIcon(QIcon("icons/player_stop.png"))
        self.recordLayout = QHBoxLayout()
        self.recordLayout.addWidget(self.buttonRec)
        self.recordLayout.addWidget(self.buttonStop)
        # retrieve  available resolutions on the system
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
        self.centralLayout.addLayout(self.recordLayout)
        self.centralLayout.addLayout(self.resLayout)
        self.centralLayout.addLayout(self.layoutRate)
        self.centralLayout.addLayout(self.layoutAudio)
        self.centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self.centralWidget)

        def record():
            res = str(self.comboRes.currentText()).rstrip('\n')
            rate = str(self.spinRate.value())
            grabAudioVideo = [
                'ffmpeg', '-f',
                'x11grab', '-r',
                rate, '-s',
                res, '-i',
                ':0.0', '-f',
                'pulse', '-ac', '2',
                '-i', 'default',
                'capture/output.mkv']
            if self.checkAudio.isChecked():
                Popen(grabAudioVideo)
                print(grabAudioVideo)
            else:
                # Remove unnecessary items to grab the video only
                grabAudioVideo.pop(14)
                grabAudioVideo.pop(13)
                grabAudioVideo.pop(12)
                grabAudioVideo.pop(11)
                grabAudioVideo.pop(10)
                grabAudioVideo.pop(9)
                grabVideo = grabAudioVideo
                Popen(grabVideo)

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
