import os
import sys
import subprocess
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData
from PyQt5.QtMultimediaWidgets import QVideoWidget
import torch
from torch import nn
import torchaudio
import torchaudio.transforms as T

def mp3_to_wav(mp3_path):
    wav_path = mp3_path.replace(".mp3", ".wav")
    if os.path.isfile(wav_path):
        pass
    else:
        cmd = "ffmpeg -i %s -acodec pcm_s16le -ac 1 -ar 16000 %s" % (mp3_path, wav_path)
        subprocess.call(cmd, shell=True)
    return wav_path

def wav_to_wav(wav1_path):
    wav2_path = wav1_path.split('.')[0] + '_1.wav'
    if os.path.isfile(wav2_path):
        pass
    else:
        cmd = "ffmpeg -i %s -acodec pcm_s16le -ac 1 -ar 16000 %s" % (wav1_path, wav2_path)
        subprocess.call(cmd, shell=True)
    return wav2_path

def get_time(wav_path):
    # Get cpu or gpu device for training.
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    # Define model
    class NeuralNetwork(nn.Module):
        def __init__(self):
            super().__init__()
            self.flatten = nn.Flatten()
            self.linear_relu_stack = nn.Sequential(
                nn.Linear(8192, 512),
                nn.ReLU(),
                nn.Linear(512, 512),
                nn.ReLU(),
                nn.Linear(512, 10)
            )

        def forward(self, x):
            x = self.flatten(x)
            logits = self.linear_relu_stack(x)
            return logits

    model = NeuralNetwork().to(device)

    INFO = torchaudio.info(wav_path)
    sample_rate = INFO.sample_rate
    num_frames = INFO.num_frames
    a = int(num_frames/sample_rate) - 1

    def transform(wav_path, s):
        SPEECH_WAVEFORM, SAMPLE_RATE = torchaudio.load(wav_path, s, 16000)

        sample_rate = 6000
        n_fft = 2048
        win_length = None
        hop_length = 512
        n_mels = 256
        n_mfcc = 256

        #Define transform
        mfcc_transform = T.MFCC(
            sample_rate=sample_rate,
            n_mfcc=n_mfcc,
            melkwargs={
                "n_fft": n_fft,
                "n_mels": n_mels,
                "hop_length": hop_length,
                "mel_scale": "htk",
            },
        )
        # Perform transform
        mfcc = mfcc_transform(SPEECH_WAVEFORM)
        return mfcc

    D = []
    for i in range(a):
        s = i * 16000
        D.append(transform(wav_path, s))

    model = NeuralNetwork()
    model.load_state_dict(torch.load("model.pth"))

    classes = [
        0,
        1,
    ]
    model.eval()
    predicted = []
    for mfcc in D:
        with torch.no_grad():
            pred = model(mfcc)
            Predicted = classes[pred[0].argmax(0)]
            predicted.append(Predicted)

    t0 = []
    for i in range(len(predicted)):
        if predicted[i] == 1:
            t0.append(i)

    t1 = []
    for i in t0:
        if (i + 1) not in t0:
            t1.append(i)

    order = [0, 1, 2, 3, 4, 7, 9, 11, 13, 15]
    t = []
    for i in order:
        t.append(t1[i] * 1000)
    
    return t

