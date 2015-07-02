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
        # La grilla es de N * N, pero se agregan dos componentes virtuales
        self.qu = WeightedQuickUnionUF(N * N + 2, debug=False)
        self.virt_top = N * N
        self.virt_bottom = N * N + 1

        # Usamos un hack: hay dos nodos virtuales en WQU, una para cada borde
        # Conectamos todos los nodos de cada borde a su nodo virtual, luego checkeamos si ambos nodos son conexos
        # Si esto es True, el sistema percola
        for i in range(N):
            self.qu.union(N * N, i)  # El nodo N * N es virtual top
        for i in range(N * N - N, N * N):
            self.qu.union(N * N + 1, i)  # El nodo N * N + 1 es virtual bottom

        self.open = [False] * (N * N)  # Indica si el nodo esta abierto o no
        self.rng = Random(rseed) if rseed else Random()

    def adyacentes(self, p):
        # Retorna los id de los nodos abiertos adyacentes a p
        adyacentes = []
        izq = p - 1
        derecha = p + 1
        arriba = p - self.N
        abajo = p + self.N

        # Checkea a los vecinos del nodo, viendo si realmente son vecinos, y
        # estan abiertos
        for nodo in (izq, derecha, arriba, abajo):
            if 0 < nodo < self.N * self.N and self.open[nodo]:
                adyacentes.append(nodo)
        return adyacentes

    def _percola(self):  # Si ambos nodos virtuales son conexos, bingo!
        return self.qu.connected(self.virt_top, self.virt_bottom)

    def umbral(self):
        cerrados = range(self.N * self.N)  # Todos los sitios parten cerrados
        # Hacemos un shuffle, para ir abriendo sitios aleatoriamente
        self.rng.shuffle(cerrados)

        while cerrados:
            nodo = cerrados.pop()
            self.open[nodo] = True  # Se abre el nodo
            vecinos = self.adyacentes(nodo)  # Se obtienen los nodos adyacentes

            # Se establece un enlace entre el nodo y cada nodo adyacente
            for vecino in vecinos:
                self.qu.union(nodo, vecino)

            if self._percola():
                break  # Si el sistema percola, terminamos
        abiertos = float(self.N ** 2 - len(cerrados))

        # La estimación del umbral de percolación
        return abiertos / (self.N * self.N)


if __name__ == '__main__':
    ST = time()
    enfe = int(sys.argv[1])
    cont = 0
    dist = int(sys.argv[2])
    N = int(sys.argv[3])
    mail = str(sys.argv[4])
    nombre = str(sys.argv[5])
    SAMPLE_SIZE = 385
    estimated_threshold = []
    mean = 0.0
    variance = 0.0
    if enfe == 1:  # quillay
        cont = 39
    if enfe == 2:  # peumo
        cont = 35
    if enfe == 3:  # boldo
        cont = 32
    if enfe == 4:  # roble
        cont = 10
    if enfe == 5:  # rauli
        cont = 20
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
    mean = (mean * cont) / 100
    mean = 1 - mean
    T = (time() - ST)
    crearPDF(enfe, dist, N, mean, T, nombre)
    envio_mail(mail, nombre)
