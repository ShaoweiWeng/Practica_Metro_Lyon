import igraph 
from igraph import* 
import csv 


#-.-.-.-.-.-.-OBTENER ESTACIONES (vertices del grafo) DE CSV-.-.-.-.-.-.-
with open('estaciones.csv', mode='r') as file:
    # Crea un lector CSV
    reader = csv.reader(file)
    next(reader)
    # Inicializa una lista para almacenar los valores de la columna de estaciones
    nombre = []
    
    # Itera a traves de las filas del archivo CSV
    for row in reader:
        # Agrega el valor de la columna "Estacion" a la lista
        nombre.append(row[1])


#-.-.-.-.-.-.-OBTENER ARISTAS Y PESOS(conexiones entre estaciones) DE CSV-.-.-.-.-.-.-
with open('aristas.csv', mode='r') as file:
    # Crea un lector CSV
    reader = csv.reader(file)
    
    # Salta la primera fila que contiene los encabezados
    next(reader)
    
    # Inicializa una lista para almacenar las aristas y pesos
    aristas = []
    pesos = []

    # Itera a traves de las filas del archivo CSV
    for i, row in enumerate(reader):
        for j, valor in enumerate(row[1:]):  # Empezamos desde la columna 1 para omitir la primera columna
            if( i<= j): # Si no se ha llegado aun a la diagonal principal (Queremos evitar aristas repetidas)
                if valor != "0":
                    pesos.append(int(valor))
                    aristas.append((i, j))


#-.-.-.-.-.-.-PREPARAR GRAFO-.-.-.-.-.-.-
n_vertices = 40

g = igraph.Graph(n_vertices, aristas)   # Creamos grafo
g["title"] = "Metro de Lyon" # Titulo del grafo
g.vs["estacion"] = nombre   # Nombre de los nodos
g.es["pesos"] = pesos   # Pesos de las aristas


#IMPORTANTE: COMO BUSCAR NODOS CON SU NOMBRE!!!!!!!
#vertice= g.vs.select(estacion="Saxe-Gambetta")  # Selecionar secuencia de vertices con nombre "Saxe-Gambetta"
#v = vertice.find()  # Escogemos el primer vertice de la secuencia (solo hay un nodo en la secuencia)
#print(v.neighbors()) # imprimir nodos vecinos