class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('音频播放器')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(800, 600)
        self.setFont(QFont('微软雅黑', 12))

        # 播放器
        self.player = QMediaPlayer()
        self.player.setVolume(50)
        self.player.stateChanged.connect(self.stateChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.metaDataChanged.connect(self.metaDataChanged)

        # 播放器控件
        self.videoWidget = QVideoWidget()
        self.player.setVideoOutput(self.videoWidget)

        # 按钮
        self.Button0 = QPushButton('1')
        self.Button0.setEnabled(False)
        self.Button0.clicked.connect(self.setPosition0)
        self.Button1 = QPushButton('2')
        self.Button1.setEnabled(False)
        self.Button1.clicked.connect(self.setPosition1)
        self.Button2 = QPushButton('3')
        self.Button2.setEnabled(False)
        self.Button2.clicked.connect(self.setPosition2)
        self.Button3 = QPushButton('4')
        self.Button3.setEnabled(False)
        self.Button3.clicked.connect(self.setPosition3)
        self.Button4 = QPushButton('5')
        self.Button4.setEnabled(False)
        self.Button4.clicked.connect(self.setPosition4)
        self.Button5 = QPushButton('6')
        self.Button5.setEnabled(False)
        self.Button5.clicked.connect(self.setPosition5)
        self.Button6 = QPushButton('7')
        self.Button6.setEnabled(False)
        self.Button6.clicked.connect(self.setPosition6)
        self.Button7 = QPushButton('8')
        self.Button7.setEnabled(False)
        self.Button7.clicked.connect(self.setPosition7)
        self.Button8 = QPushButton('9')
        self.Button8.setEnabled(False)
        self.Button8.clicked.connect(self.setPosition8)
        self.Button9 = QPushButton('10')
        self.Button9.setEnabled(False)
        self.Button9.clicked.connect(self.setPosition9)


        # 播放按钮
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        # 音量滑块
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setToolTip('音量')
        self.volumeSlider.valueChanged.connect(self.changeVolume)

        # 播放进度滑块
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        # 歌曲封面
        self.label3 = QLabel()
        self.label3.setAlignment(Qt.AlignCenter)

        # 歌曲时长
        self.label4 = QLabel()
        self.label4.setText('00:00')
        self.label4.setAlignment(Qt.AlignCenter)

        # 歌曲播放时长
        self.label5 = QLabel()
        self.label5.setText('00:00')
        self.label5.setAlignment(Qt.AlignCenter)

        # 打开文件按钮
        self.openButton = QPushButton('打开文件')
        self.openButton.clicked.connect(self.openFile)

        #按钮布局
        hbox0 = QHBoxLayout()
        hbox0.setSpacing(10)
        hbox0.addWidget(self.Button0)
        hbox0.addWidget(self.Button1)
        hbox0.addWidget(self.Button2)
        hbox0.addWidget(self.Button3)
        hbox0.addWidget(self.Button4)
        hbox0.addWidget(self.Button5)
        hbox0.addWidget(self.Button6)
        hbox0.addWidget(self.Button7)
        hbox0.addWidget(self.Button8)
        hbox0.addWidget(self.Button9)

        # 播放按钮布局
        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        hbox.addWidget(self.playButton)
        hbox.addWidget(self.volumeSlider)
        hbox.addWidget(self.label4)
        hbox.addWidget(self.positionSlider)
        hbox.addWidget(self.label5)

        # 整体布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.videoWidget)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox0)
        vbox.addWidget(self.openButton)
        self.setLayout(vbox)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, '打开文件', '', '音频文件 (*.mp3 *.wav *.flac)')
        if fileName != '':
            if 'mp3' in fileName.split('.'):
                fileName = mp3_to_wav(fileName)
            elif 'wav' in fileName.split('.'):
                fileName = wav_to_wav(fileName)
            global t
            t = get_time(fileName)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.Button0.setEnabled(True)
            self.Button1.setEnabled(True)
            self.Button2.setEnabled(True)
            self.Button3.setEnabled(True)
            self.Button4.setEnabled(True)
            self.Button5.setEnabled(True)
            self.Button6.setEnabled(True)
            self.Button7.setEnabled(True)
            self.Button8.setEnabled(True)
            self.Button9.setEnabled(True)

    def play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def changeVolume(self, volume):
        self.player.setVolume(volume)

    def setPosition(self, position):
        self.player.setPosition(position)

    def setPosition0(self):
        self.player.setPosition(t[0])

    def setPosition1(self):
        self.player.setPosition(t[1])

    def setPosition2(self):
        self.player.setPosition(t[2])

    def setPosition3(self):
        self.player.setPosition(t[3])

    def setPosition4(self):
        self.player.setPosition(t[4])

    def setPosition5(self):
        self.player.setPosition(t[5])

    def setPosition6(self):
        self.player.setPosition(t[6])

    def setPosition7(self):
        self.player.setPosition(t[7])

    def setPosition8(self):
        self.player.setPosition(t[8])

    def setPosition9(self):
        self.player.setPosition(t[9])
    
    def stateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def metaDataChanged(self):
        if self.player.isMetaDataAvailable():
            self.setCoverInfo('%s' % (self.player.metaData(QMediaMetaData.CoverArtUrlLarge)))

    def setCoverInfo(self, info):
        self.label3.setPixmap(QPixmap(info))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = Player()
    player.show()
    sys.exit(app.exec_())