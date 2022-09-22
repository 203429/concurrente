from threading import Thread, Semaphore
semaforo = Semaphore(1) # Crea la variable semáforo

def critico(id):
    global x;
    x = x + id
    print("Hilo = " + str(id) + " => " + str(x))
    x = 1

class Hilo(Thread):
    def __init__(self,id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        semaforo.acquire() # Inicializa semáforo, lo adquiere
        critico(self.id)
        semaforo.release() # Libera un semáforo e incrementa la variable semáforo

threads_semaphore = [Hilo(1), Hilo(2), Hilo(3)]
x = 1;
for t in threads_semaphore:
    t.start()