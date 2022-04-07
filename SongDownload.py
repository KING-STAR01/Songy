import requests
from bs4 import BeautifulSoup
import os


class SongDownload:
    # constructor
    def __init__(self, movie_link):

        self.movie = movie_link
        self.songsNormal = []
        self.songsHd = []
        self.songsHdNames = []
        self.songsNormalNames = []
        self.parseList()

    def parseList(self):
        page = requests.get(self.movie)
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            # print(link['href'][-3:] == 'mp3')
            temp = link['href']
            if temp.endswith('mp3'):

                if ('HQ' in temp):
                    self.songsHd.append(temp)
                    self.songsHdNames.append(link.parent.text[:link.parent.text.find("128 Kbps")])
                else:
                    self.songsNormal.append(temp)
                    self.songsNormalNames.append(link.parent.text[:link.parent.text.find("128 Kbps")])

    def download(self, quality, id, dir):
        name = None
        print(dir)
        url = self.songsNormal[id]
        print(self.songsNormal[id], id)
        # if(quality == 1):
        #     try:
        #         url = self.songsHd[id]
        #     except IndexError:
        #         url = self.songsNormal[id]
        #
        # else:
        #     try:
        #         url = self.songsNormal[id]
        #     except IndexError:
        #         url = self.songsHd[id]
        ind = url[::-1].find('/')
        name = url[len(url) - ind:].replace('%20', "_")
        filepath = os.path.join(dir, name)
        with open(filepath, 'wb') as file:
            try:
                data = requests.get(url)
                file.write(data.content)
            except requests.Timeout:
                return False

        return True


if __name__ == '__main__':
    a = SongDownload("https://naasongs.com.co/radhe-shyam-2022-telugu-songs-prabhas-1a.html")
    # print(a.songsHd)
    # print(a.songsNormal)
    # print(a.download(1,1,'/home/king_star/Desktop/'))
