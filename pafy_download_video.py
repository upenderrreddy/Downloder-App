import pafy
from humanize import naturalsize, naturaltime


def download_video():
    video_url = "https://www.youtube.com/watch?v=IHiosG1o-eQ"
    save_location = "D:/UR/Projects/Dowloader_using_PYQT5/"

    if video_url == '' or save_location == '':
        QMessageBox.warning(self, "Data Error", "URL or Save location is invalid")
    else:
        video = pafy.new(video_url)
        video.getbestvideo().download(filepath=save_location, callback=video_Progress)
        # video.download()


def video_Progress(total, received, ratio, rate, time):
    # print(naturalsize(total), naturalsize(received), ratio, rate, round(time / 60, 2))
    read_data = received
    # print(read_data)
    if total > 0:
        download_percentage = read_data * 100 / total
        print(int(download_percentage) , end=' ')
        remaining_time = round(time, 2)

        print(str('{} minutes remaining'.format(remaining_time)))
        # QApplication.processEvents()


# url = "https://www.youtube.com/watch?v=eACohWVwTOc"
# video = pafy.new(url)
#
# bestaudio = video.getbestaudio()
# bestaudio.download()
if __name__ == '__main__':
    download_video()
