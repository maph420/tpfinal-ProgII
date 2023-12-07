from sys import argv
from random import choice
import time

def abrir_archivo(nomArch, modoLectura):
    try:
        arch = open(nomArch, modoLectura)
    except:
        print("No se pudo abrir el archivo",nomArch,". Saliendo...")
        #?
        exit(-1)
    return arch

# dictFrecuencias: {str: (dictI, dictD)}
# dictI: {str: int}
# dictD: {str: int}

# Diccionario en el cual las claves son palabras, y el valor asociado a cada una de las claves son
# tuplas de la forma (dict, dict) donde el diccionario en la primer componente corresponde a un diccionario
# donde las claves son palabras a la izquierda de la palabra original y sus valores asociados son numeros enteros 
# correspondientes a la cantidad de veces que las palabras aparecen juntas (en ese orden) en el texto
# el diccionario de la segunda componente se comporta de manera analoga pero con almacenando las palabras a la derecha
# de la palabra original

# ejemplos:

def armar_dict_frecuencias(listaPals, ocurrencias):
    for i, pal in enumerate(listaPals):
        palIzq = listaPals[i-1] if i > 0 else ""
        palDer = listaPals[i+1] if i < len(listaPals)-1 else ""
       
        if pal not in ocurrencias:
            ocurrencias[pal] = ({}, {})

        if palIzq != "":
            # se agrega la palabra al diccionario de las palabras a la izquierda
            if palIzq not in ocurrencias[pal][0]:
                ocurrencias[pal][0][palIzq] = 1
            else:
                ocurrencias[pal][0][palIzq] += 1
        if palDer != "":
            # se agrega la palabra al diccionario de las palabras a la derecha
            if palDer not in ocurrencias[pal][1]:
                ocurrencias[pal][1][palDer] = 1
            else:
                ocurrencias[pal][1][palDer] += 1
    return ocurrencias
 
# dictsBigramas: (bigramasI, bigramasD)
# bigramasI: {(palIzq2, palIzq1): set(pal)}
# palIzq2, palIzq1, pal: str
# bigramasD: {(palDer1, palDer2): set(pal)}
# palDer1, palDer2, pal: str

# dictsBigramas es una tupla que contiene a los diccionarios bigramasI y bigramasD.
# El diccionario bigramasI se trata de un diccionario cuya claves son tuplas de la forma
# (palIzq2, palIzq1) donde palIzq2 es la string que se encuentra 2 palabras a la izquierda
# de pal y palIzq1 la string que se encuentra exactamente a la izquierda de pal, siendo pal
# un elemento del conjunto de valores asociados a cada clave.

# la palabra usada como clave termina resultando la palabra "entre medio", donde el primer elemento son diccionarios
# con las palabras a su izquierda junto con la cantidad de veces que aparecen juntas y el segundo elemento son
# diccionarios con las palabras a su derecha junto con la cantidad de veces que aparecen juntas

# en la parte de tests se pueden ver ejemplos del funcionamiento

def armar_dicts_bigramas(listaPals, bigramasI, bigramasD):
    i=0
    while i < len(listaPals):
        if (i > 1):
            grupoIzq = (listaPals[i-1],listaPals[i])    
            if grupoIzq not in bigramasI:
                bigramasI[grupoIzq] = set()
            bigramasI[grupoIzq].add(listaPals[i-2])
        if (i < len(listaPals)-2):
            grupoDer = (listaPals[i], listaPals[i+1])
            if grupoDer not in bigramasD:
                bigramasD[grupoDer] = set()
            bigramasD[grupoDer].add(listaPals[i+2])
        i+=1
    return (bigramasI, bigramasD)

def frecuencia_grupos(rutaEntrada):
    archivoEntradas = abrir_archivo(rutaEntrada, 'r')
    frecuenciaGrupos, bigramasI, bigramasD = {}, {}, {}
    for linea in archivoEntradas:
        dictFrecuencias = armar_dict_frecuencias(linea.split(), frecuenciaGrupos)
        dictsBigramas = armar_dicts_bigramas(linea.split(), bigramasI, bigramasD)
    archivoEntradas.close()
    return (dictFrecuencias, dictsBigramas)

