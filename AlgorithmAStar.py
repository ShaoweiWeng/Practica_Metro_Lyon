import igraph 
from igraph import* 
import csv
from geopy.distance import geodesic 
import time;
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

heuristica={}

with open('estaciones.csv', mode='r') as file:
    # Crea un lector CSV
    reader = csv.reader(file)
    
    # Salta la primera fila que contiene los encabezados
    next(reader)
    
    # Inicializa una lista para almacenar los valores de la columna de estaciones
    nombre = []
    coordenada = {}
    # Itera a traves de las filas del archivo CSV
    for row in reader:
        # Agrega el valor de la columna "Estacion" a la lista
        nombre.append(row[1])
        x = (float)(row[3]) # Coordenadas X
        y = (float)(row[4]) # Coordenadas Y
        coordenada.update({row[1]:[x,y]})


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
                    pesos.append(float(valor))
                    aristas.append((i, j))


def calculoHeuristica(destino):
    destinoX = coordenada.get(destino)[0]
    destinoY = coordenada.get(destino)[1]
    for origen in coordenada:
        origenX = coordenada.get(origen)[0]
        origenY = coordenada.get(origen)[1]
        distanciaLineaRecta = geodesic((destinoX,destinoY),(origenX,origenY)).km
        heuristica.update({origen:distanciaLineaRecta})


n_vertices = 40
print(aristas)
grafo = igraph.Graph(n_vertices, aristas)   # Creamos grafo
grafo["title"] = "Metro de Lyon" # Titulo del grafo
grafo.vs["name"] = nombre   # Nombre de los nodos
grafo.es["pesos"] = pesos   # Pesos de las arista
grafo.vs["color"] = ['red','red','red','red','red','red','red', 'red','red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red']
grafo.vs["label"] = nombre
grafo.vs["size"] = 70
grafo.vs["label_dist"] = 1.5
grafo.vs["label_size"] = 20

class Nodo:     
    def __init__(self, estacion, g = 0, h = 0):  
        self.estacion = estacion     #el propio nodo
        self.padre = None          #nodo padre
        self.g = g                 #valor g
        self.h = h                 #valor h
        self.f = 0                 #valor f
  

def algoritmoAStar(Inicio,Destino):
   # inicialización de variable
   estacioInicio = grafo.vs.find(Inicio)
   estacionDestino = grafo.vs.find(Destino)
   coste = 0
   calculoHeuristica(estacionDestino["name"])
   listaNodoAbierto = {}
   listaNodoCerrado = {}
   ruta = []
   nodoInicio = Nodo(estacioInicio)
   nodoDestino = Nodo(estacionDestino)
   nodoActual = nodoInicio
   listaNodoAbierto.update({estacioInicio["name"]:nodoActual})
   
   while(listaNodoAbierto):
      # seleccionar el nodo con f menor y elimian de la lista abierto añadir en la lista cerrado
      nodoActual = getNodoMinimo(listaNodoAbierto)
      listaNodoCerrado.update({nodoActual.estacion["name"]:nodoActual})
      del listaNodoAbierto[nodoActual.estacion["name"]]
      explorarVecino(grafo,heuristica,listaNodoAbierto,listaNodoCerrado,nodoActual)
      nodo = hayDestinoEnListaNodoAbierto(listaNodoAbierto,estacionDestino)
      
      if nodo != None:
         coste = nodo.g
      while nodo != None:
         ruta.append(nodo.estacion["name"])
         indice_nodo = grafo.vs.find(name=(nodo.estacion["name"])).index
         grafo.vs[indice_nodo]["color"] = 'green'
         if nodo.padre != None:
            indiceArista = grafo.get_eid(nodo.estacion,nodo.padre.estacion)
            grafo.es[indiceArista]["width"] = 3.0
         nodo = nodo.padre
         listaNodoAbierto={}

   for estacion in reversed(ruta):
      print(estacion)
   print("coste de distancia es {:.1f}km".format(coste))

def hayDestinoEnListaNodoAbierto(listaNodoAbierto,estacionDestino):
    for estacion in listaNodoAbierto:
        nodo = listaNodoAbierto.get(estacion)
        if nodo.estacion == estacionDestino:
            return nodo
    return None

#metodo que devuelve un nodo con f menor en la lista de nodo abierto 
def getNodoMinimo(listaNodoAbierto):
    menor = 11111111111
    for estacion in listaNodoAbierto:
        nodo = listaNodoAbierto.get(estacion)  
        if nodo.f < menor:  
            nodoMenor = nodo
            menor =  nodo.f 
        return nodoMenor

#exploral todos los nodos vecino de nodo actual y calcuar la f 
def explorarVecino(grafo:igraph,heuristica,listaNodoAbierto,listaNodoCerrado,nodoActual):
    verticeVecino = nodoActual.estacion.neighbors()
    for estacion in verticeVecino:
      
        if estacion["name"] in listaNodoCerrado:
            continue
        nodo = Nodo(estacion)
        indiceArista = grafo.get_eid(nodoActual.estacion,estacion)
        peso = grafo.es[indiceArista]["pesos"]
        g = peso + nodoActual.g
        h = heuristica.get(estacion["name"])
        f = g+h
        nodo.g = g
        nodo.h = h
        nodo.f = f
        nodo.padre = nodoActual

        if estacion in listaNodoAbierto:
            nodoAux = listaNodoAbierto.get(estacion["name"])
            if nodo.f < nodoAux.f:
                listaNodoAbierto.update({estacion["name"]:nodo})
        else:
             listaNodoAbierto.update({estacion["name"]:nodo})

app = tk.Tk()
origen = tk.StringVar(app)
destino = tk.StringVar(app) 

def boton():
    inicio = origen.get()
    final = destino.get()
    algoritmoAStar(inicio, final)

    # Eliminar el gráfico existente
    subplot.clear()

    # Volver a dibujar el nuevo gráfico
    igraph.plot(grafo, target=subplot, bbox=(0, 0, 200, 200))

    # Actualizar el lienzo
    canvas.draw()
    
app.geometry("1920x1080")
app.configure(background="black")
tk.Wm.wm_title(app,"A*")
tk.Button(app,
          text="Click Me!",
          font=("Courier", 14),
          bg="#00a8e8",
          fg="blue",
          command=boton,
          height=2,
          width=15 
).pack()

figura = Figure(figsize=(8, 8))

# Obtener el subplot de la figura
subplot = figura.add_subplot(111)

# Visualizar el grafo en el subplot
igraph.plot(grafo, target=subplot, bbox=(0, 0, 200, 200))

# Crear el lienzo de Matplotlib para integrarlo en la interfaz de Tkinter
canvas = FigureCanvasTkAgg(figura, master=app)
canvas.draw()

# Colocar el lienzo en la ventana principal
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

tk.Label(app, text="ORIGEN:").pack(side=tk.LEFT)

tk.Entry(app,
    fg="blue",
    bg="white",
    justify="center",
    textvariable=origen
).pack(side=tk.LEFT)

tk.Label(app, text="DESTINO:").pack(side=tk.LEFT)

tk.Entry(app,
    fg="blue",
    bg="white",
    justify="center",
    textvariable=destino
).pack(side=tk.LEFT)


app.mainloop()
