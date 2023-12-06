//librerias
#include "functions.h"

int main(int argc, char** argv) {

    int verif, llamadaPython;
    char* rutaArtista, **textos, *nomArchivoDestino;
    
    if (argc != 2) {
        printf("Numero de argumentos incorrecta.\nUso: ./main nombre_de_artista\n");
        return -1;
    }
    char* cadenasRutaArtista[] = {RUTA_A_LEER, argv[1]};
    rutaArtista = armar_cadena(cadenasRutaArtista, 2);

    textos = obtener_textos(rutaArtista);
    if (textos == NULL) {
        free(rutaArtista);
        return -1;
    }

    char* cadenasArchDest[] = {RUTA_A_ESCRIBIR, argv[1], ".txt"};
    nomArchivoDestino = armar_cadena(cadenasArchDest, 3);

    verif = recorrer_y_limpiar(textos, rutaArtista, nomArchivoDestino);
    if (verif != 0) {
        return -1;
    }

    free(textos);
    free(rutaArtista);
    free(nomArchivoDestino);

    llamadaPython = llamar_python(argv[1]);
    if (llamadaPython != 0) {
        printf("Error: no se pudo llamar al script en python.\n");
        return -1;
    }
    return 0;
}