
from mpi4py import MPI
from numpy import *
import sys
import os
import time
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist
from Bio import SeqIO

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

def tipoMatriz(matrix):
    if(matrix=="matlist.blosum62"):
        matrix = matlist.blosum62
        return matrix
    if(matrix=='matlist.benner6'):
        matrix = matlist.benner6
        return matrix

def generarAlineacion(inicio, fin, sec_comp, matrix):
    # Almacenamos todas las secuencias contenidas en la base de datos
    i = 0
    for seq_record in SeqIO.parse("baseProte.fasta", "fasta"):
        # en "arreglo" y sus correspondientes informaciones $
        # print(seq_record.id)
        subArreglo1[i] = seq_record.seq
        subArreglo2[i] = seq_record.id

        i = i + 1
    fin2 = time.time()
    matriz = tipoMatriz(matrix)
    gap_open = -10
    gap_extend = -0.5
    indice_mayor = 0
    max_score = 0
    inicio3 = time.time()
    # Se tomas las i secuencias de ADN a comprar contenidas en la bdd
    for i in range(inicio, fin):
        p53_entrada = sec_comp
        p53_base = subArreglo1[i]

        alns = pairwise2.align.globalds(p53_entrada, p53_base, matriz, gap_open, gap_extend)

        top_aln = alns[0]
        aln_entrada, aln_base, score, begin, end = top_aln
        if max_score <= score:
            max_score = score
            indice_mayor = i
    lista = dict(alineacion=subArreglo1[indice_mayor], info=subArreglo2[indice_mayor], puntaje=max_score)
    comm.send(lista, dest=0)

arrScore = []
arrDesc = []
arrAlin = []


def run():
    if (rank == 0):
        i = 0
        inicio1 = time.time()
        for seq_record in SeqIO.parse(sys.argv[1] + ".fasta", "fasta"):
            sec_comp = seq_record.seq
        handle = open("baseProte.fasta", "rU")
        records = list(SeqIO.parse(handle, "fasta"))
        handle.close()
        total = len(records)
        rango = int(total / (size - 1))
        resto = total - (rango * (size - 1))
        process = 0
        matrix = str(sys.argv[2])
        for i in range(1, (size - 1)):
            inicio = rango * i
            fin = rango * (i + 1)
            process = process + 1
            rangos = [inicio, fin, sec_comp, matrix]
            comm.send(rangos, dest=process)
            """
            output_handle = open(str(process) + ".fasta", "w")
            for x in range(inicio, fin):
                SeqIO.write(records[x], output_handle, "fasta")
            output_handle.close()
            """
        inicio = fin
        fin = inicio + resto
        process = process + 1
        rangos = [inicio, fin, sec_comp, matrix]
        comm.send(rangos, dest=process)
        """
        for i in range(1, size):
            comm.send(i, dest=i)

        """
    if (rank != 0):
        archivo = comm.recv(source=0)
        print "Recibido", name
        generarAlineacion(archivo[0], archivo[1], archivo[2], archivo[3])

    if (rank == 0):
        for i in range(1, (size - 1)):
            tiempo_final = time.time()
            candidato = comm.recv(source=i)
            print candidato
            print tiempo_final, "en: ", i
        print "tiempo final final!: ", time.time() - inicio1
run()
