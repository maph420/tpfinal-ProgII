def create_triplets(lista):
    grupos = []
    for i in range(len(lista) - 2):
        grupo = tuple(lista[i:i+3])
        grupos.append(grupo)
    return grupos

# Ejemplo de uso
input_list = [1, 2, 3, 4, 5]
result = create_triplets(input_list)
#print(result)

def fun(frase):
    listaPals = frase.split()
    i = 0
    encontrado = 0
    while (i < len(listaPals) and not encontrado):
        if '_' in listaPals[i]:
            encontrado = 1
        else:
            i+=1
    return ''.join(listaPals[:i])
    
a = fun("hola como _, andas")
print("lista:", a)