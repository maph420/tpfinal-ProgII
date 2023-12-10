#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LONGITUD_MAX_LINEA 256
#define RUTA_ARCHIVOS "archivos.txt"

typedef struct {
    char** textos;
    size_t longitud;
} ListaTextos;

ListaTextos obtener_textos(char* rutaArtista) {
    char linea[LONGITUD_MAX_LINEA];
    ListaTextos resultado = {NULL, 0};
    
    FILE* archivoNombres;
    char* cadenasComando[] = {"ls ", rutaArtista, "> archivos.txt"};
    char* comandoVolcarNombres = armar_cadena(cadenasComando, 3);

    if (system(comandoVolcarNombres) != 0) {
        printf("Error: Directorio no encontrado. Revisar argumento pasado.\n");
        free(comandoVolcarNombres);
        return resultado;
    }

    archivoNombres = fopen(RUTA_ARCHIVOS, "r");

    if (archivoNombres == NULL) {
        printf("Error: no se pudo abrir el archivo de nombres. Revisar argumento pasado.\n");
        free(comandoVolcarNombres);
        return resultado;
    }

    size_t i = 0;
    while (fgets(linea, LONGITUD_MAX_LINEA, archivoNombres)) {
        resultado.textos = realloc(resultado.textos, (i + 1) * sizeof(char*));
        resultado.textos[i] = malloc(sizeof(char) * (strlen(linea) + 1));
        strcpy(resultado.textos[i], linea);
        i++;
    }

    if (i == 0) {
        printf("Error: archivos.txt está vacío\n");
        free(comandoVolcarNombres);
        fclose(archivoNombres);
        return resultado;
    }

    resultado.longitud = i;
    free(comandoVolcarNombres);
    fclose(archivoNombres);
    return resultado;
}

int main() {
    char* rutaArtista = "tu_ruta"; // Reemplaza con tu ruta real
    ListaTextos lista = obtener_textos(rutaArtista);

    if (lista.textos != NULL) {
        // Utiliza la lista.textos y la lista.longitud según sea necesario
        for (size_t i = 0; i < lista.longitud; i++) {
            printf("%s", lista.textos[i]);
            free(lista.textos[i]);
        }
        free(lista.textos);
    }

    return 0;
}
