from sys import argv

# [1,2,3] -> [(1,2), (2,3)]
def agrupar(lista, frecGrupos):
    i=0
    while (i < len(lista)-1):
        grupo = (lista[i], lista[i+1])
        if grupo in frecGrupos.keys():
            frecGrupos[grupo] +=1
        else:
            frecGrupos[grupo] = 1
        i+=1
    return frecGrupos
        
def frecuencia_grupos(rutaEntrada):
    archivoEntradas = open(rutaEntrada, 'r')
    frecuenciaGrupos = {}
    
    for linea in archivoEntradas:
        frecuenciaGrupos = (agrupar(linea.split(), frecuenciaGrupos))
    #print(frecuenciaGrupos)
    archivoEntradas.close()
    return frecuenciaGrupos


def obtener_may_frecuencia_izq(datoFrecuencias, palAnterior, palPosterior):
    mayorfreq = 0
    palMayorFreq = ""    
    for (pal1, pal2) in datoFrecuencias.keys():
        #print("pal1:",pal1,"pal2:",pal2)
        if (pal1 == palAnterior) and (pal2 != palPosterior) and (pal2 != palAnterior):
            if palMayorFreq == "":
                print(pal2, "!=", palPosterior)
                mayorfreq = datoFrecuencias[(pal1,pal2)]
                palMayorFreq = pal2
            elif (datoFrecuencias[(pal1,pal2)] > mayorfreq):
                print(pal2, "!=", palPosterior)
                mayorfreq = datoFrecuencias[(pal1,pal2)]
                palMayorFreq = pal2
    return (palMayorFreq, mayorfreq)

def obtener_may_frecuencia_der(datoFrecuencias, palPosterior, palAnterior):
    mayorfreq = 0
    palMayorFreq = ""    
    for (pal1, pal2) in datoFrecuencias.keys():
        if pal2 == palPosterior:
            if palMayorFreq == "" and (pal1 != palAnterior) and (pal1 != palPosterior):
                print(pal1, "!=", palAnterior)
                mayorfreq = datoFrecuencias[(pal1,pal2)]
                palMayorFreq = pal1
            elif (datoFrecuencias[(pal1,pal2)] > mayorfreq) and (pal1 != palAnterior) and (pal1 != palPosterior):
                print(pal1, "!=", palAnterior)
                mayorfreq = datoFrecuencias[(pal1,pal2)]
                palMayorFreq = pal1
    return (palMayorFreq, mayorfreq)

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
        
        candidatoPorIzq = ("", 0)
        candidatoPorDer = ("", 0)
        
        # sabemos que como mínimo alguno de los dos if valdrá (exceptuando para la cadena vacia)
        if (posPalabraFaltante > 0):
            palabraAnterior = listaPalabras[posPalabraFaltante-1]
            #print("candidato: ", candidato)
            
        if ((posPalabraFaltante < len(listaPalabras)-1)):
            palabraPosterior = listaPalabras[posPalabraFaltante+1]
        print("palabra anterior: ", palabraAnterior)
        print("palabra posterior: ", palabraPosterior)    
        
        candidatoPorIzq = obtener_may_frecuencia_izq(datoFrecuencias, palabraAnterior, palabraPosterior)
        print("por izquierda, la palabra candidata es:", candidatoPorIzq[0], "con apariciones ", candidatoPorIzq[1])
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
    print("frecuencias: ", frecuencias)
    
    rutaSalida = "Salidas/" + argv[1] + ".txt"
    rutaFrases = "Frases/" + argv[1] + ".txt"
    obtener_candidatos(frecuencias, rutaSalida, rutaFrases)

if __name__ == "__main__":
    main()