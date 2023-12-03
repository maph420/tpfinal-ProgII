//librerias
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>

//macros
#define RUTA_A_LEER "Textos/"
#define RUTA_A_ESCRIBIR "Entradas/"
#define CANT_CARACTERES_MAX 2000
#define LONGITUD_MAX_LINEA 255

//funciones
char* armar_cadena(char* palabras[], int cantPalabras) {
    char* comando = malloc(sizeof(char)*50);
    comando[0] = '\0';
    for (int i=0; i<cantPalabras; i++) {
        strcat(comando, palabras[i]);
    }
    return comando;
}

char** obtener_textos(char* rutaArtista) {
    char linea[LONGITUD_MAX_LINEA];
    char** textos = malloc(sizeof(char *)*10);
    int i=0;
    FILE* archivoNombres;

    char* cadenasComando[] = {"ls ", rutaArtista, "> archivos.txt"};
    char* comandoVolcarNombres = armar_cadena(cadenasComando, 3);

    // system retorna algo distinto de 0 si falla el comando
    if (system(comandoVolcarNombres) != 0) {
        printf("Directorio no encontrado. \n");
        return NULL;
    }

    archivoNombres = fopen("archivos.txt", "r");
    
    if (archivoNombres == NULL) {
        printf("Error al abrir el archivo. Revisar argumento pasado.\n");
        return NULL;
    }
    
    while( fgets(linea, LONGITUD_MAX_LINEA, archivoNombres)) {
        textos[i] = malloc(sizeof(char)*50);
        strcpy(textos[i], linea);
        i++;
    }
    // aseguramos de colocar una marca que indique el fin de la lista
    textos[i] = NULL;
    free(comandoVolcarNombres);
    fclose(archivoNombres);
    return textos;
}

char* procesar_texto(char* nomTexto) {
    char c, resultado[CANT_CARACTERES_MAX];
    int i = 0, puntoEncontrado = 0, espacioEncontrado = 0, enterEncontrado = 0;

    FILE* archivoEntrada;
    archivoEntrada = fopen(nomTexto, "r");

    if (archivoEntrada == NULL) {
        printf("Hubo un problema al abrir el archivo\n");
        return NULL;
    }
    while ( (c = fgetc(archivoEntrada)) != EOF) {

        if (c >= 'A' && c <= 'Z') {
            resultado[i++] = tolower(c);
            puntoEncontrado = 0;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        }
        
        else if ((c >= 'a' && c <= 'z') || (c>= '0' && c<= '9')) {
            resultado[i++] = c;
            puntoEncontrado = 0;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        } 
        else if (c == ' ' && !espacioEncontrado && !puntoEncontrado && !enterEncontrado) {
            resultado[i++] = c;
            espacioEncontrado = 1;
            enterEncontrado = 0;
            puntoEncontrado=0;
        }

        else if (c == '.') {
            resultado[i++] = '\n';
            puntoEncontrado = 1;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        }

        else if (c == '\n' && !puntoEncontrado && !enterEncontrado && !espacioEncontrado) {
            resultado[i++] = ' ';
            enterEncontrado = 1;
            puntoEncontrado = 0;
            espacioEncontrado = 0;
        }
    }
    // nos aseguramos de agregar terminador al final de la cadena
    if (i>1) {
        resultado[i-1]='\0';
    }
    
    // copiamos el resultado en un puntero a char, para retornarlo al scope del main
    char* resultadoCopia = malloc((sizeof(char)*i)+1);
    strcpy(resultadoCopia, resultado);

    fclose(archivoEntrada);
    return resultadoCopia;
}

void llamar_python(char* args) {
    char* cadenasComando[] = {"python3 main.py ", args};
    char* comandoLlamadaPython = armar_cadena(cadenasComando, 2);
    system(comandoLlamadaPython);
    free(comandoLlamadaPython);
}

int main(int argc, char** argv) {
    int i=0;
    char *textoProcesado;
    FILE* archivoDestino;

    if (argc != 2) {
        printf("Numero de argumentos incorrecta.\nUso: ./main nombre_de_artista\n");
        return 0;
    }
    char* cadenasRutaArtista[] = {RUTA_A_LEER, argv[1]};
    char* rutaArtista = armar_cadena(cadenasRutaArtista, 2);

    char* cadenasArchDest[] = {RUTA_A_ESCRIBIR, argv[1], ".txt"};
    char* nomArchivoDestino = armar_cadena(cadenasArchDest, 3);
    
    archivoDestino = fopen(nomArchivoDestino, "w");
    
    if (archivoDestino == NULL) {
        printf("Hubo un error al abrir el archivo\n");
        return -1;
    }

    char** textos = obtener_textos(rutaArtista);
    if (textos == NULL) {
        return -1;
    }

    while (textos[i] != NULL) {
        char* cadenasRutaTexto[] = {rutaArtista, "/", textos[i]};
        char* rutaTexto = armar_cadena(cadenasRutaTexto, 3);
        rutaTexto[strlen(rutaTexto)-1] = '\0';

        textoProcesado = procesar_texto(rutaTexto);
        if (textoProcesado == NULL) {
            return -1;
        }
        fputs(textoProcesado, archivoDestino);
        fputc('\n', archivoDestino);

        free(rutaTexto);
        free(textoProcesado);
        free(textos[i]);
        i++;
    }
    free(textos);
    free(rutaArtista);
    free(nomArchivoDestino);
    fclose(archivoDestino);

    llamar_python(argv[1]);
    
    return 0;
}