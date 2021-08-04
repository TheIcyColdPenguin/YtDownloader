from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import re
import pytube as pt
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os
import music_tag

import QThreading

SELECT_QUALITY_PROMPT_STRING = "Click to select quality"


class UiMainWindow:
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

    def set_window(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(939, 534)

    def set_widget(self, main_window):
        self.widget = QtWidgets.QWidget(main_window)
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
        self.url_line_edit = QtWidgets.QLineEdit(self.widget)
        self.url_line_edit.setGeometry(QtCore.QRect(190, 130, 500, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.url_line_edit.setFont(font)
        self.url_line_edit.setStyleSheet(self.make_style("QLineEdit"))
        self.url_line_edit.setObjectName("URLLineEdit")

    def set_search_button(self, search_image_path):
        self.search_push_button = QtWidgets.QPushButton(self.widget)
        self.search_push_button.setGeometry(QtCore.QRect(700, 130, 60, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.search_push_button.setFont(font)
        self.search_push_button.setStyleSheet(self.make_style("QPushButton"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(search_image_path),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.search_push_button.setIcon(icon)
        self.search_push_button.setIconSize(QtCore.QSize(25, 25))
        self.search_push_button.setObjectName("SearchPushButton")
        self.search_push_button.clicked.connect(self.check_url)

    def set_folder_edit(self):
        self.folder_line_edit = QtWidgets.QLineEdit(self.widget)
        self.folder_line_edit.setGeometry(QtCore.QRect(190, 210, 500, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.folder_line_edit.setFont(font)
        self.folder_line_edit.setStyleSheet(self.make_style("QLineEdit"))
        self.folder_line_edit.setObjectName("FolderLineEdit")
        self.folder_line_edit.setHidden(True)

    def set_folder_button(self, folder_icon_path):
        self.select_folder_push_button = QtWidgets.QPushButton(self.widget)
        self.select_folder_push_button.setGeometry(
            QtCore.QRect(700, 210, 60, 60))
        self.select_folder_push_button.setStyleSheet(
            self.make_style("QPushButton"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(folder_icon_path),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.select_folder_push_button.setIcon(icon)
        self.select_folder_push_button.setIconSize(QtCore.QSize(35, 35))
        self.select_folder_push_button.setObjectName("FolderSelectBUtton")
        self.select_folder_push_button.setHidden(True)
        self.select_folder_push_button.clicked.connect(self.select_folder)

    def set_queue_button(self):
        self.queue_push_button = QtWidgets.QPushButton(self.widget)
        self.queue_push_button.setGeometry(QtCore.QRect(779, 40, 111, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.queue_push_button.setFont(font)
        self.queue_push_button.setStyleSheet(self.make_style("QPushButton"))
        self.queue_push_button.setObjectName("QueueButton")

    def set_combo_box(self):
        self.quality_combo_box = QtWidgets.QComboBox(self.widget)
        self.quality_combo_box.setGeometry(QtCore.QRect(190, 290, 570, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.quality_combo_box.setFont(font)
        self.quality_combo_box.setStyleSheet(self.make_style("QComboBox", '''QComboBox::drop-down {
  image: #00000000;
}'''))
        self.quality_combo_box.setObjectName("QualityButton")
        self.quality_combo_box.addItem(SELECT_QUALITY_PROMPT_STRING)
        self.quality_combo_box.setHidden(True)

    def set_start_button(self):
        self.start_push_button = QtWidgets.QPushButton(self.widget)
        self.start_push_button.setGeometry(QtCore.QRect(380, 390, 230, 90))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.start_push_button.setFont(font)
        self.start_push_button.setStyleSheet(self.make_style("QPushButton"))
        self.start_push_button.setObjectName("StartButton")
        self.start_push_button.setHidden(True)
        self.start_push_button.clicked.connect(self.click_btn)

    @staticmethod
    def is_v(url):
        return re.match(r"^(https://)?(www\.)?youtube\.com/watch\?([^&=]+?=[^&=]+?&)*v=[\w\-]+(&[^&=]+?=[^&=]+?)*$", url) \
            or re.match(r"^(https://)?youtu\.be/[\w\-]+$", url)

    @staticmethod
    def is_p(url):
        return re.match(r"^(https://)?(www\.)?youtube\.com/playlist\?([^&=]+?=[^&=]+?&)*list=[\w\-]+(&[^&=]+?=[^&=]+?)*$", url)

    def check_url(self):
        text = self.url_line_edit.text()
        is_v = self.is_v(text)
        is_p = self.is_p(text)

        if not is_v and not is_p:
            self.url_line_edit.setText("Please enter a valid url")
            return

        self.folder_line_edit.setHidden(False)
        self.select_folder_push_button.setHidden(False)
        self.quality_combo_box.setHidden(False)
        self.start_push_button.setHidden(False)

        video = pt.YouTube(text) if is_v else pt.YouTube(
            pt.Playlist(text).video_urls[0])
        self.quality_combo_box.clear()
        self.quality_combo_box.addItem(SELECT_QUALITY_PROMPT_STRING)
        options = []
        for stream in video.streams:
            vora, ext = stream.mime_type.split("/")
            if vora == "video":
                options.append(
                    f"{ext.upper()} file at {stream.resolution} resolution")
            else:
                options.append(
                    f"MP3 file at {stream.abr} bitrate") if ext.upper() == "WEBM" else None

        self.quality_combo_box.addItems(sorted(list(set(options))))

    def select_folder(self):
        self.folder_line_edit.setText(str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self.select_folder_push_button, "Select Directory"
            )))

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
        f['artist'] = (
            metadata[0]['Artist']
            if len(metadata) > 0 and metadata[0].get('Artist') is not None
            else vid.author
        )
        f['comment'] = vid.description
        f['compilation'] = False
        f['composer'] = f['artist']
        f['tracktitle'] = (
            metadata[0]['Song']
            if len(metadata) > 0 and metadata[0].get('Song') is not None
            else vid.title
        )
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
        url = self.url_line_edit.text()
        target_dir = self.folder_line_edit.text()
        quality = str(self.quality_combo_box.currentText())
        is_v, is_p = self.is_v(url), self.is_p(url)

        if is_p:
            playlist = pt.Playlist(url)
            iter_things = playlist.video_urls
        elif is_v:
            iter_things = [url]
        else:
            self.url_line_edit.setText("Please enter a valid url")
            return

        if not target_dir:
            self.folder_line_edit.setText("Please choose a directory")
            return

        if quality == SELECT_QUALITY_PROMPT_STRING:
            return

        self.title_label.setText("")
        self.title_label.setText("Downloading..")
        self.message_label.setHidden(False)
        self.quality_combo_box.setHidden(True)
        self.folder_line_edit.setHidden(True)
        self.queue_push_button.setHidden(True)
        self.select_folder_push_button.setHidden(True)
        self.url_line_edit.setHidden(True)
        self.search_push_button.setHidden(True)
        self.start_push_button.setHidden(True)
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
        self.queue_push_button.setHidden(False)
        self.url_line_edit.setHidden(False)
        self.search_push_button.setHidden(False)

    def setup_ui(self, main_window):
        main_window.setFixedSize(939, 534)
        self.set_window(main_window)
        self.set_widget(main_window)
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
        main_window.setCentralWidget(self.widget)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_label.setText(_translate(
            "MainWindow", "Youtube Downloader"))
        self.url_line_edit.setPlaceholderText(_translate(
            "MainWindow", "Type URL of the video/playlist"))
        self.folder_line_edit.setPlaceholderText(_translate(
            "MainWindow", "Enter destination folder path"))
        self.queue_push_button.setText(_translate("MainWindow", "QUEUE"))
        self.start_push_button.setText(_translate("MainWindow", "START"))


app = QtWidgets.QApplication(sys.argv)
main_window = QtWidgets.QMainWindow()
ui = UiMainWindow()
ui.setup_ui(main_window)
main_window.show()
sys.exit(app.exec_())
