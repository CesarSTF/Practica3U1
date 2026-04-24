import threading
import time
import random

capacidad_vitrina = 10
total_producir = 20

espacios_vacios = threading.Semaphore(capacidad_vitrina)
panes_listos = threading.Semaphore(0)
mutex_vitrina = threading.Lock()
vitrina = []

def panadero():
    try:
        print("[PANADERO] Comenzando jornada laboral...")
        for i in range(1, total_producir + 1):
            pan = f"Pan-{i}"
            time.sleep(random.uniform(0.1, 0.3))
            # cabe en la vitrina? Si no, espera.
            espacios_vacios.acquire()
            try:
                # abrir vitrina
                mutex_vitrina.acquire()
                try:
                    vitrina.append(pan)
                    print(f"[PANADERO] Coloco pan {pan} en la vitrina. (Panes en vitrina: {len(vitrina)})")
                finally:
                    mutex_vitrina.release()
            finally:
                panes_listos.release()
        print("[PANADERO] Jornada laboral finalizada. Todos los panes producidos.")
    except Exception as e:
        print(f"[PANADERO] Error: {e}")

def cliente(id_cliente, cantidad_a_comprar):
    try:
        print(f"[CLIENTE {id_cliente}] Llega a la panadería con hambre.")
        for _ in range(cantidad_a_comprar):
            # ¿Hay pan disponible? Si es 0 espera
            panes_listos.acquire()
            
            try:
                # Abrir vitrina
                mutex_vitrina.acquire()
                try:
                    pan_comprado = vitrina.pop(0)
                    print(f"[CLIENTE {id_cliente}] Compró {pan_comprado}. (En vitrina: {len(vitrina)})")
                except Exception as e_critica:
                    print(f"Error crítico al comprar pan: {e_critica}")
                finally:
                    # Cerrar vitrina
                    mutex_vitrina.release()
            except Exception as e_acq:
                print(f"Error de sincronización (Cliente): {e_acq}")
            finally:
                espacios_vacios.release()
                
            time.sleep(random.uniform(0.4, 0.8))
            
    except Exception as e_hilo:
        print(f"Fallo general en hilo Cliente {id_cliente}: {e_hilo}")

if __name__ == "__main__":
    try:
        hilos = []
        
        # Iniciar Panadero
        hilo_panadero = threading.Thread(target=panadero, name="Hilo-Panadero")
        hilos.append(hilo_panadero)
        hilo_panadero.start()
        
        # Iniciar 4 Clientes
        for i in range(1, 5):
            hilo_cliente = threading.Thread(target=cliente, args=(i, 5), name=f"Hilo-Cliente-{i}")
            hilos.append(hilo_cliente)
            hilo_cliente.start()
            
        # Esperar a que todos terminen
        for hilo in hilos:
            hilo.join()
            
        print("--- La panadería cierra. Todos satisfechos. ---")
        
    except Exception as e_main:
        print(f"Fallo en el programa principal: {e_main}")