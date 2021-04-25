from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import re
import pytube as pt
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os
import music_tag

import QThreading


class Ui_MainWindow:
    @staticmethod
    def make_style(obj_name, additional_props=""):
        styles = f"""{obj_name} {{
    border: 2px solid rgb(15, 163, 255);
    padding-left: 20px;
    padding-right: 20px;
    border-radius: 20px;
    color: #FFF;
    background-color: rgb(34, 36, 44);
}}

{obj_name}:hover {{
    border: 2px solid rgb(37, 213, 255);
}}

{obj_name}:focus {{
    border: 2px solid rgb(255, 65, 51);
    background-color: rgb(43, 45, 56);
}}

{additional_props}
"""
        return styles

    def set_window(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(939, 534)

    def set_widget(self, MainWindow):
        self.widget = QtWidgets.QWidget(MainWindow)
        self.widget.setObjectName("MainWidget")

    def set_label(self, background_fp):
        self.background_label = QtWidgets.QLabel(self.widget)
        self.background_label.setGeometry(QtCore.QRect(0, 0, 939, 534))
        self.background_label.setText("")
        self.background_label.setPixmap(QtGui.QPixmap(background_fp))
        self.background_label.setScaledContents(True)
        self.background_label.setObjectName("Background")

    def set_title_label(self):
        self.title_label = QtWidgets.QLabel(self.widget)
        self.title_label.setGeometry(QtCore.QRect(245, 20, 460, 80))
        font = QtGui.QFont()
        font.setFamily("Bahnschift SemiBold")
        font.setBold(True)
        font.setPointSize(25)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet('color: "white"')
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("TitleLabel")

    def set_video_progress_bar(self):
        self.video_progress_bar = QtWidgets.QProgressBar(self.widget)
        self.video_progress_bar.setGeometry(QtCore.QRect(190, 130, 570, 60))
        self.video_progress_bar.setStyleSheet(self.make_style("QProgressBar", '''QProgressBar {
    border-radius: 0px;
    text-align: center;
    color: white;
    padding-left: 0px;
    padding-right: 0px;
}
        
QProgressBar::chunk {
    background-color: red;
}'''))
        self.video_progress_bar.setObjectName("VideoProgressBar")
        self.video_progress_bar.setHidden(True)

    def set_audio_progress_bar(self):
        self.audio_progress_bar = QtWidgets.QProgressBar(self.widget)
        self.audio_progress_bar.setGeometry(QtCore.QRect(190, 210, 570, 60))
        self.audio_progress_bar.setStyleSheet(self.make_style("QProgressBar", '''QProgressBar {
    border-radius: 0px;
    text-align: center;
    color: white;
    padding-left: 0px;
    padding-right: 0px;
}
        
QProgressBar::chunk {
    background-color: red;
}'''))
        self.audio_progress_bar.setObjectName("AudioProgressBar")
        self.audio_progress_bar.setHidden(True)

    def set_message_label(self):
        self.message_label = QtWidgets.QLabel(self.widget)
        self.message_label.setGeometry(QtCore.QRect(190, 290, 570, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.message_label.setFont(font)
        self.message_label.setStyleSheet('''QLabel {
    text-align: center;
    color: white;
}''')
        self.message_label.setObjectName("MessageLabel")
        self.message_label.setHidden(True)

    def set_url_edit(self):
        self.url_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.url_lineEdit.setGeometry(QtCore.QRect(190, 130, 500, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.url_lineEdit.setFont(font)
        self.url_lineEdit.setStyleSheet(self.make_style("QLineEdit"))
        self.url_lineEdit.setObjectName("URLLineEdit")

    def set_search_button(self, search_image_path):
        self.search_pushButton = QtWidgets.QPushButton(self.widget)
        self.search_pushButton.setGeometry(QtCore.QRect(700, 130, 60, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.search_pushButton.setFont(font)
        self.search_pushButton.setStyleSheet(self.make_style("QPushButton"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(search_image_path),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.search_pushButton.setIcon(icon)
        self.search_pushButton.setIconSize(QtCore.QSize(25, 25))
        self.search_pushButton.setObjectName("SearchPushButton")
        self.search_pushButton.clicked.connect(self.check_url)

    def set_folder_edit(self):
        self.folder_lineEdit = QtWidgets.QLineEdit(self.widget)
        self.folder_lineEdit.setGeometry(QtCore.QRect(190, 210, 500, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.folder_lineEdit.setFont(font)
        self.folder_lineEdit.setStyleSheet(self.make_style("QLineEdit"))
        self.folder_lineEdit.setObjectName("FolderLineEdit")
        self.folder_lineEdit.setHidden(True)

    def set_folder_button(self, folder_icon_path):
        self.select_folder_pushButton = QtWidgets.QPushButton(self.widget)
        self.select_folder_pushButton.setGeometry(
            QtCore.QRect(700, 210, 60, 60))
        self.select_folder_pushButton.setStyleSheet(
            self.make_style("QPushButton"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(folder_icon_path),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.select_folder_pushButton.setIcon(icon)
        self.select_folder_pushButton.setIconSize(QtCore.QSize(35, 35))
        self.select_folder_pushButton.setObjectName("FolderSelectBUtton")
        self.select_folder_pushButton.setHidden(True)
        self.select_folder_pushButton.clicked.connect(self.select_folder)

    def set_queue_button(self):
        self.queue_pushButton = QtWidgets.QPushButton(self.widget)
        self.queue_pushButton.setGeometry(QtCore.QRect(779, 40, 111, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.queue_pushButton.setFont(font)
        self.queue_pushButton.setStyleSheet(self.make_style("QPushButton"))
        self.queue_pushButton.setObjectName("QueueButton")

    def set_combo_box(self):
        self.quality_comboBox = QtWidgets.QComboBox(self.widget)
        self.quality_comboBox.setGeometry(QtCore.QRect(190, 290, 570, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.quality_comboBox.setFont(font)
        self.quality_comboBox.setStyleSheet(self.make_style("QComboBox", '''QComboBox::drop-down {
  image: #00000000;
}'''))
        self.quality_comboBox.setObjectName("QualityButton")
        self.quality_comboBox.addItem("Click to select quality")
        self.quality_comboBox.setHidden(True)

    def set_start_button(self):
        self.start_pushButton = QtWidgets.QPushButton(self.widget)
        self.start_pushButton.setGeometry(QtCore.QRect(380, 390, 230, 90))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.start_pushButton.setFont(font)
        self.start_pushButton.setStyleSheet(self.make_style("QPushButton"))
        self.start_pushButton.setObjectName("StartButton")
        self.start_pushButton.setHidden(True)
        self.start_pushButton.clicked.connect(self.click_btn)

    @staticmethod
    def is_v(url):
        return re.match(r"^(https://)?www\.youtube\.com/watch\?v=[\w\-]+$", url) or re.match(r"^(https://)?youtu\.be/[\w\-]+$", url)

    @staticmethod
    def is_p(url):
        return re.match(r"^https://www\.youtube\.com/playlist\?list=[\w_\-]+$", url)

    def check_url(self):
        text = self.url_lineEdit.text()
        is_v = self.is_v(text)
        is_p = self.is_p(text)

        if not is_v and not is_p:
            self.url_lineEdit.setText("Please enter a valid url")
            return

        self.folder_lineEdit.setHidden(False)
        self.select_folder_pushButton.setHidden(False)
        self.quality_comboBox.setHidden(False)
        self.start_pushButton.setHidden(False)

        video = pt.YouTube(text) if is_v else pt.YouTube(
            pt.Playlist(text).video_urls[0])
        self.quality_comboBox.clear()
        self.quality_comboBox.addItem("Click to select quality")
        options = []
        for stream in video.streams:
            vora, ext = stream.mime_type.split("/")
            if vora == "video":
                options.append(
                    f"{ext.upper()} file at {stream.resolution} resolution")
            else:
                options.append(
                    f"MP3 file at {stream.abr} bitrate") if ext.upper() == "WEBM" else None

        self.quality_comboBox.addItems(sorted(list(set(options))))

    def select_folder(self):
        self.folder_lineEdit.setText(str(
            QtWidgets.QFileDialog.getExistingDirectory(self.select_folder_pushButton, "Select Directory")))

    @staticmethod
    def download_video(vid, ext, qual, target_dir):
        for stream in vid.streams:
            if stream.mime_type == f"video/{ext.lower()}" and stream.resolution == qual:
                print(stream.is_progressive)
                return stream.download(target_dir), stream.is_progressive

        return vid.streams.get_highest_resolution().download()

    def download_audio(self, vid, qual, target_dir, ind, n):
        if qual == "Highest":
            path = vid.streams.get_audio_only(
                subtype="webm").download(target_dir)

        for stream in vid.streams:
            if stream.mime_type == "audio/webm" and stream.abr == qual:
                path = stream.download(target_dir)
                break
        else:
            path = vid.streams.get_audio_only(
                subtype="webm").download(target_dir)

        new_path = path[:-5] + ".mp3"
        file = AudioFileClip(path)
        self.message_label.setText(
            f"Converting audio stream to mp3.. ({ind + 1} of {n})")
        file.write_audiofile(new_path)
        file.close()
        os.remove(path)

        metadata = vid.metadata.metadata
        f = music_tag.load_file(new_path)
        f['artist'] = metadata[0]['Artist'] if len(metadata) > 0 else vid.author
        f['comment'] = vid.description
        f['compilation'] = False
        f['composer'] = metadata[0]['Artist'] if len(
            metadata) > 0 else vid.author
        f['tracktitle'] = metadata[0]['Song'] if len(
            metadata) > 0 else vid.title
        f['year'] = vid.publish_date.year
        f.save()

        return new_path

    def update_progress(self, stream, _, bytes_remaining):
        progress = round(
            ((stream.filesize - bytes_remaining) / stream.filesize) * 100, 2)

        if stream.includes_audio_track:
            self.audio_progress_bar.setValue(progress)
        else:
            self.video_progress_bar.setValue(progress)

    def click_btn(self):
        self.threadpool = QtCore.QThreadPool()
        worker = QThreading.Worker(self.download)
        self.threadpool.start(worker)

    def download(self):
        url = self.url_lineEdit.text()
        target_dir = self.folder_lineEdit.text()
        quality = str(self.quality_comboBox.currentText())
        is_v, is_p = self.is_v(url), self.is_p(url)

        if is_p:
            playlist = pt.Playlist(url)
            iter_things = playlist.video_urls
        elif is_v:
            iter_things = [url]
        else:
            self.url_lineEdit.setText("Please enter a valid url")
            return

        if not target_dir:
            self.folder_lineEdit.setText("Please choose a directory")
            return

        if quality == "Click to select quality":
            return

        self.title_label.setText("")
        self.title_label.setText("Downloading..")
        self.message_label.setHidden(False)
        self.quality_comboBox.setHidden(True)
        self.folder_lineEdit.setHidden(True)
        self.queue_pushButton.setHidden(True)
        self.select_folder_pushButton.setHidden(True)
        self.url_lineEdit.setHidden(True)
        self.search_pushButton.setHidden(True)
        self.start_pushButton.setHidden(True)
        n = len(iter_things)

        for ind, text in enumerate(iter_things):
            ext, _, _, qual, vora = quality.split(" ")
            vid = pt.YouTube(text, on_progress_callback=self.update_progress)

            if vora == "resolution":
                self.video_progress_bar.setHidden(False)
                self.message_label.setText(
                    f"Downloading video.. ({ind + 1} of {n})")
                video_path, is_progressive = self.download_video(
                    vid, ext, qual, target_dir)

                if not is_progressive:
                    self.audio_progress_bar.setHidden(False)
                    self.message_label.setText(
                        f"Downloading audio.. ({ind + 1} of {n})")
                    audio_path = self.download_audio(
                        vid, "Highest", target_dir, ind, n)
                    self.message_label.setText(
                        f"Merging streams.. ({ind + 1} of {n})")
                    v = VideoFileClip(video_path)
                    a = AudioFileClip(audio_path)
                    v = v.set_audio(a)
                    self.message_label.setText(
                        f"Writing to disk.. ({ind + 1} of {n})")
                    v.write_videofile(f"{video_path[:-4]} - Output.mp4")
                    v.close()
                    a.close()
                    os.remove(audio_path)
                    os.remove(video_path)
                    os.rename(
                        f"{video_path[:-4]} - Output.mp4", f"{video_path[:-4]}.mp4")
                    self.audio_progress_bar.setHidden(True)

                self.video_progress_bar.setHidden(True)

            elif vora == "bitrate":
                self.audio_progress_bar.setHidden(False)
                self.message_label.setText(
                    f"Downloading audio stream.. ({ind + 1} of {n})")
                self.download_audio(vid, qual, target_dir, ind, n)
                self.audio_progress_bar.setHidden(True)

        self.title_label.setText("YouTube Downloader")
        self.message_label.setText("")
        self.message_label.setHidden(True)
        self.queue_pushButton.setHidden(False)
        self.url_lineEdit.setHidden(False)
        self.search_pushButton.setHidden(False)

    def setupUi(self, MainWindow):
        MainWindow.setFixedSize(939, 534)
        self.set_window(MainWindow)
        self.set_widget(MainWindow)
        self.set_label("./assets/bg.jpg")
        self.set_video_progress_bar()
        self.set_audio_progress_bar()
        self.set_message_label()
        self.set_title_label()
        self.set_url_edit()
        self.set_search_button("./assets/search.svg")
        self.set_folder_edit()
        self.set_folder_button("./assets/folder.svg")
        self.set_queue_button()
        self.set_combo_box()
        self.set_start_button()
        MainWindow.setCentralWidget(self.widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_label.setText(_translate(
            "MainWindow", "Youtube Downloader"))
        self.url_lineEdit.setPlaceholderText(_translate(
            "MainWindow", "Type URL of the video/playlist"))
        self.folder_lineEdit.setPlaceholderText(_translate(
            "MainWindow", "Enter destination folder path"))
        self.queue_pushButton.setText(_translate("MainWindow", "QUEUE"))
        self.start_pushButton.setText(_translate("MainWindow", "START"))


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
