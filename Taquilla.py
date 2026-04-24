import threading
import time

boletos_vendidos = 0
n_hilos = 5
m_ventas = 1000000

mutex = threading.Lock()

def ejecutar_venta():
    global boletos_vendidos

    try:
        for i in range(m_ventas):
            mutex.acquire()
            try:
                boletos_vendidos += 1
            except Exception as e:
                print(f"Error al vender boleto: {e}")
            finally:
                mutex.release()
    except Exception as e:
        print(f"Error en el hilo de venta: {e}")

if  __name__== "__main__":
    try:
        print("Iniciando venta de boletos...")
        tiempo_inicio = time.time()

        hilos = []

        for j in range(n_hilos):
            try:
                hilo = threading.Thread(target=ejecutar_venta, name=f"Hilo-{j+1}")
                hilos.append(hilo)
                hilo.start()
            except Exception as e:
                print(f"Error al iniciar hilo {j+1}: {e}")
        
        # esperar a que todos los hilos terminen
        for hilo in hilos:
            try:
                hilo.join()
            except Exception as e:
                print(f"Error al esperar hilo {hilo.name}: {e}")
        
        tiempo_fin = time.time()

        print(f"Venta de boletos finalizada. Total de boletos vendidos: {boletos_vendidos}")
        print(f"Tiempo total de venta: {tiempo_fin - tiempo_inicio:.2f} segundos")
    except Exception as e:
        print(f"Error en el proceso principal: {e}")
        





