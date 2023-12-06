from sys import argv
from random import choice

def armar_dict_frecuencias(listaPals, ocurrencias):
    for i, pal in enumerate(listaPals):
        palIzq = listaPals[i-1] if i > 0 else ""
        palDer = listaPals[i+1] if i < len(listaPals)-1 else ""
       
        if pal not in ocurrencias:
            ocurrencias[pal] = ({}, {})

        if palIzq != "":
            if palIzq not in ocurrencias[pal][0]:
                ocurrencias[pal][0][palIzq] = 1
            else:
                ocurrencias[pal][0][palIzq] += 1
        if palDer != "":
            if palDer not in ocurrencias[pal][1]:
                ocurrencias[pal][1][palDer] = 1
            else:
                ocurrencias[pal][1][palDer] += 1
    return ocurrencias
   
def armar_dicts_bigramas(listaPals, ocurrenciasIzq, ocurrenciasDer):
    i=0
    while i < len(listaPals):
        if (i < len(listaPals)-2):
            grupoDer = (listaPals[i], listaPals[i+1])
            if grupoDer not in ocurrenciasDer:
                ocurrenciasDer[grupoDer] = set()
            ocurrenciasDer[grupoDer].add(listaPals[i+2])
        if (i > 2):
            grupoIzq = (listaPals[i-1],listaPals[i])    
            if grupoIzq not in ocurrenciasIzq:
                ocurrenciasIzq[grupoIzq] = set()
            ocurrenciasIzq[grupoIzq].add(listaPals[i-2])
        i+=1
    return (ocurrenciasIzq, ocurrenciasDer)

def frecuencia_grupos(rutaEntrada):
    archivoEntradas = abrir_archivo(rutaEntrada, 'r')
    frecuenciaGrupos, otraFrecuenciasIzq, otraFrecuenciasDer = {}, {}, {}
    for linea in archivoEntradas:
        dictFrecuencias = armar_dict_frecuencias(linea.split(), frecuenciaGrupos)
        dictsBigramas = armar_dicts_bigramas(linea.split(), otraFrecuenciasIzq, otraFrecuenciasDer)
    archivoEntradas.close()
    return (dictFrecuencias, dictsBigramas)


def may_frecuencia_i(datoFrecuencias, palAnterior, palPosterior):
    esUltimaPal = (palPosterior == "")
    candidato, mayFrec = "", 0
    candidatoAux, frecAux = "", 0
    
    if palAnterior in datoFrecuencias.keys():
        for pal, cantAps in datoFrecuencias[palAnterior][1].items():
            if cantAps > mayFrec and pal != palPosterior and pal != palAnterior:
                # para evitar que una oracion termine con un -potencial- articulo (palabra de longitud 3 o menor)
                longitudValida = (len(pal) > 3)
                if (not esUltimaPal) and longitudValida:
                    mayFrec = cantAps
                    candidato = pal
                # aunque la condicion de arriba no cumpla, guardamos la palabra, en caso de no encontrar otra mejor
                else:
                    candidatoAux = pal
                    frecAux = cantAps
    if (candidato == ""):
        candidato = candidatoAux
        mayFrec = frecAux
    
    return (candidato, mayFrec)

# decidi hacer funciones distintas para mejor lejibilidad
def may_frecuencia_d(datoFrecuencias, palAnterior, palPosterior):
    ultimaPal = (palPosterior == "")
    candidato, candidatoAux = "", ""
    frecAux, mayFrec = 0, 0
    
    if palPosterior in datoFrecuencias.keys():
        for key,val in datoFrecuencias[palPosterior][0].items():
            if val > mayFrec and key != palAnterior and key != palPosterior: 
                # para evitar que una oracion termine con un -potencial- articulo (palabra de longitud 3 o menor)
                if not ultimaPal or (ultimaPal and len(key)>3):
                    mayFrec = val
                    candidato = key
                else:
                    candidatoAux = key
                    frecAux = val
    if (candidato == ""):
        candidato = candidatoAux
        mayFrec = frecAux
    return (candidato, mayFrec)

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
    
def abrir_archivo(nomArch, modoLectura):
    try:
        arch = open(nomArch, modoLectura)
    except:
        print("No se pudo abrir el archivo",nomArch,".Saliendo...")
        exit(-1)
    return arch

def obtener_candidatos(datoFrecuencias, bigramaIzq, bigramaDer, rutaArtista, rutaFrases):
    archivoSalida = abrir_archivo(rutaArtista, 'w')
    archivoFrases = abrir_archivo(rutaFrases, 'r')
    
    for lineaFrase in archivoFrases:
        listaPalabras = lineaFrase.split()
        posPalabraFaltante = pos_pal_faltante(listaPalabras)
        palabrasAnteriores = ("","")
        palabrasPosteriores = ("","")
        candidato = ""
        
        candidatoPorIzq = ("",0)
        candidatoPorDer = ("",0)
            
        if (posPalabraFaltante > 1):
            palabrasAnteriores = (listaPalabras[posPalabraFaltante-2], listaPalabras[posPalabraFaltante-1])
        elif (posPalabraFaltante > 0):
            palabrasAnteriores = ("", listaPalabras[posPalabraFaltante-1])
        if (posPalabraFaltante < (len(listaPalabras)-2)):
            palabrasPosteriores = (listaPalabras[posPalabraFaltante+1], listaPalabras[posPalabraFaltante+2])
        elif (posPalabraFaltante < (len(listaPalabras)-1)):
            palabrasPosteriores = (listaPalabras[posPalabraFaltante+1],"")
        
        candidatotestIzq = bigramaIzq[palabrasAnteriores] if palabrasAnteriores in bigramaIzq else set()
        candidatotestDer = bigramaDer[palabrasPosteriores] if palabrasPosteriores in bigramaDer else set()
        
        if candidatotestIzq != set():
            candidato = candidatotestIzq.pop()
        elif candidatotestDer != set():
            candidato = candidatotestDer.pop()
        else:
     
            candidatoPorIzq = may_frecuencia_i(datoFrecuencias, palabrasAnteriores[1], palabrasPosteriores[0])
            candidatoPorDer = may_frecuencia_d(datoFrecuencias, palabrasAnteriores[1], palabrasPosteriores[0])
            
            candidato = candidatoPorIzq[0] if candidatoPorIzq[1] >= candidatoPorDer[1] else candidatoPorDer[0]
           
        # como ultimo recurso, escoger el candidato de manera aleatoria entre las palabras del texto de entrada.
        if candidato == "":
            while (len(candidato) < 3):
                candidato = choice(list(datoFrecuencias.keys()))
       
        completar_frase(lineaFrase, candidato, archivoSalida)
        
    archivoFrases.close()
    archivoSalida.close()
    return

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
    bigramaDer = dictsBigrama[0]
    bigramaIzq = dictsBigrama[1]
    
    obtener_candidatos(dictFrecuencias, bigramaIzq, bigramaDer, rutaSalida, rutaFrases)

if __name__ == "__main__":
    main()