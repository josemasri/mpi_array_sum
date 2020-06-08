from mpi4py import MPI
import numpy as np
# Constantes
MAESTRO = 0
ARRAY_TAM = 100

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

tam_subarreglo = np.full((comm_size - 1), int(ARRAY_TAM / (comm_size - 1)))

# Agregando sobrante
num_elementos_sobran = ARRAY_TAM % (comm_size - 1)
for i in range(num_elementos_sobran):
    tam_subarreglo[i] += 1

# Tarea para el maestro
if rank == MAESTRO:
    # Crear el arreglo
    arreglo = np.arange(1, ARRAY_TAM + 1, dtype='i')
    elemento_actual = 0
    for i in range(1, comm_size):
        comm.Send(arreglo[elemento_actual:elemento_actual +
                          tam_subarreglo[i-1]], dest=i, tag=0)
        elemento_actual += tam_subarreglo[i-1]
    # Inicializar suma
    suma = 0
    # Recibir sumas parciales
    for i in range(1, comm_size):
        suma_parcial = comm.recv(source=i, tag=1)
        suma += suma_parcial
    print(suma)

# Tarea para esclavos
else:
    subarreglo = np.empty(tam_subarreglo[rank - 1], dtype='i')
    # Recibiendo mi subarreglo
    comm.Recv(subarreglo, source=0, tag=0)
    # Realizando la suma
    suma = 0
    for elemento in subarreglo:
        suma += elemento
    comm.send(suma, dest=0, tag=1)
