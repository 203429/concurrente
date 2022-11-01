# Crear una aplicación con las siguientes características.

# Existen uno o más productores y uno o más consumidores, todos almacenan y extraen productos de una misma bodega. El productor produce productos cada vez que puede, y el consumidor los consume cada vez que lo necesita.

# Problema:
# coordinar a los productores y consumidores, para que los productores no produzcan más ítems de los que se pueden almacenar en el momento, y los consumidores no adquieran más ítems de los que hay disponibles.

# PARA ESTO APLICARA METODOS DE SINCRONIZACIÓN Y COMUNICACIÓN JUNTO A SEMAFOROS
import threading, time, random

bodega = []
CAPACIDAD = 10
cola = threading.Semaphore(10)
item = threading.Semaphore(0)
mutex = threading.Lock()

PRODUCTORES = 5
CONSUMIDORES = 5

class Productor(threading.Thread):
    conta = 0
    def __init__(self):
        super(Productor, self).__init__()
        self.id = Productor.conta
        Productor.conta += 1

    def producir(self):
        print("Productor #" + str(self.id) + " produciendo.")
        item = random.randint(1,10)
        print("Productor #" + str(self.id) + " ha producido el item #" + str(item))
        bodega.append(item)
        print("Items en la cola: " + str(bodega))

    def run(self):
        while True:
            if len(bodega) >= CAPACIDAD:
                print("Bodega llena")
            else:
                cola.acquire()
                mutex.acquire()
                self.producir()
                mutex.release()
                item.release()
            time.sleep(6)

class Consumidor(threading.Thread):
    conta = 0
    def __init__(self):
        super(Consumidor, self).__init__()
        self.id = Consumidor.conta
        Consumidor.conta += 1

    def consumir(self):
        print("Consumidor #" + str(self.id) + " está consumiendo.")
        item = bodega.pop(0)
        print("Consumidor #" + str(self.id) + " ha consumido item #" + str(item))
        print("Items en la cola: " + str(bodega))

    def run(self):
        while True:
            if len(bodega) == 0:
                print("Bodega vacia")
            else:
                item.acquire()
                mutex.acquire()
                self.consumir()
                mutex.release()
                cola.release()
            time.sleep(6)

def main():
    productores = []
    for i in range(PRODUCTORES):
        productores.append(Productor())

    consumidores = []
    for j in range(CONSUMIDORES):
        consumidores.append(Consumidor())
    
    for p in productores:
        p.start()

    for c in consumidores:
        c.start()

if __name__ == '__main__':
    main()