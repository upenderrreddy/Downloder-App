import sys
from urllib import request

import humanize
import pafy
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.uic import loadUiType

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_ui()
        self.handle_buttons()

    def init_ui(self):
        # contains all ui changes in loading
        pass

    def handle_buttons(self):
        # handle all buttons in the App
        # whenever download button is clicked download() method will be called
        self.pushButton.clicked.connect(self.download)

        # whenever browse button is clicked handle_browse() method will be called
        self.pushButton_19.clicked.connect(self.handle_browse)

        # whenever search button is clicked get_video_data() method will be called
        self.pushButton_6.clicked.connect(self.get_video_data)

        # whenever download button is clicked download_video() method will be called
        self.pushButton_17.clicked.connect(self.download_video)

        # browse for save location of video
        self.pushButton_20.clicked.connect(self.save_browse)

        #
        self.pushButton_4.clicked.connect(self.playlist_download)

        # playlist save browse
        self.pushButton_16.clicked.connect(self.playlist_save_browse)

    def handle_progress(self, block_no, block_size, total_size):
        # calculate the progress
        read_data = block_no * block_size

        if total_size > 0:
            download_percentage = int(read_data / total_size * 100)
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def handle_browse(self):
        # enable browsing files to pick a save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        # print(save_location)  #
        self.lineEdit_2.setText(save_location[0])

    def download(self):
        # downloading file
        # print('Starting download')

        # get download url and save location from gui
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        # validating user input
        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "URL or Save location is invalid")
        else:
            try:
                # urlretrieve() takes downlaod_url, save_location and here we are sending info obtained by this method to handle_progress()
                request.urlretrieve(download_url, save_location, self.handle_progress)
            except Exception:
                QMessageBox.warning(self, "Download Error", "Invalid URL or Save location")
                return
        QMessageBox.information(self, "Download Completed", "Download completed Successfully")

        # After download is completed make url and save location text fields empty
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    ##################################################################
    # Download single YouTube video #

    def save_browse(self):
        # save location in the line edit
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        # print(save_location)  #
        self.lineEdit_4.setText(save_location[0])

    def get_video_data(self):
        video_url = self.lineEdit_3.text()
        print(video_url)
        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Video URL is invalid")
        else:
            # creating pafy object
            video = pafy.new(video_url)
            # print(video.title)
            # print(video.duration)
            # print(video.length)
            # print(video.likes)
            # print(video.dislikes)
            # print(video.viewcount)

            video_streams = video.streams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)

    def download_video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "URL or Save location is invalid")
        else:
            video = pafy.new(video_url)
            video_stream = video.streams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(filepath=save_location, callback=self.video_progress)

    def video_progress(self, total, received, ratio, rate, time):
        read_data = received
        # print(read_data)
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(int(download_percentage))
            remaining_time = round(time / 60, 2)
            self.label_4.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    ################################################
    #  Youtube Playlist Download  #
    def playlist_download(self):
        playlist_url = self.lineEdit_7.text()
        save_location = self.lineEdit_8.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))

        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()

        QApplication.processEvents()

        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.streams
            self.lcdNumber.display(current_video_in_download)
            download = current_video_stream[quality].download(callback=self.playlist_progress)
            QApplication.processEvents()

            current_video_in_download += 1

    def playlist_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_4.setValue(download_percentage)
            remaining_time = round(time / 60, 2)

            self.label_6.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()
    def playlist_save_browse(self):
        # save location in the line edit
        save_location = QFileDialog.getExistingDirectory(self , "Select Download Directory")
        # print(save_location)  #
        self.lineEdit_8.setText(save_location)
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
