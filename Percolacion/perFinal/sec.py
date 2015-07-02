#!/usr/bin/env python
# -*- coding: utf-8 -*-

from algorithm import WeightedQuickUnionUF
from random import Random
from time import time
import sys
from pdf import crearPDF
from mail import envio_mail

class PercolationSimulation(object):
    def __init__(self, N, rseed=None):
        self.N = N
        self.qu = WeightedQuickUnionUF(N * N + 2, debug=False) # La grilla es de N * N, pero se agregan dos componentes virtuales
        self.virt_top = N * N
        self.virt_bottom = N * N + 1

        # Usamos un hack: hay dos nodos virtuales en WQU, una para cada borde
        # Conectamos todos los nodos de cada borde a su nodo virtual, luego checkeamos si ambos nodos son conexos
        # Si esto es True, el sistema percola
        for i in range(N):
            self.qu.union(N * N, i) # El nodo N * N es virtual top
        for i in range(N * N - N, N * N):
            self.qu.union(N * N + 1, i) # El nodo N * N + 1 es virtual bottom

        self.open = [False] * (N * N) # Indica si el nodo esta abierto o no
        self.rng = Random(rseed) if rseed else Random()

    def adyacentes(self, p):
        # Retorna los id de los nodos abiertos adyacentes a p
        adyacentes = []
        izq = p - 1
        derecha = p + 1
        arriba = p - self.N
        abajo = p + self.N

        # Checkea a los vecinos del nodo, viendo si realmente son vecinos, y estan abiertos
        for nodo in (izq, derecha, arriba, abajo):
            if 0 < nodo < self.N * self.N and self.open[nodo]:
                adyacentes.append(nodo)
        return adyacentes

    def _percola(self): # Si ambos nodos virtuales son conexos, bingo!
        return self.qu.connected(self.virt_top, self.virt_bottom)

    def umbral(self):
        cerrados = range(self.N * self.N) # Todos los sitios parten cerrados
        self.rng.shuffle(cerrados) # Hacemos un shuffle, para ir abriendo sitios aleatoriamente

        while cerrados:
            nodo = cerrados.pop()
            self.open[nodo] = True # Se abre el nodo
            vecinos = self.adyacentes(nodo) # Se obtienen los nodos adyacentes

            for vecino in vecinos: # Se establece un enlace entre el nodo y cada nodo adyacente
                self.qu.union(nodo, vecino)

            if self._percola(): break # Si el sistema percola, terminamos
        abiertos = float(self.N ** 2 - len(cerrados))

        return abiertos / (self.N * self.N) # La estimación del umbral de percolación


if __name__ == '__main__':
    ST = time()
    arbol = int(sys.argv[1])
    comb = 0
    suelo = int(sys.argv[2])
    dist = int(sys.argv[3])
    N = int(sys.argv[4])
    mail = str(sys.argv[5])
    nombre = str(sys.argv[6])
    SAMPLE_SIZE = 385
    estimated_threshold = []
    mean = 0.0
    variance = 0.0
    if arbol == 1: #quillay
        comb = 39
    if arbol == 2: #peumo
        comb = 35
    if arbol == 3: #boldo
        comb = 32
    if arbol == 4: #roble
        comb = 10
    if arbol == 5: #rauli
        comb = 20
    if suelo == 1:
        comb = (comb + 97)/2
    if suelo == 2:
        comb = (comb + 80)/2
    if suelo == 3:
        comb = (comb + 53)/2
    if suelo == 4:
        comb = (comb + 78)/2
        pass
    for i in range(SAMPLE_SIZE):
        percolacion = PercolationSimulation(N)
        estimado = percolacion.umbral()
        mean += estimado
        estimated_threshold.append(estimado)
    mean /= SAMPLE_SIZE
    for x in estimated_threshold:
        variance += (x - mean) ** 2
    variance /= (SAMPLE_SIZE - 1)
    mean = (mean * comb)/100
    mean = 1 - mean
    nompdf = nombre + ".pdf"
    T = (time()-ST)
    crearPDF(arbol,suelo,dist,N,mean,T,nompdf)
    envio_mail(mail,nompdf)   