#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from Libro.mail import envio_mail
from mpi4py import MPI
from numpy import *
import sys
import os
import time
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist
from Bio import SeqIO

#Librerias para PDF

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

#Módulos para enviar mail:

import requests

# Se incluyen modulos para sacar Advertencias (warnings)
import warnings
warnings.filterwarnings('ignore')

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

# Se define el arreglo que poseera la informacion de la secuancia de ADN a
# comparar
subArreglo1 = list(range(1000))
# Se define el arreglo correspondiente a la nesima secuencia contenida en
# la base de datos
subArreglo2 = list(range(1000))

def envio_mail(mail, nombre):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org/messages",
        auth=("api", "key-bccd075f02a12db1dee03a7710800a5d"),
        files=[("attachment", open("/var/www/html/webParalela/FASTA/Envio/"+nombre+".pdf")),
                           ("attachment", open("/var/www/html/webParalela/FASTA/Envio/"+nombre+".fasta"))],
        data={"from": "Cluster Marvel<postmaster@sandbox3761d267c8184fa2afb562ff83f8881e.mailgun.org>",
              "to": "<"+mail+">",
              "subject": "Resultados Alineamiento de Secuencias",
              "text":
              "Hola. Se adjuntan 2 archivos con la respuesta a su pedido:"
              "\nUn PDF con información general ("+nombre+".pdf) y un archivo FASTA con el detalle de las alineaciones de ADN("+nombre+".fasta)."
              "\n\nRealizado por: http://00-ironman.clustermarvel.utem/webParalela/"})

def crearPDF(arrPor, desc, cant, final, descr, nombre, matrix, penalty):

    #ancho = 612
    #alto = 792
    c=canvas.Canvas("/var/www/html/webParalela/FASTA/Envio/"+nombre+".pdf", pagesize = letter)
    #cabecera
    c.setFont("Helvetica-Oblique",10)
    c.drawImage("/var/www/html/webParalela/logo.png",10,700,width=90,height=90)
    c.drawString(110,765,"Universidad Tecnológica Metropolitana de Chile")
    c.drawString(110,753,"Ingenieria Civil en Computación Mención Informática")
    c.drawString(110,741,"Computación Paralela")
    c.drawString(110,729,"Plataforma Integrada")


    #Titulo
    c.setFont("Helvetica-Bold",30)
    c.drawString(140,629,"Resultado Fasta")
    c.line(50,620,562,620)
    #Subtitulo
    c.setFont("Helvetica-Oblique",20)
    c.drawString(150,600,"Alineamientos de secuencias de ADN.")


    #Cuerpo
    #input
    c.setFont("Helvetica",15)
    c.drawString(100,575,"Descripción de la cadena de entrada:")
    c.setFont("Helvetica",10)
    c.drawString(150,550,desc)
    c.setFont("Helvetica",15)
    c.drawString(100,525,"Con la matriz elegida:")
    c.setFont("Helvetica",10)
    c.drawString(150,500,matrix)
    c.setFont("Helvetica",15)
    c.drawString(100,475,"Y con la penalización de:")
    c.setFont("Helvetica",10)
    c.drawString(150,450,str(penalty))

    #Acá parte el for
    #output
    c.setFont("Helvetica",15)
    c.drawString(100,425,"El(Los) porcentaje(s) de similitud para la(s) "+str(cant)+" cadena(s) es(son) el(los)")
    c.drawString(100,411,"siguiente(s):")
    c.setFont("Helvetica",10)
    posicion = 405
    for i in range(0,cant):
        posicion = posicion - 15
        c.drawString(100,posicion,"Cadena "+str(i+1)+": "+str(arrPor[i])+"%, que corresponde a: "+str(descr[i]))
        if(arrPor[i]=="100.0"):
            posicion = posicion - 15
            c.drawString(100,posicion,"(Esta cadena es la misma que la de entrada)")

    c.setFont("Helvetica", 10)
    sTiempo = "Tiempo de ejecucion del algoritmo: " + str(final) + " Segundos"
    c.drawString(150,60,sTiempo)


    #Pie de pagina
    c.line(20,40,582,40)
    c.setFont("Helvetica-Bold",8)
    c.drawString(180,30,"Recuerda seguir utilizando nuestra pagina : 00-ironman.clustermaarvel.utem")
    now = "Documento creado en :" + time.strftime("%c")
    c.drawString(230,20,now)
    c.showPage()
    c.save()

def mismaSecuencia(sec_comp, matrix, penalizacion):
    matriz = tipoMatriz(matrix)
    gap_extend = -0.5
    indice_mayor=0 
    max_score=0

    p52_entrada = sec_comp
    p52_base = sec_comp

    alns = pairwise2.align.globalds(p52_entrada, p52_base, matriz, penalizacion, gap_extend)
    top_aln = alns[0]
    aln_entrada, aln_base, scoremax, begin, end = top_aln
    return scoremax

