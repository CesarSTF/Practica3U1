import threading
import time
import random

cant_lectores = 0
mutex_lectores = threading.Lock() 
sem_escritor = threading.Lock()   

def lector(id_lector):
    global cant_lectores
    try:
        print(f"[Estudiante {id_lector}] Llega frente al tablón...")
        
        mutex_lectores.acquire()
        try:
            cant_lectores += 1
            if cant_lectores == 1:
                sem_escritor.acquire()
        except Exception as e_entrada:
            print(f"Error en entrada de Estudiante {id_lector}: {e_entrada}")
        finally:
            mutex_lectores.release()
            
        print(f"[Estudiante {id_lector}] LEYENDO... (Lectores actuales: {cant_lectores})")
        time.sleep(random.uniform(0.5, 1.5)) 
        print(f"[Estudiante {id_lector}] Terminó de leer.")
        
        mutex_lectores.acquire()
        try:
            cant_lectores -= 1
            if cant_lectores == 0:
                sem_escritor.release()
        except Exception as e_salida:
            print(f"Error en salida de Estudiante {id_lector}: {e_salida}")
        finally:
            mutex_lectores.release()
            
    except Exception as e_hilo:
        print(f"Error general en Estudiante {id_lector}: {e_hilo}")

def escritor(id_escritor):
    try:
        print(f"[Profesor {id_escritor}] Llega y necesita el tablón exclusivamente...")
        
        sem_escritor.acquire()
        try:
            print(f"[Profesor {id_escritor}] ESCRIBIENDO... ¡Nadie más puede leer ni escribir!")
            time.sleep(random.uniform(1.0, 2.0)) 
            print(f"[Profesor {id_escritor}] Terminó de actualizar las notas.")
        except Exception as e_critica:
            print(f"Error crítico al escribir: {e_critica}")
        finally:
            sem_escritor.release()
            
    except Exception as e_hilo:
        print(f"Error general en Profesor {id_escritor}: {e_hilo}")

if __name__ == "__main__":
    try:
        hilos = []
        
        print("--- Inicia la jornada académica ---")
        
        for i in range(1, 4):
            t = threading.Thread(target=lector, args=(i,), name=f"Hilo-Estudiante-{i}")
            hilos.append(t)
            t.start()
            
        time.sleep(0.1) 
        
        t_profesor = threading.Thread(target=escritor, args=(1,), name="Hilo-Profesor-1")
        hilos.append(t_profesor)
        t_profesor.start()
        
        time.sleep(0.1)
        for i in range(4, 6):
            t = threading.Thread(target=lector, args=(i,), name=f"Hilo-Estudiante-{i}")
            hilos.append(t)
            t.start()
            
        for hilo in hilos:
            hilo.join()
            
        print("--- Fin de la jornada. Tablón libre. ---")
        
    except Exception as e_main:
        print(f"Fallo en el programa principal: {e_main}")