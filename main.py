from sys import argv

# [1,2,3] -> [(1,2), (2,3)]
def armar_grupos_de_dos(l, aparicionesParejas):
    i=0
    j=1
    while (j < len(l)):
        t = (l[i], l[j])
        if t in aparicionesParejas.keys():
            aparicionesParejas[t] +=1
        else:
            aparicionesParejas[t] = 1
        i+=1
        j+=1
    #print(aparicionesParejas)
    return aparicionesParejas
        

def apariciones_grupos(rutaArtista):
    archivoEntradas = open(rutaArtista, 'r')
    frecuenciaGrupos = {}
    
    for linea in archivoEntradas:
        frecuenciaGrupos = (armar_grupos_de_dos(linea.split(), frecuenciaGrupos))
    #print(frecuenciaGrupos)
    archivoEntradas.close()
    return frecuenciaGrupos

def obtener_pos_pal_faltante(frase):
    i=0
    encontrado = 0
    pospal = 0
    while (i < len(frase) and (not encontrado)):
        if (frase[i] == '_'):
            encontrado = 1
            pospal = i
        else:
            i += 1
    return pospal

def obtener_may_frecuencia_izq(datoFrecuencias, palAnterior):
    mayorfreq = 1
    palMayorFreq = ""    
    for (pal1, pal2) in datoFrecuencias.keys():
        if pal1 == palAnterior:
            if palMayorFreq == "":
                palMayorFreq = pal2
            if datoFrecuencias[(pal1,pal2)] > mayorfreq:
                mayorfreq = datoFrecuencias[(pal1,pal2)]
                palMayorFreq = pal2
    return (palMayorFreq, mayorfreq)

def obtener_may_frecuencia_der(datoFrecuencias, palPosterior):
    mayorfreq = 1
    palMayorFreq = ""    
    for (pal1, pal2) in datoFrecuencias.keys():
        if pal2 == palPosterior:
            if palMayorFreq == "":
                palMayorFreq = pal1
            if datoFrecuencias[(pal1,pal2)] > mayorfreq:
                mayorfreq = datoFrecuencias[(pal1,pal2)]
                palMayorFreq = pal1
    return (palMayorFreq, mayorfreq)

def completar_frase(frase, palabraCandidata, archivo):
    listaFrase = frase.split()
    i=0
    for palabra in frase:
        if palabra == "_":
            archivo.write(palabraCandidata.upper())
        else:
            archivo.write(palabra)
    archivo.write("\n")
    


def obtener_candidatos(datoFrecuencias, rutaArtista):
    archivoSalida = open(rutaArtista, 'w')
    
    rutaFrases = "Frases/" + argv[1] + ".txt"
    archivoFrases = open(rutaFrases, 'r')
    
    for key, value in datoFrecuencias.items():
        print(f"{key}->{value}")
        
    #print("datoFrecuencias: ", datoFrecuencias)
    
    #print("----------------")
    for frase in archivoFrases:
        listaPalabras = frase.split()
        #print(listaPalabras)
        
        posPalabraFaltante = obtener_pos_pal_faltante(listaPalabras)
        palabraAnterior = ""
        palabraPosterior = ""
        candidato = ""
        
        t1 = ("", 0)
        t2 = ("", 0)
        
        # sabemos que como mínimo alguno de los dos if valdrá (exceptuando para la cadena vacia)
        if (posPalabraFaltante > 0):
            palabraAnterior = listaPalabras[posPalabraFaltante-1]
            t1 = obtener_may_frecuencia_izq(datoFrecuencias, palabraAnterior)
            candidato = t1[0]
            #print("candidato: ", candidato)
            
        if ((posPalabraFaltante < len(listaPalabras)-1) and candidato == ""):
            palabraPosterior = listaPalabras[posPalabraFaltante+1]
            t2 = obtener_may_frecuencia_der(datoFrecuencias, palabraPosterior)
            if t2[0] != "":
                candidato = t2[0]
        # buscar posibles palabras anteriores
        completar_frase(frase, candidato, archivoSalida)
        
        
    archivoFrases.close()
    archivoSalida.close()
    return

def main():
    if (len(argv) != 2):
        print("Cantidad incorrecta de argumentos. Saliendo...")
        exit(-1)    

    rutaArtista = "Entradas/" + argv[1] + ".txt"
    frecuencias = apariciones_grupos(rutaArtista)
    rutaSalida = "Salidas/" + argv[1] + ".txt"
    obtener_candidatos(frecuencias, rutaSalida)

if __name__ == "__main__":
    main()