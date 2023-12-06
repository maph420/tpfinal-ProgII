from main import armar_dict_frecuencias, armar_dicts_bigramas, frecuencia_grupos, may_frecuencia_i, may_frecuencia_d, pos_pal_faltante, completar_frase, obtener_candidatos

#armar_dict_frecuencias(listaPals, ocurrencias):

#armar_dicts_bigramas(listaPals, bigramasI, bigramasD):

#frecuencia_grupos(rutaEntrada)

#may_frecuencia_i(datoFrecuencias, palAnterior, palPosterior)
    
#may_frecuencia_d(datoFrecuencias, palAnterior, palPosterior)
    
#completar_frase(lineaFrase, palabraCandidata, archivo)
    
#obtener_candidatos(datoFrecuencias, bigramaIzq, bigramaDer, rutaArtista, rutaFrases)
   

def test_pos_pal_faltante():
    assert pos_pal_faltante(['el', 'dia', 'se', 'encuentra', '_']) == 4
    assert pos_pal_faltante(['jugo', '_', 'luna', 'me', 'diste']) == 1
    assert pos_pal_faltante(['_', 'importa', 'si', 'las', 'horas', 'pasan']) == 0
    assert pos_pal_faltante(["_"],) == 0
    # este caso no resulta relevante (asumiendo que las frases a completar nunca son vacias)
    assert pos_pal_faltante([]) == 0
    
test_pos_pal_faltante()