'''
Author:    ____Arratia Rodrigo A.____
Date:           ___May-2015___
'''

import time
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist
from Bio import SeqIO

det = True #variable que indica si existe una coinsidencia en la base de datos
arreglo1 = list(range(300)) #Se define el arreglo que poseera la informacion de la secuancia de ADN a comparar
arreglo2 = list(range(300)) #Se define el arreglo correspondiente a la nesima secuencia contenida en la base de datos
i = 0

inicio1 = time.time()
for seq_record in SeqIO.parse("holaProte.fasta", "fasta"): # Recorre el archivo fasta, secuencia por secuencia
    sec_comp=seq_record.seq  #Guardamos en una variable la secuencia a comprar
    sec_comp2=seq_record.id







#************************calculo del score maximo para dicha secuencia *************************
matrix = matlist.blosum62
gap_open = -10
gap_extend = -0.5
indice_mayor=0 
max_score=0

p52_entrada = sec_comp
p52_base = sec_comp

alns = pairwise2.align.globalds(p52_entrada, p52_base, matrix, gap_open, gap_extend)
top_aln = alns[0]
aln_entrada, aln_base, scoremax, begin, end = top_aln
print 'La alineacion entre la misma secuencia es la siguiente: \n', aln_entrada+'\n\n'+aln_base
print ' El maximo score posible es: ', scoremax

#***************************aqui termina la comparacion entre la misma secuencia de entrada***************************







fin1 = time.time()
print 'secuencia a comparar: \n', sec_comp   #Imprimimos la secuencia a comparar
inicio2 = time.time()
for seq_record in SeqIO.parse("baseProte.fasta", "fasta"):#Almacenamos todas las secuencias contenidas en la base de datos
                                                     # en "arreglo" y sus correspondientes informaciones en "arreglo2"
    #print(seq_record.id)
    #print 'secuencia', i,':'
    #print(seq_record.seq)
    arreglo1[i]=seq_record.seq
    arreglo2[i]=seq_record.id
    
    i=i+1
fin2 = time.time()
print 'El numero de secuencias en la Base de Datos son:', i #Numero de secuencias de ADN contenidas en la bdd
arrayScore = list(range(i))# se define el arreglo que contendra todos los scores

inicio3 = time.time()
for i in range (0, 250):  #Se tomas las i secuencias de ADN a comprar contenidas en la bdd
    p53_entrada = sec_comp
    p53_base = arreglo1[i]

    alns = pairwise2.align.globalds(p53_entrada, p53_base, matrix, gap_open, gap_extend)

    top_aln = alns[0]
    aln_entrada, aln_base, score, begin, end = top_aln
    #print aln_entrada+'\n\n'+aln_base
    arrayScore[i] = score
    print "Score", i+1,':', score #Rescatamos el indicede la casilla cuyo contenido represente a la secuencia con mayor score
    if max_score <= score:
        indice_segundo = indice_mayor #Almacena en indice anterior antes de ser reemplazado
        max_score = score
        indice_mayor = i 
        if score == scoremax:
            det = False

print 'mejor score', indice_mayor+1, '\n'
print 'segundo mejor score', indice_segundo+1, '\n'
fin3 = time.time()

if det == False:
    inicio4 = time.time()
    print 'Se ha encontrado una coincidencia exacta entre la secuencia ingresada en la base de datos... \n'
    p51_basesegunda = arreglo1[indice_segundo] 
    alns = pairwise2.align.globalds(p53_entrada, p51_basesegunda, matrix, gap_open, gap_extend) #ALineamos la secuencia de ADN a comprar con la que posee mayor score (mayor similitud)
    top_aln = alns[0]
    aln_entrada, aln_basesegunda, score, begin, end = top_aln
    fin4 = time.time()
 #   print 'La segunda secuencia alineada con mejor score con es: \n', aln_entrada+'\n\n'+aln_basesegunda 
    secuencia1 = aln_entrada
    secuencia2 = aln_basesegunda