def tipoMatriz(matrix):
    if(matrix=="matlist.blosum62"):
        matrix = matlist.blosum62
        return matrix
    if(matrix=='matlist.benner6'):
        matrix = matlist.benner6
        return matrix
    if(matrix=='matlist.benner22'):
        matrix = matlist.benner22
        return matrix 
    if(matrix=='matlist.benner74'):
        matrix = matlist.benner74
        return matrix
    if(matrix=="matlist.blosum100"):
        matrix = matlist.blosum100
        return matrix
    if(matrix=="matlist.blosum30"):
        matrix = matlist.blosum30
        return matrix
    if(matrix=="matlist.blosum35"):
        matrix = matlist.blosum35
        return matrix
    if(matrix=="matlist.blosum40"):
        matrix = matlist.blosum40
        return matrix
    if(matrix=="matlist.blosum45"):
        matrix = matlist.blosum45
        return matrix
    if(matrix=="matlist.blosum50"):
        matrix = matlist.blosum50
        return matrix
    if(matrix=="matlist.blosum55"):
        matrix = matlist.blosum55
        return matrix
    if(matrix=="matlist.blosum60"):
        matrix = matlist.blosum60
        return matrix
    if(matrix=="matlist.blosum65"):
        matrix = matlist.blosum65
        return matrix
    if(matrix=="matlist.blosum70"):
        matrix = matlist.blosum70
        return matrix
    if(matrix=="matlist.blosum75"):
        matrix = matlist.blosum75
        return matrix
    if(matrix=="matlist.blosum80"):
        matrix = matlist.blosum80
        return matrix
    if(matrix=="matlist.blosum85"):
        matrix = matlist.blosum85
        return matrix
    if(matrix=="matlist.blosum90"):
        matrix = matlist.blosum90
        return matrix
    if(matrix=="matlist.blosum95"):
        matrix = matlist.blosum95
        return matrix
    if(matrix=="matlist.pam30"):
        matrix = matlist.pam30
        return matrix
    if(matrix=="matlist.pam60"):
        matrix = matlist.pam60
        return matrix
    if(matrix=="matlist.pam90"):
        matrix = matlist.pam90
        return matrix
    if(matrix=="matlist.pam120"):
        matrix = matlist.pam120
        return matrix
    if(matrix=="matlist.pam180"):
        matrix = matlist.pam180
        return matrix
    if(matrix=="matlist.pam250"):
        matrix = matlist.pam250
        return matrix
    if(matrix=="matlist.pam300"):
        matrix = matlist.pam300
        return matrix

def mejoresPorProcesador(cant, secInicial, descripciones, secuencias, arrayScore, matrix): # cant = la cantidad de secuencias $
    tam = len(arrayScore)
    array = list(range(tam))

    for i in range(1,tam):
        for j in range(0,tam-i):
            if(arrayScore[j] < arrayScore[j+1]):
                k = arrayScore[j+1]
                l = descripciones[j+1]
                m = secuencias[j+1]
                n = secInicial[j+1]
                arrayScore[j+1] = arrayScore[j]
                descripciones[j+1] = descripciones[j]
                secuencias[j+1] = secuencias[j]
                secInicial[j+1] = secInicial[j]
                arrayScore[j] = k
                descripciones[j] = l
                secuencias[j] = m
                secInicial[j] = n 
	retorno = dict(alineaciones = secuencias[0:cant+1], info = descripciones[0:cant+1], puntaje = arrayScore[0:cant+1], matriz = matrix, normal = secInicial[0:cant+1])
    return retorno

def generarAlineacion(inicio, fin, sec_comp, matrix, gap_open, resultados):
    # Almacenamos todas las secuencias contenidas en la base de datos
    i = 0
    bestScore = list(range(1000))
    bestAlign = list(range(1000))
    bestInfo = list(range(1000))
    bestNorm =list(range(1000))
    for seq_record in SeqIO.parse("/mpi/FASTA/base.fasta", "fasta"):
        subArreglo1[i] = seq_record.seq
        subArreglo2[i] = seq_record.id

        i = i + 1
    fin2 = time.time()
    gap_extend = -0.5
    indice_mayor = 0
    max_score = 0
    inicio3 = time.time()
    # Se tomas las i secuencias de ADN a comprar contenidas en la bdd
    for i in range(inicio, fin):
    	p53_entrada = sec_comp
    	p53_base = subArreglo1[i]

    	alns = pairwise2.align.globalds(p53_entrada, p53_base, matrix, gap_open, gap_extend)

    	top_aln = alns[0]
    	aln_entrada, aln_base, score, begin, end = top_aln
    	bestScore[i] = score
    	bestInfo[i] = subArreglo2[i]
    	bestAlign[i] = aln_base
        bestNorm[i] = aln_entrada
    lista = mejoresPorProcesador(resultados, bestNorm, bestInfo, bestAlign, bestScore, matrix)
    comm.send(lista, dest=0)

