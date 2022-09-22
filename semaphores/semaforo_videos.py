from threading import Thread, Semaphore
from pytube import YouTube
semaforo = Semaphore(1) # Crea la variable semáforo

def critico(id,url):
    print("Hilo = " + str(id) + " Video = " + url)
    path = "C:/Users/IzAla/Downloads/videos"
    try:
        YouTube(url).streams.first().download(path)
        print(f'URL Descargado:  = {url}')
    except Exception as error:
        print("Error: " + error)

class Hilo(Thread):
    def __init__(self,id,url):
        Thread.__init__(self)
        self.id = id
        self.url = url

    def run(self):
        semaforo.acquire() # Inicializa semáforo, lo adquiere
        critico(self.id, self.url)
        semaforo.release() # Libera un semáforo e incrementa la variable semáforo

urls = [
    "https://www.youtube.com/watch?v=GXD0ySQFxRQ",
    "https://www.youtube.com/watch?v=NUz4d-bd2hs",
    "https://www.youtube.com/watch?v=xU8m9X-1fgE",
    "https://www.youtube.com/watch?v=RAPrd4jpxxI",
    "https://www.youtube.com/watch?v=COd37qgfwcc"
    ]
threads_semaphore = [Hilo(1,urls[0]), Hilo(2,urls[1]), Hilo(3,urls[2]), Hilo(4,urls[3]), Hilo(5,urls[4])]
for t in threads_semaphore:
    t.start()