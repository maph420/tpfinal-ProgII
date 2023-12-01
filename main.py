from sys import argv

# [1,2,3] -> [(1,2), (2,3)]
def armar_grupos_de_dos(l):
    listaTuplas = []
    i=0
    j=1
    while (j < len(l)):
        t = (l[i], l[j])
        listaTuplas.append(t)
        i+=1
        j+=1
    return listaTuplas
        

def parse_entries():
    rutaArtista = "Entradas/" + argv[1] + ".txt"
    archivoEntradas = open(rutaArtista, 'r')
    i=0
    l = []
    
    for a in archivoEntradas:
        l += armar_grupos_de_dos(a.split())
        i+=1
    print(l)
    archivoEntradas.close()
    return {}


def completar_frases():
    rutaFrases = "Frases/" + argv[1] + ".txt"
    archivoFrases = open(rutaFrases, 'r')
    
    archivoFrases.close()


def main():
    if (len(argv) != 2):
        print("Cantidad incorrecta de argumentos. Saliendo...")
        exit(-1)    

    entradas = {}
    entradas = parse_entries()


if __name__ == "__main__":
    main()