def Mejores(cant, secInicial, descripciones, secuencias, arrayScore, matriz, gap_open, scoremax, mail, sec_id, final, nombre, laMatriz):
    gap_extend = -0.5
    tam = len(arrayScore)
    array = list(range(tam))
    arrPorc = list(range(cant))
    dscr = list(range(cant))

    for i in range(1,tam):
        for j in range(0,tam-i):
            if(arrayScore[j] < arrayScore[j+1]):
                k = arrayScore[j+1]
                l = descripciones[j+1]
                m = secuencias[j+1]
                n = secInicial[j+1]
                arrayScore[j+1] = arrayScore[j]
                descripciones[j+1] = descripciones[j]
                secuencias[j+1] = secuencias[j]
                secInicial[j+1] = secInicial[j]
                arrayScore[j] = k
                descripciones[j] = l
                secuencias[j] = m
                secInicial[j] = n 
    """
    print '*****Secuencias mas similes*****\n'
    for z in range(0,cant):
        print 'Score [', z,']:', arrayScore[z]
        print descripciones[z]
        print secuencias[z]
    print 'las secuencias alineadas son: \n'
    for s in range(0,cant):
        secBase = secuencias[s]
        alns = pairwise2.align.globalds(secInicial, secBase, matrix, gap_open, gap_extend) #ALineamos la $
        top_aln = alns[0]
        aln_entrada, aln_basemay, score, begin, end = top_aln
        print '\n\n'
        print aln_entrada+'\n\n'+aln_basemay
    """
    fa = open("/var/www/html/webParalela/FASTA/Envio/"+nombre+".fasta", "w")
    fa.close()
    fa = open("/var/www/html/webParalela/FASTA/Envio/"+nombre+".fasta", "a")
    for s in range(0,cant):
        secBase = secuencias[s]
        secIni = secInicial[s]
        arrSco = arrayScore[s]
        descr = descripciones[s]
        """
        print secInicial
        print secBase[0]
        print matrix
        print gap_open
        print gap_extend
        
        alns = pairwise2.align.globalds(secInicial, secBase[0], matrix, gap_open, gap_extend) #ALineamos la secuencia de ADN a comprar con la que posee mayor score (mayor similitud)
        top_aln = alns[0]
        aln_entrada, aln_basemay, score, begin, end = top_aln
        """
        scoreFinal = arrayScore[s]
        simil = ((1 - ((scoremax - scoreFinal[0]) / scoremax)) * 100)
        fa.write("----- Datos secuencia "+str(s+1)+"  -----")
        fa.write("\n")
        fa.write(str(descr[0]))
        fa.write("\n")
        fa.write("\n\n")
        fa.write("--- Alineacion---")
        fa.write("\n")
        fa.write(str(secBase[0]))
        fa.write("\n\n")
        fa.write(str(secIni[0]))
        fa.write("\n\n")
        fa.write("Score:"+str(arrSco[0]))
        fa.write("\n")
        fa.write("Porcentaje de similitud: "+str(simil)+"%")
        fa.write("\n\n")
        fa.write("\n\n")
        arrPorc[s] = str(simil)
        dscr[s] = descr[0] 
        print arrPorc[s] 
    fa.close()
    crearPDF(arrPorc, sec_id, cant, final, dscr, nombre, laMatriz, gap_open)
    envio_mail(mail, nombre)




arrScore = list(range(1000))
arrDesc = list(range(1000))
arrAlin = list(range(1000))
arrOrig = list(range(1000))

def run():
    if (rank == 0):
        i = 0
        inicio1 = time.time()
        for seq_record in SeqIO.parse("/var/www/html/webParalela/FASTA/"+sys.argv[1], "fasta"):
            sec_comp = seq_record.seq
            sec_id = seq_record.id
        handle = open("/mpi/FASTA/base.fasta", "rU")
        records = list(SeqIO.parse(handle, "fasta"))
        handle.close()
        total = len(records)
        rango = int(total / (size - 1))
        resto = total - (rango * (size - 1))
        process = 0
        penalizacion = int(sys.argv[3])
        resultados = int(sys.argv[4])
        matrix = str(sys.argv[2])
        matriz = tipoMatriz(matrix)
        mail = str(sys.argv[5])
        nombre = str(sys.argv[6])
        for i in range(1, (size - 1)):
            inicio = rango * i
            fin = rango * (i + 1)
            process = process + 1
            rangos = [inicio, fin, sec_comp, matriz, penalizacion, resultados]
            comm.send(rangos, dest=process)
        inicio = fin
        fin = inicio + resto
        process = process + 1
        rangos = [inicio, fin, sec_comp, matriz, penalizacion, resultados]
        comm.send(rangos, dest=process)
    if (rank != 0):
        archivo = comm.recv(source=0)
        generarAlineacion(archivo[0], archivo[1], archivo[2], archivo[3], archivo[4], archivo[5])
    if (rank == 0):
        for i in range(1, (size - 1)):
            tiempo_final = time.time()
            candidato = comm.recv(source=i)
            arrScore[i] = candidato["puntaje"]
            arrDesc[i] = candidato["info"]
            arrAlin[i] = candidato["alineaciones"]
            arrOrig[i] = candidato["normal"]
        scoremax = mismaSecuencia(sec_comp, matrix, penalizacion)
        print "tiempo final final!: ", time.time() - inicio1
        final = time.time() - inicio1
        final = round(final, 3)
        Mejores(resultados, arrOrig, arrDesc, arrAlin, arrScore, matriz, penalizacion, scoremax, mail, sec_id, final, nombre, matrix)
	#comm.Disconnect()
run()
