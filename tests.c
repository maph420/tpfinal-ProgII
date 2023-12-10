#include <stdio.h>
#include <assert.h>
#include "funciones.h"

void liberar_textos(char** textos) {
    
    if (textos != NULL) {
        for (int i = 0; textos[i] != NULL; i++) {
                free(textos[i]);
        }
    }
    free(textos);
}

void test_armar_cadena() {
    char* palabras1[] = {"Esto", " ", "es", " UNA ", "prueba!"};
    char* palabras2[] = {"SoloUnaPalabra"};
    //?
    char* palabras3[] = {NULL};
    char *test1, *test2, *test3;

    test1 = armar_cadena(palabras1, 5);
    assert(strcmp(test1, "Esto es UNA prueba!") == 0);
    
    test2 = armar_cadena(palabras2, 1);
    assert(strcmp(test2, "SoloUnaPalabra") == 0);
    
    test3 = armar_cadena(palabras3, 0);
    assert(strcmp(test3, "") == 0);

    free(test1);
    free(test2);
    free(test3);
    printf("-------\n-Los test de armar_cadena pasaron exitosamente.\n");
}
/*
void test_obtener_textos() {
    // Test case 1: Provide a valid directory
    char** textos1 = obtener_textos("Tests/Textos/Andres_Calamaro");
    assert(textos1 != NULL);
    assert(strcmp(textos1[0],"flaca.txt\n") == 0);
    assert(strcmp(textos1[1],"mienfermedad.txt\n") == 0);
    assert(strcmp(textos1[2],"tequieroigual.txt\n") == 0);
    
    char** textos2 = obtener_textos("Tests/Textos#Andres_Calamaro.txt");
    assert(textos2 == NULL);
   
    char** textos3 = obtener_textos("Tests/Textos/Gustavo_Cerati");
    assert(textos3 != NULL);
    assert(strcmp(textos3[0],"crimen.txt\n") == 0);
    assert(strcmp(textos3[1],"jugodeluna.txt\n") == 0);
    assert(strcmp(textos3[2],"karaoke.txt\n") == 0);

    char** textos4 = obtener_textos("Tests/Textos/Cantante1");
    assert(textos4 == NULL);
    
    liberar_textos(textos1);
    liberar_textos(textos2);
    liberar_textos(textos3);
    liberar_textos(textos4);
    
    printf("-------\n-Los test de obtener_textos pasaron\n");
}*/
void test_limpiar_texto() {
    char* result1 = limpiar_texto("Tests/archivo_a_limpiar.txt");
    assert(result1 != NULL);
    assert(strcmp(result1, "este texto va a ser limpiado menos mal") == 0);
    char* result2 = limpiar_texto("Tests/noexisto.txt");
    assert(result2 == NULL);
    
    free(result1);
    free(result2);
    printf("-------\n-Los test de limpiar_texto pasaron\n");
}
void test_recorrer_y_limpiar() {
    char** textos1 = malloc(sizeof(char*) * 4);
    // strdup reserva memoria a textos1[i] de manera dinamica, a diferencia de strcpy
    textos1[0] = strdup("texto1.txt\n");
    textos1[1] = strdup("texto2.txt\n");
    textos1[2] = strdup("texto3.txt\n");
    textos1[3] = NULL;

    char *rutaArtista = malloc(sizeof(char) * 50);
    char *nomArchDestino = malloc(sizeof(char) * 50);

    strcpy(rutaArtista, "Tests/Textos/Cantante2");
    strcpy(nomArchDestino, "Tests/salida.txt");

    recorrer_y_limpiar(textos1, rutaArtista, nomArchDestino);

    FILE* archSalida = fopen("Tests/salida.txt", "r");
    char linea[LONGITUD_MAX_LINEA];
    char** contenidoLinea = malloc(sizeof(char*) * 30);
    int i=0;

    while( fgets(linea, LONGITUD_MAX_LINEA, archSalida)) {
        contenidoLinea[i] = malloc(sizeof(char) * 50);
        strcpy(contenidoLinea[i], linea);
        i++;
    }
    contenidoLinea[i] = NULL;
    assert(strcmp(contenidoLinea[0], "este es el primer texto\n") == 0);
    assert(strcmp(contenidoLinea[1], "el que le sigue al primero es el segundo\n") == 0);
    assert(strcmp(contenidoLinea[2], "este archivo de texto es el segundo\n") == 0);
    assert(strcmp(contenidoLinea[3], "por ultimo este es el tercero\n") == 0);
    assert(strcmp(contenidoLinea[4], "este es el ultimo texto\n") == 0);
    
    printf("-------\n-Los test de recorrer_y_limpiar pasaron\n");
    liberar_textos(contenidoLinea);
    fclose(archSalida);
    free(textos1);
    free(rutaArtista);
    free(nomArchDestino);
}
int main() {
    
    test_armar_cadena();
    //test_obtener_textos();
    test_limpiar_texto();
    test_recorrer_y_limpiar();
    printf("-------\nTodos los tests se corrieron con éxito\n");

    return 0;
}