def may_frecuencia(dictFrecuencias, palAnterior, palPosterior):
    esUltimaPal = (palPosterior == "")
    candidato, mayFrec = "", 0
    candidatoAux, frecAux = "", 0
    
    if palAnterior in dictFrecuencias.keys():
        for pal, cantAps in dictFrecuencias[palAnterior][1].items():
            if cantAps > mayFrec and pal != palPosterior and pal != palAnterior:
                # para evitar que una oracion termine con un -potencial- articulo (palabra de longitud 3 o menor)
                longitudValida = (len(pal) > 3)
                if (not esUltimaPal) or (esUltimaPal and longitudValida):
                    mayFrec = cantAps
                    candidato = pal
                # aunque la condicion de arriba no cumpla, guardamos la palabra, en caso de no encontrar otra mejor
                else:
                    candidatoAux = pal
                    frecAux = cantAps

    if palPosterior in dictFrecuencias.keys():
        for pal, cantAps in dictFrecuencias[palPosterior][0].items():
            if cantAps > mayFrec and pal != palAnterior and pal != palPosterior: 
                # para evitar que una oracion termine con un -potencial- articulo (palabra de longitud 3 o menor)
                longitudValida = (len(pal) > 3)
                if (not esUltimaPal) or (esUltimaPal and longitudValida):
                    mayFrec = cantAps
                    candidato = pal
                else:
                    candidatoAux = pal
                    frecAux = cantAps

    if (candidato == ""):
        candidato = candidatoAux
        mayFrec = frecAux
    return candidato

def pos_pal_faltante(listaPals):
    i, encontrado, pospal = 0, 0, 0
    while (i < len(listaPals) and (not encontrado)):
        if (listaPals[i] == '_'):
            encontrado = 1
            pospal = i
        else:
            i += 1
    return pospal

def completar_frase(lineaFrase, palabraCandidata, archivo):
    for palabra in lineaFrase:
        if palabra == "_":
            archivo.write(palabraCandidata.upper())
        else:
            archivo.write(palabra)

def obtener_candidatos(datoFrecuencias, bigramaIzq, bigramaDer, rutaArtista, rutaFrases):
    archivoSalida = abrir_archivo(rutaArtista, 'w')
    archivoFrases = abrir_archivo(rutaFrases, 'r')
    
    for lineaFrase in archivoFrases:
        listaPalabras = lineaFrase.split()
        posPalabraFaltante = pos_pal_faltante(listaPalabras)
        palabrasAnteriores, palabrasPosteriores = ("",""), ("","")
        candidato = ""
        
        if (posPalabraFaltante > 1):
            palabrasAnteriores = (listaPalabras[posPalabraFaltante-2], listaPalabras[posPalabraFaltante-1])
        elif (posPalabraFaltante > 0):
            palabrasAnteriores = ("", listaPalabras[posPalabraFaltante-1])
            
        if (posPalabraFaltante < (len(listaPalabras)-2)):
            palabrasPosteriores = (listaPalabras[posPalabraFaltante+1], listaPalabras[posPalabraFaltante+2])
        elif (posPalabraFaltante < (len(listaPalabras)-1)):
            palabrasPosteriores = (listaPalabras[posPalabraFaltante+1],"")
        
        candidatoBigramaI = bigramaIzq[palabrasAnteriores] if palabrasAnteriores in bigramaIzq else set()
        candidatoBigramaD = bigramaDer[palabrasPosteriores] if palabrasPosteriores in bigramaDer else set()
        
        if candidatoBigramaI != set():
            candidato = candidatoBigramaI.pop()
        elif candidatoBigramaD != set():
            candidato = candidatoBigramaD.pop()
        # en caso de no encontrar una coincidencia exacta a traves de bigramas, tratar de hallar
        # una palabra adecuada basandose en la frecuencia de apariciones
        else:
            candidato = may_frecuencia(datoFrecuencias, palabrasAnteriores[1], palabrasPosteriores[0])
        
           
        # como ultimo recurso, escoger el candidato de manera aleatoria entre las palabras del 
        # texto de entrada. Se prefiere que no sea un articulo.
        if candidato == "":
            while (len(candidato) < 3):
                candidato = choice(list(datoFrecuencias.keys()))
       
        completar_frase(lineaFrase, candidato, archivoSalida)
        
    archivoFrases.close()
    archivoSalida.close()

def main():
    rutaEntrada = "Entradas/" + argv[1] + ".txt"
    rutaSalida = "Salidas/" + argv[1] + ".txt"
    rutaFrases = "Frases/" + argv[1] + ".txt"
    
    if (len(argv) != 2):
        print("Cantidad incorrecta de argumentos. Saliendo...")
        exit(-1)    

    start = time.time()
    infoTexto = frecuencia_grupos(rutaEntrada)
    
    dictFrecuencias = infoTexto[0]
    dictsBigrama = infoTexto[1]
    bigramaDer = dictsBigrama[0]
    bigramaIzq = dictsBigrama[1]
    
    obtener_candidatos(dictFrecuencias, bigramaIzq, bigramaDer, rutaSalida, rutaFrases)
    print(f"It took {time.time() - start}s")    

if __name__ == "__main__":
    main()