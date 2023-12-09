import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
 
# now we can import the module in the parent
# directory.
import main
 

from main import armar_dict_frecuencias, armar_dicts_bigramas, may_frecuencia, pos_pal_faltante, completar_frase, obtener_pal_anteriores, obtener_pal_posteriores
   
def test_obtener_pal_anteriores():
    # Caso 1: lista vacia
    result = obtener_pal_anteriores([], 0)
    assert result == ("", "")

    # Caso 2: palabra en la primer posicion
    listaPalabras = ["sol", "brilla", "en", "el", "cielo"]
    posPal = 0
    result = obtener_pal_anteriores(listaPalabras, posPal)
    assert result == ("", "")

    # Caso 3: palabra en la segunda posicion
    listaPalabras = ["sol", "brilla", "en", "el", "cielo"]
    posPal = 1
    result = obtener_pal_anteriores(listaPalabras, posPal)
    assert result == ("", "sol")

    # Caso 4: ejemplo generico
    listaPalabras = ["sol", "brilla", "en", "el", "cielo"]
    posPal = 3
    result = obtener_pal_anteriores(listaPalabras, posPal)
    assert result == ("brilla", "en")

    # Caso 5: palabra en la ultima posicion
    listaPalabras = ["sol", "brilla", "en", "el", "cielo"]
    posPal = 4
    result = obtener_pal_anteriores(listaPalabras, posPal)
    assert result == ("en", "el")

def test_obtener_pal_posteriores():
    # Caso 1: lista vacia
    listaPalabras = []
    posPal = 0
    result = obtener_pal_posteriores(listaPalabras, posPal)
    assert result == ("", "")

    # Caso 2: palabra en la primer posicion
    listaPalabras = ["sol", "brilla", "en", "el", "cielo"]
    posPal = 0
    result = obtener_pal_posteriores(listaPalabras, posPal)
    assert result == ("brilla", "en")

    # Caso 3: caso generico
    listaPalabras = ["en", "la", "cumbre", "nevada", "suele", "hacer", "frio"]
    posPal = 3
    result = obtener_pal_posteriores(listaPalabras, posPal)
    assert result == ("suele", "hacer")

    # Caso 4: palabra en penúltima posicion
    listaPalabras = ["sol", "brilla", "en", "el", "cielo"]
    posPal = 3
    result = obtener_pal_posteriores(listaPalabras, posPal)
    assert result == ("cielo", "")

    # Caso 5: palabra en ultima posicion
    listaPalabras = ["sol", "brilla", "en", "el", "cielo"]
    posPal = 4
    result = obtener_pal_posteriores(listaPalabras, posPal)
    assert result == ("", "")

def test_armar_dict_frecuencias():
    # Caso 1: Lista de palabras vacia
    listPals = "".split()
    dictTest = armar_dict_frecuencias(listPals, {})
    assert dictTest == {}
    
    # Caso 2: Lista con una unica palabra
    listPals = "unica".split()
    dictTest = armar_dict_frecuencias(listPals, {})
    assert dictTest == {'unica': ({}, {})}
    
    # Caso 3: Lista con dos palabras
    listPals = "la luna".split()
    dictTest = armar_dict_frecuencias(listPals, {})
    assert dictTest == {'la': ({}, {'luna': 1}), 
                         'luna': ({'la': 1}, {})}

    # Caso 4: Lista sin ningun par de palabras juntos mas de una vez
    listPals = "la estrella fugaz de la noche".split()
    dictTest = armar_dict_frecuencias(listPals, {})
    assert dictTest == {'la': ({'de': 1}, {'estrella': 1, 'noche': 1}), 
                        'estrella': ({'la': 1}, {'fugaz': 1}), 
                        'fugaz': ({'estrella': 1}, {'de': 1}), 
                        'de': ({'fugaz': 1}, {'la': 1}), 
                        'noche': ({'la': 1}, {})}
    
    # Caso 5: Lista con algunos pares de palabras juntos mas de una vez
    listPals = "el sol brilla y brilla ilumina el día día tras día día tras día día tras día".split()
    dictTest = armar_dict_frecuencias(listPals, {})
    assert dictTest == {'el': ({'ilumina': 1}, {'sol': 1, 'día': 1}), 
                         'sol': ({'el': 1}, {'brilla': 1}), 
                         'brilla': ({'sol': 1, 'y': 1}, {'y': 1, 'ilumina': 1}), 
                         'y': ({'brilla': 1}, {'brilla': 1}), 
                         'ilumina': ({'brilla': 1}, {'el': 1}), 
                         'día': ({'el': 1, 'día': 3, 'tras': 3}, {'día': 3, 'tras': 3}), 
                         'tras': ({'día': 3}, {'día': 3})}
    print(armar_dict_frecuencias("hoy sale la luna o se apaga la luna".split(),{}))
    
