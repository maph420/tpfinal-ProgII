from main import armar_dict_frecuencias, armar_dicts_bigramas, frecuencia_grupos, may_frecuencia_i, may_frecuencia_d, pos_pal_faltante, completar_frase, obtener_candidatos

#frecuencia_grupos(rutaEntrada)
    
#may_frecuencia_d(datoFrecuencias, palAnterior, palPosterior)
    
#completar_frase(lineaFrase, palabraCandidata, archivo)
    
# ?
#obtener_candidatos(datoFrecuencias, bigramaIzq, bigramaDer, rutaArtista, rutaFrases)
   
def test_armar_dict_frecuencias():
    
    # Caso 1: Lista de palabras vacia
    listaPals1 = "".split()
    dictTest1 = armar_dict_frecuencias(listaPals1, {})
    assert dictTest1 == {}
    
    # Caso 2: Lista con una unica palabra
    listaPals2 = "unica".split()
    dictTest2 = armar_dict_frecuencias(listaPals2, {})
    assert dictTest2 == {'unica': ({}, {})}
    
    # Caso 3: Lista con dos palabras
    listaPals3 = "la luna".split()
    dictTest3 = armar_dict_frecuencias(listaPals3, {})
    assert dictTest3 == {'la': ({}, {'luna': 1}), 
                         'luna': ({'la': 1}, {})}

    # Caso 4: Lista sin ningun par de palabras juntos mas de una vez
    listaPals4 = "la estrella fugaz de la noche".split()
    dictTest4 = armar_dict_frecuencias(listaPals4, {})
    assert dictTest4 == {'la': ({'de': 1}, {'estrella': 1, 'noche': 1}), 
                        'estrella': ({'la': 1}, {'fugaz': 1}), 
                        'fugaz': ({'estrella': 1}, {'de': 1}), 
                        'de': ({'fugaz': 1}, {'la': 1}), 
                        'noche': ({'la': 1}, {})}
    
    # Caso 5: Lista con algunos pares de palabras juntos mas de una vez
    listaPals5 = "el sol brilla y brilla ilumina el día día tras día día tras día día tras día".split()
    dictTest5 = armar_dict_frecuencias(listaPals5, {})
    assert dictTest5 == {'el': ({'ilumina': 1}, {'sol': 1, 'día': 1}), 
                         'sol': ({'el': 1}, {'brilla': 1}), 
                         'brilla': ({'sol': 1, 'y': 1}, {'y': 1, 'ilumina': 1}), 
                         'y': ({'brilla': 1}, {'brilla': 1}), 
                         'ilumina': ({'brilla': 1}, {'el': 1}), 
                         'día': ({'el': 1, 'día': 3, 'tras': 3}, {'día': 3, 'tras': 3}), 
                         'tras': ({'día': 3}, {'día': 3})}
    print("Los test de armar_dict_frecuencias pasaron correctamente.")
    print(armar_dict_frecuencias("hoy sale el sol hoy el sol brilla".split(), {}))
    
def test_armar_dicts_bigramas():    
    
    # Caso 1: lista de palabras vacia
    listaPals1 = "".split()
    dictTest1 = armar_dicts_bigramas(listaPals1, {}, {})
    assert dictTest1[0] == {}
    assert dictTest1[1] == {}
    
    # Caso 2: lista con una unica palabra
    listaPals2 = "unica".split()
    dictTest2 = armar_dicts_bigramas(listaPals2, {}, {})
    assert dictTest2[0] == {}
    assert dictTest2[1] == {}
    
    # Caso 3: lista con dos palabras
    listaPals3 = "el dia".split()
    dictTest3 = armar_dicts_bigramas(listaPals3, {}, {})
    assert dictTest3[0] == {}
    assert dictTest3[1] == {}
    
    # Caso 4: lista de >2 palabras, con palabras repetidas no contiguas
    listaPals4 = "naranja color naranja".split()
    dictTest4 = armar_dicts_bigramas(listaPals4, {}, {})
    assert dictTest4[0] == {('color', 'naranja'): {'naranja'}}
    assert dictTest4[1] == {('naranja', 'color'): {'naranja'}}

    # Caso 5: lista de >2 palabras, con palabras repetidas contiguas
    listaPals5 = "luna luna azul".split()
    dictTest5 = armar_dicts_bigramas(listaPals5, {}, {})
    assert dictTest5[0] == {('luna', 'azul'): {'luna'}}
    assert dictTest5[1] == {('luna', 'luna'): {'azul'}}

    # Caso 6: lista de >2 palabras generica 
    listaPals6 = "el espadachin negro hizo su cometido de nuevo".split()
    dictTest6 = armar_dicts_bigramas(listaPals6, {}, {})
    assert dictTest6[0] == {('espadachin', 'negro'): {'el'}, 
                         ('negro', 'hizo'): {'espadachin'}, 
                         ('hizo', 'su'): {'negro'}, 
                         ('su', 'cometido'): {'hizo'}, 
                         ('cometido', 'de'): {'su'}, 
                         ('de', 'nuevo'): {'cometido'}}
    assert dictTest6[1] == {('el', 'espadachin'): {'negro'}, 
                            ('espadachin', 'negro'): {'hizo'}, 
                            ('negro', 'hizo'): {'su'}, 
                            ('hizo', 'su'): {'cometido'}, 
                            ('su', 'cometido'): {'de'}, 
                            ('cometido', 'de'): {'nuevo'}}
    
    print("Los test de armar_dicts_bigramas pasaron correctamente.")

def test_pos_pal_faltante():
    assert pos_pal_faltante(['el', 'dia', 'se', 'encuentra', '_']) == 4
    assert pos_pal_faltante(['jugo', '_', 'luna', 'me', 'diste']) == 1
    assert pos_pal_faltante(['_', 'importa', 'si', 'las', 'horas', 'pasan']) == 0
    assert pos_pal_faltante(["_"],) == 0
    # este caso no resulta relevante (asumiendo que las frases a completar nunca son vacias)
    assert pos_pal_faltante([]) == 0
    print("Los test de pos_pal_faltante pasaron correctamente.")

def test_may_frecuencia_i():
    # Caso 1: Palabra anterior no esta en el diccionario
    dictFrecuencias = {}
    palAnterior, palPosterior = "sol", "brilla"
    result = may_frecuencia_i(dictFrecuencias, palAnterior, palPosterior)
    assert result == ("", 0)

    # Caso 2: Palabra anterior está en el diccionario, pero no tiene frecuencias por derecha
    # brilla directamente no esta entre las claves del diccionario, entonces la unica alternativa
    # es ver que hay a la derecha de sol, pero a la derecha de sol no hay nada
    # frase: "el sol brilla"
    dictFrecuencias = {"el": ({}, {'sol': 1}),
                        "sol": ({'el': 1}, {})}
    palAnterior, palPosterior = "sol", "brilla"
    result = may_frecuencia_i(dictFrecuencias, palAnterior, palPosterior)
    assert result == ("", 0)


    # Caso de prueba 4: Palabra anterior con múltiples frecuencias a la derecha, elige la de mayor frecuencia
    dictFrecuencias = {"sol": ({}, {"brilla": 2, "sale": 3, "amanecer": 1})}
    palAnterior, palPosterior = "sol", "brilla"
    result = may_frecuencia_i(dictFrecuencias, palAnterior, palPosterior)
    assert result == ("sale", 3)

def main():
    test_pos_pal_faltante()
    test_armar_dict_frecuencias()
    test_armar_dicts_bigramas()
    test_may_frecuencia_i()


if __name__ == "__main__": 
    main()