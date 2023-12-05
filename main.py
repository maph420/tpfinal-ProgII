from sys import argv

# [1,2,3] -> [(1,2), (2,3)]
def agrupar(listaPals, ocurrencias):
    i=0
    palIzq = ""
    palDer = ""
    for word in listaPals:
        if i>0:
            palIzq = listaPals[i-1]
       
        if i < len(listaPals)-1:
            palDer = listaPals[i+1]
       
        if word not in ocurrencias:
            ocurrencias[word] = ({}, {})

        if palIzq != "":
            if palIzq not in ocurrencias[word][0]:
                ocurrencias[word][0][palIzq] = 1
            else:
                ocurrencias[word][0][palIzq] += 1
        if palDer != "":
            if palDer not in ocurrencias[word][1]:
                ocurrencias[word][1][palDer] = 1
            else:
                ocurrencias[word][1][palDer] += 1
        i+=1
    return ocurrencias
        
def frecuencia_grupos(rutaEntrada):
    archivoEntradas = open(rutaEntrada, 'r')
    frecuenciaGrupos = {}
    for linea in archivoEntradas:
        frecuenciaGrupos = (agrupar(linea.split(), frecuenciaGrupos))
    archivoEntradas.close()
    return frecuenciaGrupos


def obtener_may_frecuencia_izq(datoFrecuencias, palAnterior, palPosterior):
    candidato = ""
    mayFrec = 0
    if palAnterior in datoFrecuencias.keys():
        for key,val in datoFrecuencias[palAnterior][1].items():
            if val > mayFrec and key != palPosterior:
                mayFrec = val
                candidato = key
    return (candidato, mayFrec)

# decidi hacer funciones distintas para mejor lejibilidad
def obtener_may_frecuencia_der(datoFrecuencias, palAnterior, palPosterior):
    candidato = ""
    mayFrec = 0
    if palPosterior in datoFrecuencias.keys():
        for key,val in datoFrecuencias[palPosterior][0].items():
            if val > mayFrec and val != palAnterior:
                mayFrec = val
                candidato = key
    return (candidato, mayFrec)

def pos_pal_faltante(listaPals):
    i=0
    encontrado = 0
    pospal = 0
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
    
def obtener_candidatos(datoFrecuencias, rutaArtista, rutaFrases):
    archivoSalida = open(rutaArtista, 'w')
    archivoFrases = open(rutaFrases, 'r')
    
    for key, value in datoFrecuencias.items():
        print(f"{key}->{value}")
        
    #print("datoFrecuencias: ", datoFrecuencias)
    #print("----------------")
    
    for lineaFrase in archivoFrases:
        print("linea: ", lineaFrase)
        listaPalabras = lineaFrase.split()
        posPalabraFaltante = pos_pal_faltante(listaPalabras)
        palabraAnterior = ""
        palabraPosterior = ""
        candidato = ""
        
        candidatoPorIzq = ("",0)
        candidatoPorDer = ("",0)
        
        # sabemos que como mínimo alguno de los dos if valdrá (exceptuando para la cadena vacia)
        if (posPalabraFaltante > 0):
            palabraAnterior = listaPalabras[posPalabraFaltante-1]
            
        if ((posPalabraFaltante < len(listaPalabras)-1)):
            palabraPosterior = listaPalabras[posPalabraFaltante+1]
            
        print("palabra anterior: ", palabraAnterior)
        print("palabra posterior: ", palabraPosterior)    
        
        candidatoPorIzq = obtener_may_frecuencia_izq(datoFrecuencias, palabraAnterior, palabraPosterior)
        print("por izquierda, la palabra candidata es:", candidatoPorIzq[0], "con apariciones: ", candidatoPorIzq[1])
        
        candidatoPorDer = obtener_may_frecuencia_der(datoFrecuencias, palabraPosterior, palabraAnterior)
        print("por derecha, la palabra candidata es:", candidatoPorDer[0], "con apariciones: ", candidatoPorDer[1])
            
        candidato = candidatoPorIzq[0] if candidatoPorIzq[1] >= candidatoPorDer[1] else candidatoPorDer[0]
        print("entonces, el mas adecuado es:", candidato)
        # buscar posibles palabras anteriores
        completar_frase(lineaFrase, candidato, archivoSalida)
        
    archivoFrases.close()
    archivoSalida.close()
    return

def main():
    if (len(argv) != 2):
        print("Cantidad incorrecta de argumentos. Saliendo...")
        exit(-1)    

    rutaEntrada = "Entradas/" + argv[1] + ".txt"
    frecuencias = frecuencia_grupos(rutaEntrada)
    
    rutaSalida = "Salidas/" + argv[1] + ".txt"
    rutaFrases = "Frases/" + argv[1] + ".txt"
    obtener_candidatos(frecuencias, rutaSalida, rutaFrases)

if __name__ == "__main__":
    main()