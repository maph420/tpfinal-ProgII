def create_triplets(lista):
    grupos = []
    for i in range(len(lista) - 2):
        grupo = tuple(lista[i:i+3])
        grupos.append(grupo)
    return grupos

# Ejemplo de uso
input_list = [1, 2, 3, 4, 5]
result = create_triplets(input_list)
print(result)