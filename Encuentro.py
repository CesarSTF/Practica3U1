import threading
import time
import random

class BarreraSincronizacion:
    def __init__(self, n_total):
        self.contador = 0                                     
        self.n_total = n_total                                
        self.mtx_barrera = threading.Lock()                   
        self.var_cond_barrera = threading.Condition(self.mtx_barrera) 

    def llegar_a_barrera(self, id_hilo):
        try:
            self.mtx_barrera.acquire()                        
            try:
                self.contador += 1                            
                print(f"[Barrera] Hilo {id_hilo} ha llegado al punto de encuentro. ({self.contador}/{self.n_total})")
                
                if self.contador == self.n_total:             
                    print(f"[Barrera] ¡El Hilo {id_hilo} es el último! Despertando a todos...")
                    self.var_cond_barrera.notify_all()       
                else:
                    while self.contador < self.n_total:       
                        self.var_cond_barrera.wait()          
            except Exception as e_critica:
                print(f"Error interno en la barrera para el hilo {id_hilo}: {e_critica}")
            finally:
                self.mtx_barrera.release()                    
                
        except Exception as e_acq:
            print(f"Error de sincronización al llegar a barrera: {e_acq}")


def tarea_hilo(id_hilo, barrera):
    try:
        print(f"[Hilo {id_hilo}] Iniciando Fase 1...")
        tiempo_fase1 = random.uniform(0.5, 3.0) 
        time.sleep(tiempo_fase1)
        print(f"[Hilo {id_hilo}] Terminó Fase 1 en {tiempo_fase1:.2f}s. Esperando a sus compañeros...")
        
        barrera.llegar_a_barrera(id_hilo)
        
        print(f"[Hilo {id_hilo}] Iniciando Fase 2...")
        time.sleep(random.uniform(0.5, 1.0))
        print(f"[Hilo {id_hilo}] Tarea completada.")
        
    except Exception as e_hilo:
        print(f"Fallo general en Hilo {id_hilo}: {e_hilo}")

if __name__ == "__main__":
    try:
        N_HILOS = 5
        mi_barrera = BarreraSincronizacion(N_HILOS)
        hilos = []
        
        print("--- Inicio de procesamiento paralelo en 2 Fases ---")
        
        for i in range(1, N_HILOS + 1):
            t = threading.Thread(target=tarea_hilo, args=(i, mi_barrera), name=f"Hilo-Proceso-{i}")
            hilos.append(t)
            t.start()
            
        for hilo in hilos:
            hilo.join()
            
        print("--- Todo el procesamiento finalizó con éxito ---")
        
    except Exception as e_main:
         print(f"Fallo en el programa principal: {e_main}")