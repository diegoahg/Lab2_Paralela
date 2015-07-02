
from numpy import *
import re


def buscaPatron(txt, keyword, jumpMin, jumpMax):

        # El texto es transformado en array y se utilizan expresiones regulares
        # para establecer un patron.
    texto = array(list(txt))
    patron = re.compile(keyword)
    coincidencia = []

    for pagina, contenido in enumerate(texto):
        # print("****************Pagina ", pagina)
        contenido = array(list(contenido))
        for jump in range(jumpMin, jumpMax+1):
            for i in range(jump + 1):
                # Se selecciona el texto con los saltos aplicados
                ContenidoConSalto = contenido[
                    arange(i, len(contenido), jump)]
                ContenidoConSalto = "".join(ContenidoConSalto.tolist())

                # Devuelve un objeto iterador con los datos de la coincidencia
                # del patron.
                iterator = re.finditer(patron, ContenidoConSalto)
                for j in iterator:
                    # Si el iterador no esta vacio se guarda la coincidencia
                    if(j != None):
                        # print(ContenidoConSalto)
                        # print("yes")
                        # Se guardan los datos de la coincidencia en un
                        # diccionario para exportarlo.
                        # print(keyword)
                        coincidencia.append(
                            {'keyword': keyword, 'pagina': pagina + 1, 'salto': jump,
                             'inicio': (jump) * (j.start(0)) + i + 1, 'fin': (jump) * (j.end(0)) - 1})

    return coincidencia
