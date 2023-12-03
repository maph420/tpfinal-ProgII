from collections import defaultdict

def crear_diccionario_palabras(s):
    palabras = s.split()
    diccionario = defaultdict(lambda: defaultdict(int))

    for i in range(len(palabras) - 1):
        palabra_actual = palabras[i]
        palabra_siguiente = palabras[i + 1]

        diccionario[palabra_actual][palabra_siguiente] += 1

    # Convertir el diccionario interno a tuplas
    for palabra, vecinos in diccionario.items():
        diccionario[palabra] = tuple((vecino, cantidad) for vecino, cantidad in vecinos.items())

    return diccionario

# Ejemplo de uso:
cadena_ejemplo = "flaca no me claves tus punales por la espalda tan profundo no me duelen no me hacen mal"
resultado = crear_diccionario_palabras(cadena_ejemplo)

# Imprimir el resultado
for palabra in resultado:
    print(palabra)