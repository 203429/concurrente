import requests
import time
import concurrent.futures
import psycopg2

try:
    connect = psycopg2.connect(database='progcondb', user='postgres', password='PassAlanGG')
    help = connect.cursor()
    help.execute('select version()')
    version = help.fetchone()
except Exception as error:
    print("Error: " + error)

def service(url):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(get_service, url)

def get_service(url):
    response = requests.get(url)
    if response.status_code == 200 :
        data = response.json()
        photos = data
        for photo in photos:
            write_db(photo["title"])
    else:
        pass

def connect_db():
    pass

def write_db(data):
    try:
        help.execute("INSERT INTO photos(title) VALUES ('"+data+"')")
    except Exception as error:
        print("Error: " + error)
    else:
        connect.commit()

if __name__ == "__main__":
    init_time = time.time()
    url_site = ["https://jsonplaceholder.typicode.com/photos"]
    service(url_site)
    end_time = time.time() - init_time
    print(end_time)