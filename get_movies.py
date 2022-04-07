import requests
from bs4 import BeautifulSoup

movielinks = []
movienames = []

def parseLinks(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content,'html.parser')


    a=soup.find_all(class_ = "entry-title")
    for movie in a:
        movielinks.append(movie.find('a')['href'])
        movienames.append(movie.text)



firsturl = "https://naasongs.com.co"
mainurl = "https://naasongs.com.co/page/" #https://naasongs.com.co/page/pageno
#313 pages



parseLinks(firsturl)
for i in range(2,314):
    parseLinks(mainurl+str(i))

with open("movielinks.txt","w") as file:
    for i in movielinks:
        file.write(i+"\n")
        
with open("movienames.txt","w") as file:
    for i in movienames:
        print(i)
        file.write(i+"\n")

    