def test_armar_dicts_bigramas():    
    
    # Caso 1: lista de palabras vacia
    listPals = "".split()
    dictTest = armar_dicts_bigramas(listPals, {}, {})
    assert dictTest[0] == {}
    assert dictTest[1] == {}
    
    # Caso 2: lista con una unica palabra
    listPals = "unica".split()
    dictTest = armar_dicts_bigramas(listPals, {}, {})
    assert dictTest[0] == {}
    assert dictTest[1] == {}
    
    # Caso 3: lista con dos palabras
    listPals = "el dia".split()
    dictTest = armar_dicts_bigramas(listPals, {}, {})
    assert dictTest[0] == {}
    assert dictTest[1] == {}
    
    # Caso 4: lista de >2 palabras, con palabras repetidas no contiguas
    listPals = "naranja color naranja".split()
    dictTest = armar_dicts_bigramas(listPals, {}, {})
    assert dictTest[0] == {('color', 'naranja'): {'naranja'}}
    assert dictTest[1] == {('naranja', 'color'): {'naranja'}}

    # Caso 5: lista de >2 palabras, con palabras repetidas contiguas
    listPals = "luna luna azul".split()
    dictTest = armar_dicts_bigramas(listPals, {}, {})
    assert dictTest[0] == {('luna', 'azul'): {'luna'}}
    assert dictTest[1] == {('luna', 'luna'): {'azul'}}

    # Caso 6: lista de >2 palabras generica 
    listPals = "el espadachin negro hizo su cometido de nuevo".split()
    dictTest = armar_dicts_bigramas(listPals, {}, {})
    assert dictTest[0] == {('espadachin', 'negro'): {'el'}, 
                         ('negro', 'hizo'): {'espadachin'}, 
                         ('hizo', 'su'): {'negro'}, 
                         ('su', 'cometido'): {'hizo'}, 
                         ('cometido', 'de'): {'su'}, 
                         ('de', 'nuevo'): {'cometido'}}
    assert dictTest[1] == {('el', 'espadachin'): {'negro'}, 
                            ('espadachin', 'negro'): {'hizo'}, 
                            ('negro', 'hizo'): {'su'}, 
                            ('hizo', 'su'): {'cometido'}, 
                            ('su', 'cometido'): {'de'}, 
                            ('cometido', 'de'): {'nuevo'}}

def test_pos_pal_faltante():
    assert pos_pal_faltante(['el', 'dia', 'se', 'encuentra', '_']) == 4
    assert pos_pal_faltante(['jugo', '_', 'luna', 'me', 'diste']) == 1
    assert pos_pal_faltante(['_', 'importa', 'si', 'las', 'horas', 'pasan']) == 0
    assert pos_pal_faltante(["_"],) == 0
    # este caso no resulta relevante (asumiendo que las frases a completar nunca son vacias)
    assert pos_pal_faltante([]) == 0
    
