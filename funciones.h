#ifndef FUNCIONES_H
#define FUNCIONES_H
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>
#include<assert.h>

//macros
#define RUTA_A_LEER "Textos/"
#define RUTA_A_ESCRIBIR "Entradas/"
#define RUTA_ARCHIVOS "archivos.txt"
#define CANT_CARACTERES_MAX 2000
#define LONGITUD_MAX_LINEA 255
#define LONGITUD_MAX_COMANDO 100
#define LONGITUD_NOM_ARCHIVO_MAX 50

typedef struct {
    char** textos;
    int longitud;
} ListaTextos;

char* armar_cadena(char* palabras[], int cantPalabras);
ListaTextos obtener_textos(char* rutaArtista);
char* limpiar_texto(char* nomTexto);
int recorrer_y_limpiar(ListaTextos listaTextos, char* rutaArtista, char* nomArchivoDestino);
int llamar_python(char* args);

#endif