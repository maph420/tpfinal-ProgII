#include <stdio.h>
#include <assert.h>
#include "funciones.h"

void liberar_textos(ListaTextos listaTextos) {
    
    if (listaTextos.textos != NULL) {
        for (int i = 0; i < listaTextos.longitud; i++) {
                free(listaTextos.textos[i]);
                listaTextos.textos[i] = NULL;
        }
    }
    free(listaTextos.textos);
}

void test_armar_cadena() {
    char* palabras1[] = {"Esto", " ", "es", " UNA ", "prueba!"};
    char* palabras2[] = {"SoloUnaPalabra"};
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

void test_obtener_textos() {
    // Test case 1: Provide a valid directory
    ListaTextos listaTextos1 = obtener_textos("Tests/Textos/Andres_Calamaro");
    assert(listaTextos1.textos != NULL);
    assert(strcmp(listaTextos1.textos[0],"flaca.txt\n") == 0);
    assert(strcmp(listaTextos1.textos[1],"mienfermedad.txt\n") == 0);
    assert(strcmp(listaTextos1.textos[2],"tequieroigual.txt\n") == 0);
    
    ListaTextos listaTextos2 = obtener_textos("Tests/Textos#Andres_Calamaro.txt");
    assert(listaTextos2.textos == NULL);
   
    ListaTextos listaTextos3 = obtener_textos("Tests/Textos/Gustavo_Cerati");
    assert(listaTextos3.textos != NULL);
    assert(strcmp(listaTextos3.textos[0],"crimen.txt\n") == 0);
    assert(strcmp(listaTextos3.textos[1],"jugodeluna.txt\n") == 0);
    assert(strcmp(listaTextos3.textos[2],"karaoke.txt\n") == 0);

    ListaTextos listaTextos4 = obtener_textos("Tests/Textos/Cantante1");
    assert(listaTextos4.textos == NULL);
    
    // de listaTextos2 y listaTextos4 la memoria ya es liberada dentro de la funcion obtener_textos
    liberar_textos(listaTextos1);
    liberar_textos(listaTextos3);

    printf("-------\n-Los test de obtener_textos pasaron\n");
}
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

    FILE* archSalida;
    char linea[LONGITUD_MAX_LINEA];
    int i=0;

    ListaTextos listaTextosTest;
    listaTextosTest.textos = malloc(sizeof(char*) * 3);
    listaTextosTest.longitud = 3;

    ListaTextos contenidoLinea;
    contenidoLinea.textos = malloc(sizeof(char*) * 5);
    contenidoLinea.longitud = 5;

    listaTextosTest.textos[0] = malloc(sizeof(char)*LONGITUD_MAX_LINEA);
    strcpy(listaTextosTest.textos[0], "texto1.txt\n");

    listaTextosTest.textos[1] = malloc(sizeof(char)*LONGITUD_MAX_LINEA);
    strcpy(listaTextosTest.textos[1], "texto2.txt\n");

    listaTextosTest.textos[2] = malloc(sizeof(char)*LONGITUD_MAX_LINEA);
    strcpy(listaTextosTest.textos[2], "texto3.txt\n");

    char *rutaArtista = malloc(sizeof(char) * LONGITUD_NOM_ARCHIVO_MAX);
    char *nomArchDestino = malloc(sizeof(char) * LONGITUD_NOM_ARCHIVO_MAX);

    strcpy(rutaArtista, "Tests/Textos/Cantante2");
    strcpy(nomArchDestino, "Tests/salida.txt");

    // la memoria empleada en listaTextosTest es liberada en la misma funcion
    recorrer_y_limpiar(listaTextosTest, rutaArtista, nomArchDestino);
    
    archSalida = fopen("Tests/salida.txt", "r");
 
    while( fgets(linea, LONGITUD_MAX_LINEA, archSalida)) {
        contenidoLinea.textos[i] = malloc(sizeof(char) * 50);
        strcpy(contenidoLinea.textos[i], linea);
        i++;
    }
    assert(strcmp(contenidoLinea.textos[0], "este es el primer texto\n") == 0);
    assert(strcmp(contenidoLinea.textos[1], "el que le sigue al primero es el segundo\n") == 0);
    assert(strcmp(contenidoLinea.textos[2], "este archivo de texto es el segundo\n") == 0);
    assert(strcmp(contenidoLinea.textos[3], "por ultimo este es el tercero\n") == 0);
    assert(strcmp(contenidoLinea.textos[4], "este es el ultimo texto\n") == 0);
    
    printf("-------\n-Los test de recorrer_y_limpiar pasaron\n");

    fclose(archSalida);
    liberar_textos(contenidoLinea);
    free(rutaArtista);
    free(nomArchDestino);
}

int main() {
    
    test_armar_cadena();
    test_obtener_textos();
    test_limpiar_texto();
    test_recorrer_y_limpiar();
    printf("-------\nTodos los tests se corrieron con éxito\n");

    return 0;
}