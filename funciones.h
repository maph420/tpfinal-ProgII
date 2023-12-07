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

char* armar_cadena(char* palabras[], int cantPalabras);
char** obtener_textos(char* rutaArtista);
char* limpiar_texto(char* nomTexto);
int recorrer_y_limpiar(char** textos, char* rutaArtista, char* nomArchivoDestino);
int llamar_python(char* args);

#endif