def test_may_frecuencia():
    # Caso 1: Palabra anterior no esta en el diccionario
    dictFrecuencias = {}
    palAnterior, palPosterior = "sol", "brilla"
    result = may_frecuencia(dictFrecuencias, palAnterior, palPosterior)
    assert result == ""

    # Caso 2: Palabra anterior está en el diccionario, pero no tiene frecuencias por derecha
    # brilla directamente no esta entre las claves del diccionario, entonces la unica alternativa
    # es ver que hay a la derecha de sol, pero a la derecha de sol no hay nada
    # frase: "el sol brilla"
    dictFrecuencias = {"el": ({}, {'sol': 1}),
                        "sol": ({'el': 1}, {})}
    palAnterior, palPosterior = "sol", "brilla"
    result = may_frecuencia(dictFrecuencias, palAnterior, palPosterior)
    assert result == ""

    # Caso 3: Encuentra candidatos por izquierda y derecha, se queda con la izquierda
    # frase: hoy sale el sol hoy el sol brilla
    dictFrecuencias = {'hoy': ({'sol': 1}, {'sale': 1, 'el': 1}), 
                       'sale': ({'hoy': 1}, {'el': 1}), 
                       'el': ({'sale': 1, 'hoy': 1}, {'sol': 2}), 
                       'sol': ({'el': 2}, {'hoy': 1, 'brilla': 1}), 
                       'brilla': ({'sol': 1}, {})}
    palAnterior, palPosterior = "el", "hoy"
    result = may_frecuencia(dictFrecuencias, palAnterior, palPosterior)
    assert result == "sol"  

    # Caso 4: Encontrar candidato como ultima palabra
    # frase: hoy sale la luna o se apaga la luna
    dictFrecuencias = {'hoy': ({}, {'sale': 1}), 
                       'sale': ({'hoy': 1}, {'la': 1}), 
                       'la': ({'sale': 1, 'apaga': 1}, {'luna': 2}), 
                       'luna': ({'la': 2}, {'o': 1}), 
                       'o': ({'luna': 1}, {'se': 1}), 
                       'se': ({'o': 1}, {'apaga': 1}), 
                       'apaga': ({'se': 1}, {'la': 1})}
    palAnterior, palPosterior = "la", ""
    result = may_frecuencia(dictFrecuencias, palAnterior, palPosterior)
    assert result == "luna"  

    # Caso 5: Encuentra dos posibles candidatos (misma frecuencia), por defecto se queda con el primero
    # Frase: el increible color el esperanzador color
    dictFrecuencias = {'el': ({'color': 1}, {'increible': 1, 'esperanzador': 1}), 
                       'increible': ({'el': 1}, {'color': 1}), 
                       'color': ({'increible': 1, 'esperanzador': 1}, {'el': 1}), 
                       'esperanzador': ({'el': 1}, {'color': 1})}
    palAnterior, palPosterior = "el", "color"
    assert may_frecuencia(dictFrecuencias, palAnterior, palPosterior) == "increible"

# recorremos unicamente una vez el archivo para verificar
# los enters son agregados manualmente para separar las frases por renglones
# (como trabaja la funcion)
def test_completar_frase():
    # con la opcion w+ se abre para escribir y leer, y en caso de escribir se pisa lo anterior
    archivoTests = open("Tests/archivo_a_escribir.txt", 'w+')
    
    completar_frase("esta frase va a ser _\n", "completada", archivoTests)
    completar_frase("el _ azul\n", "cielo", archivoTests)
    completar_frase("_ frase contiene dos caracteres _\n", "esta", archivoTests)
    completar_frase("dia_nublado\n", " ", archivoTests)
    completar_frase("frase sin cambios\n", "palabra", archivoTests)
    
    frasesCompletas = ["esta frase va a ser COMPLETADA\n", "el CIELO azul\n",
                       "ESTA frase contiene dos caracteres ESTA\n", "dia nublado\n",
                       "frase sin cambios\n"]    
    
    for i, linea in enumerate(archivoTests):
        if i<5: 
            assert linea == frasesCompletas[i]
    
    archivoTests.close()

# En tanto a las funciones frecuencia_grupos() y obtener_candidatos() no considere adecado hacerles un
# testing, ya que dichas funciones se basan en una combinacion de distintas llamadas a las funciones testeadas
# con anterioridad.

def main():
    test_pos_pal_faltante()
    test_armar_dict_frecuencias()
    test_armar_dicts_bigramas()
    test_may_frecuencia()
    test_completar_frase()
    test_obtener_pal_anteriores()
    test_obtener_pal_posteriores()

if __name__ == "__main__": 
    main()