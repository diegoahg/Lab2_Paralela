
'''
 Retorna un array con el inicio y final de cada intervalo.
 lista -> [inicio, final]

 Ej:
        Salto = 100
        procesadores = 5

        Output
        [1, 20, 21, 40, 41, 60, 61, 80, 81, 100]

        Retorna 5 intervalos con su inicio y fin concatenados.
'''


def saltoProc(Max, p):
    count = 0
    lista = [1]
    rango = int(Max / p)

    for i in range(p - 1):
        lista.append(count + rango)
        lista.append(count + rango + 1)
        count += rango
    lista.append(Max)

    return lista
