from sys import argv
from random import choice

# [1,2,3] -> [(1,2), (2,3)]
def agrupar(listaPals, ocurrencias):
    i=0
    palIzq = ""
    palDer = ""
    for pal in listaPals:
        if i>0:
            palIzq = listaPals[i-1]
       
        if i < len(listaPals)-1:
            palDer = listaPals[i+1]
       
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
        i+=1
    return ocurrencias
   
def otro_agrupar(listaPals, ocurrenciasIzq, ocurrenciasDer):
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
    archivoEntradas = open(rutaEntrada, 'r')
    frecuenciaGrupos = {}
    otraFrecuenciasIzq = {}
    otraFrecuenciasDer = {}
    for linea in archivoEntradas:
        frecuenciaGrupos = agrupar(linea.split(), frecuenciaGrupos)
        otraFrecuencias = otro_agrupar(linea.split(), otraFrecuenciasIzq, otraFrecuenciasDer)
    archivoEntradas.close()
    return (frecuenciaGrupos, otraFrecuencias)


def obtener_may_frecuencia_izq(datoFrecuencias, palAnterior, palPosterior):
    ultimaPal = True if palPosterior == "" else False
    candidato = ""
    candidatoAux = ""
    frecAux = 0
    mayFrec = 0
    if palAnterior in datoFrecuencias.keys():
        for key,val in datoFrecuencias[palAnterior][1].items():
            if val > mayFrec and key != palPosterior and key != palAnterior:
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

# decidi hacer funciones distintas para mejor lejibilidad
def obtener_may_frecuencia_der(datoFrecuencias, palAnterior, palPosterior):
    ultimaPal = True if palPosterior == "" else False
    candidato = ""
    mayFrec = 0
    candidatoAux = ""
    frecAux = 0
    
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
    
def obtener_candidatos(datoFrecuencias, bigramaIzq, bigramaDer, rutaArtista, rutaFrases):
    archivoSalida = open(rutaArtista, 'w')
    archivoFrases = open(rutaFrases, 'r')
    
    for key, value in datoFrecuencias.items():
        print(f"{key}->{value}")
    
    for lineaFrase in archivoFrases:
        print("linea: ", lineaFrase)
        listaPalabras = lineaFrase.split()
        posPalabraFaltante = pos_pal_faltante(listaPalabras)
        palabraAnterior = ""
        palabraPosterior = ""
        palabrasAnteriores = ("","")
        palabrasPosteriores = ("","")
        candidato = ""
        
        candidatoPorIzq = ("",0)
        candidatoPorDer = ("",0)
        
        # sabemos que como mínimo alguno de los dos if valdrá (exceptuando para la cadena vacia)
        if (posPalabraFaltante > 0):
            palabraAnterior = listaPalabras[posPalabraFaltante-1]
            
        if ((posPalabraFaltante < len(listaPalabras)-1)):
            palabraPosterior = listaPalabras[posPalabraFaltante+1]
            
        if (posPalabraFaltante > 1):
            palabrasAnteriores = (listaPalabras[posPalabraFaltante-2], listaPalabras[posPalabraFaltante-1])
        if (posPalabraFaltante < (len(listaPalabras)-2)):
            palabrasPosteriores = (listaPalabras[posPalabraFaltante+1], listaPalabras[posPalabraFaltante+2])
        
        if (palabrasAnteriores != ""):
            print("palabras anteriores:",palabrasAnteriores)
        
        if (palabrasPosteriores != ""):
            print("palabras anteriores:",palabrasPosteriores)
        
        candidatotestIzq = set()
        candidatotestDer = set()
        
        if palabrasAnteriores in bigramaIzq:
            candidatotestIzq = bigramaIzq[palabrasAnteriores]
        if palabrasPosteriores in bigramaDer:
            candidatotestDer = bigramaDer[palabrasPosteriores]
        
        print("candidato test izq: ", candidatotestIzq)
        print("candidato test der ", candidatotestDer)    
        if candidatotestIzq != set():
            candidato = candidatotestIzq.pop()
        elif candidatotestDer != set():
            candidato = candidatotestDer.pop()
        else:
            print("SIN CANDIDATOS EXACTOS")
        
            candidatoPorIzq = obtener_may_frecuencia_izq(datoFrecuencias, palabraAnterior, palabraPosterior)
            print("por izquierda, la palabra candidata es:", candidatoPorIzq[0], "con apariciones: ", candidatoPorIzq[1])
        
            candidatoPorDer = obtener_may_frecuencia_der(datoFrecuencias, palabraAnterior, palabraPosterior)
            print("por derecha, la palabra candidata es:", candidatoPorDer[0], "con apariciones: ", candidatoPorDer[1])
            
            candidato = candidatoPorIzq[0] if candidatoPorIzq[1] >= candidatoPorDer[1] else candidatoPorDer[0]
            print("entonces, el mas adecuado es:", candidato)
        
        # como ultimo recurso, escoger el candidato de manera aleatoria entre las palabras del texto de entrada.
        if candidato == "":
            while (len(candidato) < 3):
                candidato = choice(list(datoFrecuencias.keys()))
       
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
    
    frec1 = frecuencias[0]
    frec2 = frecuencias[1]
    bigramaDer = frec2[0]
    bigramaIzq = frec2[1]
    
    print("bigramas por izquierda:")
    for k,v in bigramaIzq.items():
        print(k,"->",v)
    print("----")
    print("bigramas por derecha:")
    for k,v in bigramaDer.items():
        print(k,"->",v)
    print("----")
    rutaSalida = "Salidas/" + argv[1] + ".txt"
    rutaFrases = "Frases/" + argv[1] + ".txt"
    obtener_candidatos(frec1, bigramaIzq, bigramaDer, rutaSalida, rutaFrases)

if __name__ == "__main__":
    main()