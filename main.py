from sys import argv
from random import choice

# abrir_archivo: str, str -> file
# Simplemente realiza operaciones con archivos, pero con chequeo de errores.

def abrir_archivo(nomArch, modoLectura):
    try:
        arch = open(nomArch, modoLectura)
    except:
        print("No se pudo abrir el archivo",nomArch,". Saliendo...")
        exit(-1)
    return arch

# dictFrecuencias: {str: (dictI, dictD)}
# dictI: {str: int}
# dictD: {str: int}

# armar_dict_frecuencias: list(str), { str: ({str: int}, {str: int}) } -> { str: ({str: int}, {str: int}) }
# Construye el diccionario de frecuencias, dado la lista de palabras del texto a analizar.

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

# armar_dicts_bigramas: list(str), {(palIzq2, palIzq1): set(pal)}, {(palDer1, palDer2): set(pal)} -> ( {(palIzq2, palIzq1): set(pal)}, {(palDer1, palDer2): set(pal)} )
# Arma los diccionarios de bigramas. Retorna una tupla con el diccionario de bigramas por izquierda y el diccionario
# con bigramas por derecha, en ese orden.

def armar_dicts_bigramas(listaPals, bigramasI, bigramasD):
    i=0
    while i < len(listaPals):
        if (i < len(listaPals)-2):
            # par de palabras a la izquierda de la palabra
            gruposIzq = (listaPals[i], listaPals[i+1])
            if gruposIzq not in bigramasI:
                bigramasI[gruposIzq] = set()
            bigramasI[gruposIzq].add(listaPals[i+2])
        if (i > 1):
            # par de palabras a la derecha de la palabra
            grupoDer = (listaPals[i-1],listaPals[i])    
            if grupoDer not in bigramasD:
                bigramasD[grupoDer] = set()
            bigramasD[grupoDer].add(listaPals[i-2])
        i+=1
    return (bigramasI, bigramasD)

# frecuencia_grupos: str -> ( { str: ({str: int}, {str: int}) }, ( {(palIzq2, palIzq1): set(pal)}, {(palDer1, palDer2): set(pal)} ) )
# Se encarga de leer el archivo de entrada y crea las dos estructuras que almacenan la informacion, en forma de tupla.

def frecuencia_grupos(rutaEntrada):
    archivoEntradas = abrir_archivo(rutaEntrada, 'r')
    frecuenciaGrupos, bigramasI, bigramasD = {}, {}, {}
    for linea in archivoEntradas:
        dictFrecuencias = armar_dict_frecuencias(linea.split(), frecuenciaGrupos)
        dictsBigramas = armar_dicts_bigramas(linea.split(), bigramasI, bigramasD)
    archivoEntradas.close()
    return (dictFrecuencias, dictsBigramas)

# may_frecuencia: { str: ({str: int}, {str: int}) }, str, str -> str
# Dado el diccionario de frecuencias, la palabra anterior y posterior a la palabra buscada,
# retorna la palabra mas adecuada para completar la palabra buscada. Primero se basa en las frecuencias por izquierda.
# Si no encuentra una palabra acorde con frecuencia mayor a 1, se fija por derecha.

def may_frecuencia(dictFrecuencias, palAnterior, palPosterior):
    esUltimaPal = (palPosterior == "")
    candidato, mayFrec = "", 0
    
    if palAnterior in dictFrecuencias.keys():
        for pal, cantAps in dictFrecuencias[palAnterior][1].items():
            if cantAps > mayFrec and pal != palPosterior and pal != palAnterior:
                # para evitar que una oracion termine con un -potencial- articulo (palabra de longitud 3 o menor)
                longitudValida = (len(pal) > 3)
                if (not esUltimaPal) or (esUltimaPal and longitudValida):
                    mayFrec = cantAps
                    candidato = pal
    if mayFrec > 1:
        return candidato
    if palPosterior in dictFrecuencias.keys():
        for pal, cantAps in dictFrecuencias[palPosterior][0].items():
            if cantAps > mayFrec and pal != palAnterior and pal != palPosterior: 
                longitudValida = (len(pal) > 3)
                if (not esUltimaPal) or (esUltimaPal and longitudValida):
                    mayFrec = cantAps
                    candidato = pal
    return candidato

