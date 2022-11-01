# INTEGRANTES:
# ALAN ALBERTO GÓMEZ GÓMEZ - 203429
# CARLOS CAMACHO BELLO - 203456

import threading, time, queue, random

CLIENTES = 20
CAPACIDAD_RESTAURANTE = 10
CAPACIDAD_RESTAURANTE_RESERVARCION = round(CAPACIDAD_RESTAURANTE * 0.2)
CANTIDAD_MESEROS = round(CAPACIDAD_RESTAURANTE * 0.1)
CANTIDAD_COCINEROS = round(CAPACIDAD_RESTAURANTE * 0.1)

restaurante = queue.Queue(CAPACIDAD_RESTAURANTE)
cola_reservacion = queue.Queue(CAPACIDAD_RESTAURANTE_RESERVARCION)
cola_restaurante = queue.Queue()
ordenes = queue.Queue()
ordenes_listas = queue.Queue()

m_recepcionista = threading.Condition()
m_restaurante = threading.Condition()
m_mesero = threading.Condition()
m_cocinero = threading.Condition()

class Recepcionista():
    def atender_con_reservacion(self):
        m_recepcionista.acquire()
        if not cola_reservacion.empty():
            cliente = cola_reservacion.get()
            print("Recepcionista está atendiendo al cliente #" + str(cliente.id) + " con reservación.")
            time.sleep(2)
            self.asignar_mesa(cliente)
            # restaurante.append(cliente)
            # print("Cliente #" + str(cliente.id) + " ingresó al restaurante.")
            m_recepcionista.notify()
            m_recepcionista.release()
        else:
            print("Recepcionista: Cola de reservaciones vacía.")
            m_recepcionista.wait()

    def atender_sin_reservacion(self):
        m_recepcionista.acquire()
        if not cola_restaurante.empty():
            cliente = cola_restaurante.get()
            print("Recepcionista está atendiendo al cliente #" + str(cliente.id) + ".")
            time.sleep(1.5)
            self.asignar_mesa(cliente)
            # restaurante.append(cliente)
            # print("Cliente #" + str(cliente.id) + " ingresó al restaurante.")
            m_recepcionista.notify()
            m_recepcionista.release()
        else:
            print("Recepcionista: Cola de restaurante vacía.")
            m_recepcionista.wait()

    def asignar_mesa(self,cliente):
        m_restaurante.acquire()
        if not restaurante.full():
            print("Cliente #" + str(cliente.id) + " ingresó al restaurante.")
            restaurante.put(cliente)
            print("Cliente #" + str(cliente.id) + " se ha sentado y está listo para ordenar.")
            m_mesero.acquire()
            m_mesero.notify()
            m_mesero.release()
            m_restaurante.release()
        else:
            print("Restaurante lleno, cliente #" + str(cliente.id) + " esperando.")
            m_restaurante.wait()

class Cliente(threading.Thread):
    conta = 1
    orden_tomada = False
    def __init__(self):
        super(Cliente, self).__init__()
        self.id = Cliente.conta
        Cliente.conta += 1

    def reservar(self):
        if not cola_reservacion.full():
            print("Cliente #" + str(self.id) + " ha ingreso a la cola de reservaciones.")
            cola_reservacion.put(self)
            time.sleep(3)
            while True:
                if cola_reservacion.queue[0].id == self.id:
                    recepcionista.atender_con_reservacion()
                    break
        else:
            self.formarse()

    def formarse(self):
        print("Cliente #" + str(self.id) + " ha ingreso a la cola del restaurnate.")
        cola_restaurante.put(self)
        time.sleep(2)
        while True:
            if cola_restaurante.queue[0].id == self.id:
                recepcionista.atender_sin_reservacion()
                break

    def comer(self):
        while True:
            tiempo = random.randint(2,6)    # Tiempo para comer
            if not ordenes_listas.empty():
                comida = ordenes_listas.get()
                print("Cliente #" + str(comida) + " está comiendo")
                time.sleep(tiempo)
                print("Cliente #" + str(comida) + " ha terminado de comer y salio del restaurante")
                break
                # FIN :D

    def run(self):
        des = random.choice([True, False])
        if des:
            self.reservar()
        else:
            self.formarse()
        self.comer()

class Mesero(threading.Thread):
    conta = 1
    def __init__(self):
        super(Mesero, self).__init__()
        self.id = Mesero.conta
        Mesero.conta += 1

    def atender_cliente(self):
        while True:
            m_mesero.acquire()
            if not restaurante.empty():
                cliente = restaurante.get()
                if cliente.orden_tomada == False:
                    print("Mesero #" + str(self.id) + " está atendiendo al cliente #" + str(cliente.id))
                    time.sleep(2)   # Simulación de pedir
                    print("Mesero #" + str(self.id) + " agregó la orden del cliente #" + str(cliente.id) + " a la cola")
                    cliente.orden_tomada = True    # Bloquear
                    ordenes.put(cliente.id)
                    m_cocinero.acquire()
                    m_cocinero.notify()
                    m_cocinero.release()
                    m_mesero.notify()
                    m_mesero.release()
                else:
                    m_mesero.notify()
                    m_mesero.release()
            else:
                print("Mesero #" + str(self.id) + " está libre/descansando.")
                m_mesero.wait()

    def run(self):
        self.atender_cliente()

class Cocinero(threading.Thread):
    conta = 1
    def __init__(self):
        super(Cocinero, self).__init__()
        self.id = Cocinero.conta
        Cocinero.conta += 1

    def cocinar(self):
        while True:
            m_cocinero.acquire()
            if not ordenes.empty():
                orden = ordenes.get()
                print("Cocinero #" + str(self.id) + " está cocinando la orden del cliente #" + str(orden))
                time.sleep(3)
                print("Cocinero #" + str(self.id) + " ha terminado la orden del cliente #" + str(orden))
                ordenes_listas.put(orden)
                m_cocinero.release()
            else:
                print("Cocinero #" + str(self.id) + " está libre/descansando.")
                m_cocinero.wait()
    
    def run(self):
        self.cocinar()

if __name__ == '__main__':
    recepcionista = Recepcionista()

    clientes = []
    for _ in range(CLIENTES):
        clientes.append(Cliente())

    for cm in clientes:
        cm.start()

    meseros = []
    for _ in range(CANTIDAD_MESEROS):
        meseros.append(Mesero())
    
    for me in meseros:
        me.start()

    cocineros = []
    for _ in range(CANTIDAD_COCINEROS):
        cocineros.append(Cocinero())

    for co in cocineros:
        co.start()