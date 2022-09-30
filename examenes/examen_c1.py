# Alan Alberto Gómez Gómez
# 203429

import threading
from time import sleep

persona_comiendo = threading.Lock()

class Persona(threading.Thread):
    def __init__(self,id,palillo_izq,palillo_der):
        threading.Thread.__init__(self)
        self.id = id
        self.palillo_izq = palillo_izq
        self.palillo_der = palillo_der

    def get_palillo_izq(self):
        return self.palillo_izq

    def set_palillo_der(self,palillo_der):
        self.palillo_der = palillo_der
    
    def set_palillo_izq(self,palillo_izq):
        self.palillo_izq = palillo_izq

    def run(self):
        persona_comiendo.acquire()
        comer(self.id)
        persona_comiendo.release()

def comer(id):
    print("Persona " + str(id) + " comiendo.")
    palillo_izq = personas[id-1].get_palillo_izq()
    if id == len(personas): # Al llegar la última persona este usará el palillo de la primera persona
        id = 0
    palillo_der = personas[id].get_palillo_izq()
    personas[id].set_palillo_izq(-1)    # Estado -1 indica que no tiene palillo disponible
    print("Usando su palillo izquierdo " + str(palillo_izq))
    print("Usando el palillo derecho de la persona " + str(palillo_der))
    personas[id].set_palillo_izq(palillo_der)
    sleep(5)
    print("Ha terminado de comer.\n")
    sleep(1)

# La clase persona contiene su ID de la persona, ID del palillo izquierdo e ID del palillo derecho.
# Cada ID de persona y palillo izquierdo son iguales para identificar que este usando el suyo
personas = [Persona(1,1,0),Persona(2,2,0),
Persona(3,3,0),Persona(4,4,0),
Persona(5,5,0),Persona(6,6,0),
Persona(7,7,0),Persona(8,8,0)]

for x in personas:
    x.start()