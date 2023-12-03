from sys import argv

def agrupar(lista, trigrama):
    i=0
    while (i < len(lista)-2):
        grupoTrigrama = (lista[i], lista[i+1], lista[i+2])
        trigrama.add(grupoTrigrama)
        i+=1
    return trigrama

def frecuencia_grupos(rutaEntrada):
    archivoEntradas = open(rutaEntrada, 'r')
    trigrama = set()
    for linea in archivoEntradas:
        frecuenciaGrupos = agrupar(linea.split(), trigrama)
    archivoEntradas.close()
    return frecuenciaGrupos

def frec_trigrama_izq(trigramas, palsAnteriores):
    candidato = ""
    candidatoAux = ""
    print("PALS ANTERIORES: ", palsAnteriores)
    for (pal1,pal2,pal3) in trigramas:
        if (pal1,pal2) == palsAnteriores:
            candidato = pal3
        elif (palsAnteriores != ""):
            if (pal1 == palsAnteriores[0]):
                if (palsAnteriores[1] != ""):
                    candidatoAux = pal3
                else:
                    candidato = pal2
            if (pal2 == palsAnteriores[1]):
                candidato = pal3
    if (candidato == ""):
        candidato = candidatoAux
    return candidato

def frec_trigrama_der(trigramas, palsPosteriores): 
    candidato = ""
    candidatoAux = ""
    print("PALS POSTERIORES: ", palsPosteriores)
    for (pal1,pal2,pal3) in trigramas:
        if (pal2,pal3) == palsPosteriores:
            candidato = pal1
        elif palsPosteriores != "":
            if (pal3 == palsPosteriores[1]):
                if (palsPosteriores[0] != ""):
                    candidatoAux = pal1
                else:
                    candidato = pal2
            if (pal2 == palsPosteriores[0]):
                candidato = pal1
    if (candidato == ""):
        candidato = candidatoAux
    return candidato

def pos_pal_faltante(listaPals):
    i=0
    encontrado = 0
    pospal = 0
    while (i < len(listaPals) and (not encontrado)):
        if ('_' in listaPals[i]):
            encontrado = 1
            pospal = i
        else:
            i += 1
    return pospal

def completar_frase(lineaFrase, palabraCandidata, archivo):
    for palabra in lineaFrase:
        if "_" in palabra:
            archivo.write(palabraCandidata.upper())
        else:
            archivo.write(palabra)
            
def obtener_candidatos(trigrama, rutaArtista, rutaFrases):
    archivoSalida = open(rutaArtista, 'w')
    archivoFrases = open(rutaFrases, 'r')
    
    for lineaFrase in archivoFrases:
        print("-------------------")
        print(lineaFrase)
        listaPalabras = lineaFrase.split()
        posPalabraFaltante = pos_pal_faltante(listaPalabras)
        palabrasAnteriores = ""
        palabrasPosteriores = ""

        candidato = ""
          
        if (posPalabraFaltante == 1):
            palabrasAnteriores = (listaPalabras[posPalabraFaltante-1], "")
        elif (posPalabraFaltante > 1):
            palabrasAnteriores = (listaPalabras[posPalabraFaltante-2],listaPalabras[posPalabraFaltante-1])
            
        if ((posPalabraFaltante == len(listaPalabras)-2)):
            palabrasPosteriores = ("", listaPalabras[posPalabraFaltante+1])
        if ((posPalabraFaltante < len(listaPalabras)-2)):
            palabrasPosteriores = (listaPalabras[posPalabraFaltante+1],listaPalabras[posPalabraFaltante+2])  
        
        candidato = frec_trigrama_izq(trigrama, palabrasAnteriores)
        
        
        if (candidato == ""):
            candidato = frec_trigrama_der(trigrama, palabrasPosteriores)
      
        print("CANDIDATO:", candidato)
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
   
    print("TRIGRAMAS:\n")
    for trigrama in frecuencias:
        print(trigrama)
    
    rutaSalida = "Salidas/" + argv[1] + ".txt"
    rutaFrases = "Frases/" + argv[1] + ".txt"
    obtener_candidatos(frecuencias, rutaSalida, rutaFrases)

if __name__ == "__main__":
    main()