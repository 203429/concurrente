import requests
import threading
import psycopg2
import time
from pytube import YouTube

from dotenv import load_dotenv
import os
load_dotenv()

try:
    connect = psycopg2.connect(database=os.getenv("DATABASE"), user=os.getenv("USER_DB"), password=os.getenv("PASSWORD_DB"))
    help = connect.cursor()
    help.execute('select version()')
    version = help.fetchone()
except Exception as error:
    print("Error: " + error)

def get_video():
    urls = [
    "https://www.youtube.com/watch?v=GXD0ySQFxRQ",
    "https://www.youtube.com/watch?v=NUz4d-bd2hs",
    "https://www.youtube.com/watch?v=xU8m9X-1fgE",
    "https://www.youtube.com/watch?v=RAPrd4jpxxI",
    "https://www.youtube.com/watch?v=COd37qgfwcc"
    ]
    for url in urls:
        th_video_download = threading.Thread(target=video_download, args=[url])
        th_video_download.start()

def video_download(url):
    path = "C:/Users/IzAla/Downloads/videos"
    print(f'Descargando URL:  = {url}')
    try:
        YouTube(url).streams.first().download(path)
        print(f'URL Descargado:  = {url}')
    except Exception as error:
        print("Error: " + error)

def get_api_data():
    url = 'https://jsonplaceholder.typicode.com/photos'
    response = requests.get(url)
    if response.status_code == 200 :
        data_list = response.json()
        for data in data_list:
            print("Escribiendo en la base de datos: " + str(data["id"]))
            write_db(data["title"])
    else:
        pass

def write_db(data):
    try:
        help.execute("INSERT INTO act2(info) VALUES ('"+data+"')")
    except Exception as error:
        print("Error: " + error)
    else:
        connect.commit()

def get_api_service():
    for x in range(0,50):
        th_service = threading.Thread(target=get_service, args=[x])
        th_service.start()
        time.sleep(0.3)

def get_service(dato=0):
    response = requests.get('https://randomuser.me/api/')
    if response.status_code == 200:
        # print(f'Dato = {dato}')
        results = response.json().get('results')
        name = results[0].get('name').get('first')
        print(name)

if __name__ == '__main__':
    th1 = threading.Thread(target=get_video)
    th1.start()
    th2 = threading.Thread(target=get_api_data)
    th2.start()
    th3 = threading.Thread(target=get_api_service)
    th3.start()