# pos_pal_faltante: list(str) -> int
# Dada una lista de palabras, retorna el indice en el cual aparece
# el caracter '_' en la cadena.

def pos_pal_faltante(listaPals):
    i, encontrado, pospal = 0, 0, 0
    while (i < len(listaPals) and (not encontrado)):
        if (listaPals[i] == '_'):
            encontrado = 1
            pospal = i
        else:
            i += 1
    return pospal

# completar_frase: str, str, file -> None
# Escribe en el archivo los contenidos de lineaFrase, intercambiando los caracteres '_'
# por palabraCandidata. Se asume que solo hay un '_' por lineaFrase.

def completar_frase(lineaFrase, palabraCandidata, archivo):
    for palabra in lineaFrase:
        if palabra == "_":
            archivo.write(palabraCandidata)
        else:
            archivo.write(palabra)

# obtener_pal_anteriores: list(str), int -> ( str, str )
# Retorna las dos palabras anteriores a la palabra cuyo indice se especifica como argumento.

def obtener_pal_anteriores(listaPalabras, posPal):
    palabrasAnteriores = ("","")
    if (posPal > 1):
        palabrasAnteriores = (listaPalabras[posPal-2], listaPalabras[posPal-1])
    elif (posPal > 0):
        palabrasAnteriores = ("", listaPalabras[posPal-1])
    return palabrasAnteriores

# obtener_pal_posteriores: list(str), int -> ( str, str )
# Analogo a la funcion anterior.

def obtener_pal_posteriores(listaPalabras, posPal):
    palabrasPosteriores = ("","")
    if (posPal < (len(listaPalabras)-2)):
        palabrasPosteriores = (listaPalabras[posPal+1], listaPalabras[posPal+2])
    elif (posPal < (len(listaPalabras)-1)):
        palabrasPosteriores = (listaPalabras[posPal+1],"")
    return palabrasPosteriores
    
# buscar_y_completar: { str: ({str: int}, {str: int}) }, {(palIzq2, palIzq1): set(pal)}, {(palDer1, palDer2): set(pal)}, str, str -> None
# Dadas las estructuras de informacion del texto y las rutas a escribir, busca un candidato para completar
# la frase y la completa.

def buscar_y_completar(datoFrecuencias, bigramaIzq, bigramaDer, rutaArtista, rutaFrases):
    archivoSalida = abrir_archivo(rutaArtista, 'w')
    archivoFrases = abrir_archivo(rutaFrases, 'r')
    
    for lineaFrase in archivoFrases:
        listaPalabras = lineaFrase.split()
        posPalabraFaltante = pos_pal_faltante(listaPalabras)
        candidato = ""
        
        palabrasAnteriores = obtener_pal_anteriores(listaPalabras, posPalabraFaltante)
        palabrasPosteriores = obtener_pal_posteriores(listaPalabras, posPalabraFaltante)

        # buscar coincidencia por palabras a la izquierda
        if palabrasAnteriores in bigramaIzq and bigramaIzq[palabrasAnteriores] != set():
            
            candidato = bigramaIzq[palabrasAnteriores].pop()
    
        # buscar coincidencia por palabras a la derecha
        elif palabrasPosteriores in bigramaDer and bigramaDer[palabrasPosteriores] != set():
            candidato = bigramaDer[palabrasPosteriores].pop()

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
    
    infoTexto = frecuencia_grupos(rutaEntrada)
    
    dictFrecuencias = infoTexto[0]
    dictsBigrama = infoTexto[1]
    bigramaIzq = dictsBigrama[0]
    bigramaDer = dictsBigrama[1]
   
    buscar_y_completar(dictFrecuencias, bigramaIzq, bigramaDer, rutaSalida, rutaFrases) 
    print(f"----------\nSalida generada en: {rutaSalida}\n----------")

if __name__ == "__main__":
    main()