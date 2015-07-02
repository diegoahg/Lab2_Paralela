
from numpy import *
import re
import sys
import warnings
warnings.filterwarnings('ignore')

# Busca patrones en cada pagina que se le ingresa


def buscaPatron(txt, keyword, jumpMax):

        # El texto es transformado en array y se utilizan expresiones regulares
        # para establecer un patron.
    texto = array(list(txt))
    patron = re.compile(keyword)
    coincidencia = []
    toolbar_width = 50
    aux = len(texto) / toolbar_width
    cont = aux
    # setup toolbar
    print("\nBuscando : ", keyword)
    print("----------------------------------------------------------")
    sys.stdout.write("0 [%s] 100" % (" " * (toolbar_width)))
    sys.stdout.flush()
    # return to start of line, after '['
    sys.stdout.write("\b" * (toolbar_width + 1 + 4))

    for pagina, contenido in enumerate(texto):
        # print("****************Pagina ", pagina)

        if(pagina+1 >= cont):
            sys.stdout.write("#")
            sys.stdout.flush()
            cont += aux

        contenido = array(list(contenido))
        for jump in range(jumpMax):
            for i in range(jump + 1):
                # Se selecciona el texto con los saltos aplicados
                ContenidoConSalto = contenido[
                    arange(i, len(contenido), jump + 1)]
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
                        coincidencia.append(
                            {'keyword': keyword, 'pagina': pagina + 1, 'salto': jump + 1,
                             'inicio': (jump + 1) * (j.start(0)) + i + 1, 'fin': (jump + 1) * (j.end(0)) - 1})
    
    if(toolbar_width>len(texto)):
    	for i in range(toolbar_width-len(texto)):
    		sys.stdout.write("#")
    		sys.stdout.flush()
    sys.stdout.write("\n")
    return coincidencia
