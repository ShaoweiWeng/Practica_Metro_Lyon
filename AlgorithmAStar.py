
from tkinter import ttk
import igraph 
from igraph import* 
import csv
from geopy.distance import geodesic 
import time;
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import random
from igraph.drawing.text import *

class Nodo:     
    def __init__(self, estacion, g = 0, h = 0):  
        self.estacion = estacion     #el propio nodo
        self.padre = None          #nodo padre
        self.g = g                 #valor g
        self.h = h                 #valor h
        self.f = 0      
   
class AutoCanvasUpdaterApp:

    nombreEstacion = []
    cordenadaEstacion={}
    dirFileEstacion='estaciones.csv'
    heuristica={}
    aristas = []
    pesos = []
    origen=None
    destino=None
    ejec = False
    res = True
    color = []
    def __init__(self, master):
        self.readFileEstacion()
        self.readFileArista()
        self.construirGrafo()

        self.master = master
        self.master.title("A star ")

        self.master.geometry("1920x1080")
        self.master.configure(background="black")

        # Crear un lienzo
        frame = tk.Frame(self.master)
        frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(frame, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # Inicializar el contenido del lienzo
        self.igraph_plot = Plot()
        self.igraph_plot.add(self.grafo, layout="kk")
        self.auto_update_canvas()
        # Programar la primera actualización después de 1000 milisegundos (1 segundo)

    def draw_initial_content(self):
        self.grafo.vs["color"] = ['red','red','red','red','red','red','red', 'red','red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red']
        self.auto_update_canvas()

    def auto_update_canvas(self):
        
        self.canvas.delete("all")
        igraph_plot = plot(self.grafo, bbox=(1, 2, 1000, 800), margin=50)
        igraph_plot.save("graph_plot.png")
        image = tk.PhotoImage(file="graph_plot.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        self.canvas.image = image

    def readFileArista(self):
        with open('aristas.csv', mode='r') as file:
            # Crea un lector CSV
            reader = csv.reader(file)
            # Salta la primera fila que contiene los encabezados
            next(reader)
            # Itera a traves de las filas del archivo CSV
            for i, row in enumerate(reader):
                for j, valor in enumerate(row[1:]):  # Empezamos desde la columna 1 para omitir la primera columna
                    if( i<= j): # Si no se ha llegado aun a la diagonal principal (Queremos evitar aristas repetidas)
                        if valor != "0":
                            self.pesos.append(float(valor))
                            self.aristas.append((i, j))
    """ separador  """
    def readFileEstacion(self):
        with open(self.dirFileEstacion, mode='r') as file:
            # Crea un lector CSV
            reader = csv.reader(file)
            # Salta la primera fila que contiene los encabezados
            next(reader)
            # Inicializa una lista para almacenar los valores de la columna de estaciones
            # Itera a traves de las filas del archivo CSV
            for row in reader:
                # Agrega el valor de la columna "Estacion" a la lista
                self.nombreEstacion.append(row[1])
                self.color.append('red')
                x = (float)(row[3]) # Coordenadas X
                y = (float)(row[4]) # Coordenadas Y
                self.cordenadaEstacion.update({row[1]:[x,y]})
    """" separador"""
    def calculoHeuristica(self,destino):
        destinoX = self.cordenadaEstacion.get(destino)[0]
        destinoY = self.cordenadaEstacion.get(destino)[1]
        for origen in self.cordenadaEstacion:
            origenX = self.cordenadaEstacion.get(origen)[0]
            origenY = self.cordenadaEstacion.get(origen)[1]
            distanciaLineaRecta = geodesic((destinoX,destinoY),(origenX,origenY)).km
            self.heuristica.update({origen:distanciaLineaRecta})
    """" separador """
    def construirGrafo(self):
        self.grafo = igraph.Graph(len(self.nombreEstacion),self.aristas)
        self.grafo["title"] = "Metro de Lyon" # Titulo del grafo
        self.grafo.vs["name"] = self.nombreEstacion   # Nombre de los nodos
        self.grafo.es["pesos"] = self.pesos   # Pesos de las arista   
        self.grafo.vs["color"] = self.color
        self.grafo.vs["label"] = self.nombreEstacion
        self.grafo.vs["size"] = 35
        self.grafo.vs["label_dist"] = 1.1
        self.grafo.vs["label_size"] = 13
    """" separador """
    def algoritmoAStar(self,Inicio,Destino):
        # inicialización de variable
        estacioInicio = self.grafo.vs.find(Inicio)
        estacionDestino = self.grafo.vs.find(Destino)
        coste = 0
        self.calculoHeuristica(Destino)
        listaNodoAbierto = {}
        listaNodoCerrado = {}
        ruta = []
        nodoInicio = Nodo(estacioInicio)
        nodoDestino = Nodo(estacionDestino)
        nodoActual = nodoInicio
        nodoActual.f = self.heuristica.get(Inicio)
        listaNodoAbierto.update({estacioInicio["name"]:nodoActual})
        index = 0
        while(nodoActual):
        # seleccionar el nodo con f menor y elimian de la lista abierto añadir en la lista cerrado
            index=self.nombreEstacion.index(nodoActual.estacion["name"])
            self.grafo.vs[index]["color"] = "black"

            #print(nodoActual.estacion["name"])
            #print(nodoActual.f)
            #print(nodoActual.g)
            #print(nodoActual.h)
            #print("----------")

            self.auto_update_canvas()
            self.master.update()
            self.grafo.vs[index]["color"] = "yellow"
            
            if nodoActual.estacion == nodoDestino.estacion:
                self.grafo.vs["color"] = ['red','red','red','red','red','red','red', 'red','red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red', 'red','red','red','red','red','red','red', 'red']
                self.auto_update_canvas()
                self.master.update()

                time.sleep(0.5)

                index=self.nombreEstacion.index(nodoActual.estacion["name"])
                self.grafo.vs[index]["color"] = "green"
                self.auto_update_canvas()
                self.master.update()

                coste = nodoActual.f
                ruta.append(nodoActual.estacion["name"])
                nodo = nodoActual.padre
                while(nodo):
                    ruta.append(nodo.estacion["name"])

                    index=self.nombreEstacion.index(nodo.estacion["name"])
                    self.grafo.vs[index]["color"] = "green"
                    self.auto_update_canvas()
                    self.master.update()

                    nodo = nodo.padre
                return ruta,coste
            else:
                
                listaNodoCerrado.update({nodoActual.estacion["name"]:nodoActual})
                del listaNodoAbierto[nodoActual.estacion["name"]]
                self.explorarVecino(listaNodoAbierto,listaNodoCerrado,nodoActual)
                nodoActual = self.getNodoMinimo(listaNodoAbierto)
            
            time.sleep(0.5)
        return None,None
    
    def getNodoMinimo(self,listaNodoAbierto):
        menor = 100000
        nodoMenor = None
        for estacion in listaNodoAbierto:
            nodo = listaNodoAbierto.get(estacion) 
            if nodo.f < menor:
                nodoMenor = nodo
                menor = nodoMenor.f
        return nodoMenor
    
    def explorarVecino(self,listaNodoAbierto,listaNodoCerrado,nodoActual):
        verticeVecino = nodoActual.estacion.neighbors()
        for estacion in verticeVecino:
            
            if estacion["name"] in listaNodoCerrado:
                continue
            nodo = Nodo(estacion)
            indiceArista = self.grafo.get_eid(nodoActual.estacion,estacion)
            peso = self.grafo.es[indiceArista]["pesos"]
            g = peso + nodoActual.g
            h = self.heuristica.get(estacion["name"])
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

def boton():
        inicio = origen.get()
        final =  destino.get()
        if (app.res and (not app.ejec)) : 
            app.res = False
            app.ejec = True
            app.algoritmoAStar(inicio, final)
            app.ejec = False

def restart():
        if(not app.ejec):
            app.res = True
            app.draw_initial_content()


def obtenerNombre():
    with open('estaciones.csv', mode='r') as file:
        # Crea un lector CSV
        reader = csv.reader(file)
        # Salta la primera fila que contiene los encabezados
        next(reader)

        # Inicializa una lista para almacenar los valores de la columna de estaciones
        nombre = []
        for row in reader:
            # Agrega el valor de la columna "Estacion" a la lista
            nombre.append(row[1])
    return nombre
    

if __name__ == "__main__":
    root = tk.Tk()
    origen = tk.StringVar(root)
    destino = tk.StringVar(root) 

    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, fill=tk.BOTH)

    nombre = obtenerNombre()
    
    tk.Button(frame,text="START!",font=("Courier", 14),bg="#00a8e8",fg="blue",command=boton,height=2,width=15).pack(side=tk.LEFT)
    tk.Button(frame,text="RESTART!",font=("Courier", 14),bg="#00a8e8",fg="blue",command=restart,height=2,width=15).pack(side=tk.LEFT)
    tk.Label(frame, text="ORIGEN:").pack(side=tk.LEFT)
    ttk.Combobox(frame,textvariable=origen, values=nombre).pack(side=tk.LEFT)
    tk.Label(frame, text="DESTINO:").pack(side=tk.LEFT)
    ttk.Combobox(frame,textvariable=destino, values=nombre).pack(side=tk.LEFT)

    app = AutoCanvasUpdaterApp(root)
    root.mainloop()