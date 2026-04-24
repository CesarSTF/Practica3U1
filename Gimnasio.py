import threading
import time
import random

class MiSemaforo:
    def __init__(self, valor_inicial):
        self.contador = valor_inicial
        self.cerrojo = threading.Lock()
        self.cola_espera = threading.Condition(self.cerrojo)

    def esperar(self):
        try:
            self.cerrojo.acquire()
            while self.contador <= 0:
                self.cola_espera.wait()
            self.contador -= 1
        except Exception as e:
            print(f"Error al esperar en el semáforo: {e}")
        finally:
            self.cerrojo.release()

    def senial(self):
        try:
            self.cerrojo.acquire()
            self.contador += 1
            self.cola_espera.notify()
        except Exception as e:
            print(f"Error al señalizar en el semáforo: {e}")
        finally:
            self.cerrojo.release()

def rutina_atleta(id_atleta, semaforo_gimnasio):
    try:
        print(f"[LLEGADA] Atleta {id_atleta} quiere entrenar. Esperando máquina...")
        
        semaforo_gimnasio.esperar()
        
        try:
            print(f"[ENTRENANDO] Atleta {id_atleta} consiguió máquina. (Máquinas libres restantes: {semaforo_gimnasio.contador})")
            tiempo_uso = random.uniform(1.0, 3.0)
            time.sleep(tiempo_uso)
            
            print(f"[TERMINÓ] Atleta {id_atleta} terminó su rutina de press.")
            
        except Exception as e_rutina:
             print(f"Error durante la rutina del atleta {id_atleta}: {e_rutina}")
        finally:
            semaforo_gimnasio.senial()
            
    except Exception as e_hilo:
        print(f"Fallo general en el hilo del atleta {id_atleta}: {e_hilo}")

if __name__ == "__main__":
    try:
        MAQUINAS_DISPONIBLES = 3
        TOTAL_ATLETAS = 8
        
        semaforo = MiSemaforo(MAQUINAS_DISPONIBLES)
        hilos_atletas = []
        
        print(f"--- Abriendo el Gimnasio con {MAQUINAS_DISPONIBLES} máquinas ---")
        
        for i in range(1, TOTAL_ATLETAS + 1):
            try:
                hilo = threading.Thread(target=rutina_atleta, args=(i, semaforo), name=f"Hilo-Atleta-{i}")
                hilos_atletas.append(hilo)
                hilo.start()
                time.sleep(0.2) 
            except Exception as e_inicio:
                print(f"Error al dejar entrar al atleta {i}: {e_inicio}")
                
        # Esperar a que todos terminen
        for hilo in hilos_atletas:
            try:
                hilo.join()
            except Exception as e_espera:
                print(f"Error esperando a {hilo.name}: {e_espera}")
                
        print("--- Todos los atletas terminaron. Cerrando el Gimnasio ---")

    except Exception as e_main:
         print(f"Fallo en el programa principal: {e_main}")