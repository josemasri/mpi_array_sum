from mpi4py import MPI
import numpy
MAESTRO = 0
ARRAY_TAM = 100

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

tam_subarreglo = int(ARRAY_TAM / (comm_size - 1))
# Tarea para el maestro
if rank == MAESTRO:
    # Crear el arreglo
    arreglo = numpy.arange(1, ARRAY_TAM+1, dtype='i')
    for i in range(1, comm_size):
        subarreglo = arreglo[(i-1)*tam_subarreglo:(i)*tam_subarreglo]
        comm.Send(subarreglo, dest=i, tag=0)
    # Inicializar suma
    suma = 0
    # Recibir sumas parciales
    for i in range(1, comm_size):
        suma_parcial = comm.recv(source=i, tag=1)
        suma += suma_parcial
    print(suma)

# Tarea para esclavos
else:
    subarreglo = numpy.empty(tam_subarreglo, dtype='i')
    # Recibiendo mi subarreglo
    comm.Recv(subarreglo, source=0, tag=0)
    # Realizando la suma
    suma = 0
    for elemento in subarreglo:
        suma += elemento
    comm.send(suma, dest=0, tag=1)