if det == True:
    
    print '\n'
    print 'La secuencia con mayor score es la numero: ', indice_mayor+1, 'cuya informacion informacion  es:'
    print '\n'
    print arreglo2[indice_mayor] #Imprimimos la alineacion
    print arreglo1[indice_mayor]   



    print '\n'     
    inicio4 = time.time()
    p53_basemay = arreglo1[indice_mayor]
    alns = pairwise2.align.globalds(p53_entrada, p53_basemay, matrix, gap_open, gap_extend) #ALineamos la secuencia de ADN a comprar con la que posee mayor score (mayor similitud)
    top_aln = alns[0]
    aln_entrada, aln_basemay, score, begin, end = top_aln
    fin4 = time.time()
  #  print 'La secuencia alineada es: \n', aln_entrada+'\n\n'+aln_basemay
    secuencia1 = aln_entrada
    secuencia2 = aln_basemay

print '\n' 
print 'tiempo en leer la secuencia a comparar y guardarla en una variable: ', (fin1-inicio1), 'segundos'
print 'Tiempo en almacenar las secuencias de ADN en los arrays:               ', (fin2-inicio2), 'segundos'
print 'Tiempo en calcular el score de cada secuencia de ADN en la bdd:        ', (fin3-inicio3), 'segundos'
print 'Tempo en calcular el alineamiento e imprimirlo por pantalla :          ', (fin4-inicio4), 'segundos'

tpo = ((fin1-inicio1)+(fin2-inicio2)+(fin3-inicio3)+(fin4-inicio4))
print 'Tiempo total de ejecucion:                                             ',tpo, 'segundos'
print '\n\n\n'


"""
print secuencia1, '\n'
print secuencia2

#***********************Funcion fichero***********************

'''
    for i in range(0, len(string1)):
        f.write(string1[i])
'''
def efichero (sec1, sec2):
    f = open("ficheroFasta.txt","w")
    f.close()
    f = open("ficheroFasta.txt", "a")
    f.write(str(sec1))
    f.write("\n")
    f.write(str(sec2))
    f.close()

def Mejores(cant, secInicial, descripciones, secuencias, arrayScore, scoremax): # cant = la cantidad de secuencias que desea el cliente///// scoremax = calculo de score entre la misma secuencia de entrada
    matrix = matlist.benner6
    gap_open = -10
    gap_extend = -0.5
    tam = len(arrayScore)
    array = list(range(tam))
        
    for i in range(1,tam):
        for j in range(0,tam-i):
            if(arrayScore[j] < arrayScore[j+1]):
                k = arrayScore[j+1]
                l = descripciones[j+1]
                m = secuencias[j+1]
                arrayScore[j+1] = arrayScore[j]
                descripciones[j+1] = descripciones[j]
                secuencias[j+1] = secuencias[j]
                arrayScore[j] = k
                descripciones[j] = l
                secuencias[j] = m
    print '*****Secuencias mas similes*****\n'
    for z in range(0,cant):
        print 'Score [', z,']:', arrayScore[z]
        print descripciones[z]
        print secuencias[z]
    print 'las secuencias alineadas son: \n'
    
    for s in range(0,cant):
        secBase = secuencias[s]
        alns = pairwise2.align.globalds(secInicial, secBase, matrix, gap_open, gap_extend) #ALineamos la secuencia de ADN a comprar con la que posee mayor score (mayor similitud)
        top_aln = alns[0]
        aln_entrada, aln_basemay, score, begin, end = top_aln
        simil = ((1 - ((scoremax - arrayScore[s]) / scoremax)) * 100)
        print '\n\n'
        print aln_entrada+'\n\n'+aln_basemay
        fa = open("secuencia"+str(s+1)+".fasta", "w")
        fa.close()
        fa = open("secuencia"+str(s+1)+".fasta", "a")
        fa.write("----- Datos secuencia "+str(s+1)+"  -----")
        fa.write("\n")
        fa.write(str(descripciones[s]))
        fa.write("\n")
        fa.write(str(secuencias[s]))
        fa.write("\n\n")
        fa.write("--- Alineacion---")
        fa.write("\n")
        fa.write(str(aln_entrada))
        fa.write("\n")
        fa.write(str(aln_basemay))
        fa.write("\n\n")
        fa.write("Score:"+str(arrayScore[s]))
        fa.write("\n")
        fa.write("Porcentaje de similitud: "+str(simil)+"%")
        fa.close()
        
        
Mejores(3,sec_comp,arreglo2,arreglo1,arrayScore,scoremax)
"""
