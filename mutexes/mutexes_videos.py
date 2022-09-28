import threading
from pytube import YouTube

mutex = threading.Lock()
def crito(id,url):
    print("Hilo = " + str(id) + " Video = " + url)
    path = "C:/Users/IzAla/Downloads/videos_mutexes"
    try:
        YouTube(url).streams.first().download(path)
        print(f'URL Descargado:  = {url}')
    except Exception as error:
        print("Error: " + error)

class Hilo(threading.Thread):
    def __init__(self,id,url):
        threading.Thread.__init__(self)
        self.id = id
        self.url = url

    def run(self):
        mutex.acquire()
        crito(self.id, self.url)
        # print("Valor " + str(self.id))
        mutex.release()

urls = [
    "https://www.youtube.com/watch?v=GXD0ySQFxRQ",
    "https://www.youtube.com/watch?v=NUz4d-bd2hs",
    "https://www.youtube.com/watch?v=xU8m9X-1fgE",
    "https://www.youtube.com/watch?v=RAPrd4jpxxI",
    "https://www.youtube.com/watch?v=COd37qgfwcc"
    ]
hilos = [Hilo(1,urls[0]), Hilo(2,urls[1]), Hilo(3,urls[2]), Hilo(4,urls[3]), Hilo(5,urls[4])]
for h in hilos:
    h.start()