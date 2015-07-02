from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import time
import random

#parametros a utilizar en la creacion del pdf
def crearPDF(arbol,suelo,dist,tam,mean,tiempo,nombre):

    #Usar nombre del arbol
    if arbol == 1:
        nomArbol = "Quillay"
    if arbol == 2:
        nomArbol = "Peumo"
    if arbol == 3:
        nomArbol = "Boldo"
    if arbol == 4:
        nomArbol = "Roble"
    if arbol == 5:
        nomArbol = "Rauli"

    #Usar nombre del suelo
    if suelo == 1:
        nomSuelo = "Serranias aridas o semiaridas"
    if suelo == 2:
        nomSuelo = "Granitico"
    if suelo == 3:
        nomSuelo = "Vertisoles"
    if suelo == 4:
        nomSuelo = "Aluviales del valle central"

    puntoa = random.randint(0,tam)
    puntob = random.randint(0,tam)
    puntoc = random.randint(0,tam)

    #ancho = 612
    #alto = 792
    name = nombre + ".pdf"
    c=canvas.Canvas(name, pagesize = letter)
    #cabecera
    c.setFont("Helvetica-Oblique",8)
    c.drawImage("/mpi/Percolacion/perFinal/logo.png",10,700,width=50,height=50)
    c.drawString(70,740,"Universidad Tecnologica Metropolitana de Chile")
    c.drawString(70,730,"Ingenieria Civil en Compiutacion Mencion Informtica")
    c.drawString(70,720,"Computacion Paralela")
    c.drawString(70,710,"Plataforma Integrada")


    #Titulo
    c.setFont("Helvetica-Bold",30)
    c.drawString(140,629,"Resultado Percolacion")
    c.line(50,620,562,620)
    #Subtitulo
    c.setFont("Helvetica-Oblique",20)
    c.drawString(220,600,"Incendio Forestal")


    #Cuerpo
    #input
    c.setFont("Helvetica",15)
    c.drawString(100,550,"Los parametros de entrada para esta simulacion son:")
    c.setFont("Helvetica-Oblique",15)
    sArbol = "Arbol: " + nomArbol
    sSuelo = "Suelo: " + nomSuelo
    sDist = "Distribucion: " + str(dist) + "%"
    sTam = "Tamano: " + str(tam) + " Hectareas"
    c.drawString(150,500,sArbol)
    c.drawString(150,480,sSuelo)
    c.drawString(150,460,sDist)
    c.drawString(306,460,sTam)
    #output
    c.setFont("Helvetica",15)
    c.drawString(100,415,"Luego de haber realizado 385 repeticiones para obtener un")
    c.drawString(100,398,"error menor al 5% podemos obtener los siguientes resultados: ")
    sMean = "Probabilidad de propagacion del incendio: " + str(mean)
    meanpor = int(mean*100)
    sMeanPor = "Equivalente a un: " + str(meanpor) + "%." 
    sTiempo = "Tiempo de ejecucion de la simulacion: " + str(tiempo) + " Segundos"
    punt = "los 3 focos de la matriz cuadrada son " + str(puntoa) + ", " + str(puntob) + " y " + str(puntoc)
    c.drawString(150,348,sMean)
    c.drawString(150,328,sMeanPor)
    c.drawString(150,308,sTiempo)
    c.drawString(150,308,punt)
    # c.drawImage("/mpi/Percolacion/perFinal/logo.png",200,80,width=200,height=200)


    #Pie de pagina
    c.line(20,40,582,40)
    c.setFont("Helvetica-Bold",8)
    c.drawString(180,30,"Recuerda seguir utilizando nuestra pagina : 00-ironman.clustermaarvel.utem")
    now = "Documento creado en :" + time.strftime("%c")
    c.drawString(230,20,now)
    c.showPage()
    c.save()