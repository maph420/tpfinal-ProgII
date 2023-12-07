#include "funciones.h"

char* armar_cadena(char* palabras[], int cantPalabras) {
    char* comando = malloc(sizeof(char)*100);
    // inicializar la cadena comando
    comando[0] = '\0';
    for (int i=0; i<cantPalabras; i++) {
        strcat(comando, palabras[i]);
    }
    return comando;
}

char** obtener_textos(char* rutaArtista) {
    char linea[LONGITUD_MAX_LINEA];
    char** textos = malloc(sizeof(char *)*30);
    int i=0;
    FILE* archivoNombres;

    char* cadenasComando[] = {"ls ", rutaArtista, "> archivos.txt"};
    char* comandoVolcarNombres = armar_cadena(cadenasComando, 3);

    // system retorna algo distinto de 0 si falla el comando
    if (system(comandoVolcarNombres) != 0) {
        printf("Error: Directorio no encontrado. Revisar argumento pasado. \n");
        free(textos);
        free(comandoVolcarNombres);
        return NULL;
    }

    archivoNombres = fopen(RUTA_ARCHIVOS, "r");
    
    if (archivoNombres == NULL) {
        free(textos);
        free(comandoVolcarNombres);
        fclose(archivoNombres);
        printf("Error: no se pudo abrir el archivo de nombres. Revisar argumento pasado.\n");
        return NULL;
    }
    
    while( fgets(linea, LONGITUD_MAX_LINEA, archivoNombres)) {
        textos[i] = malloc(sizeof(char)*50);
        strcpy(textos[i], linea);
        i++;
    }
    if (i==0) {
        printf("Error: archivos.txt esta vacio\n");
        free(textos);
        free(comandoVolcarNombres);
        fclose(archivoNombres);
        return NULL;
    }
    // aseguramos de colocar una marca que indique el fin de la lista
    textos[i] = NULL;
    free(comandoVolcarNombres);
    fclose(archivoNombres);
    return textos;
}   

char* limpiar_texto(char* nomTexto) {
    char c, resultado[CANT_CARACTERES_MAX];
    int i = 0, puntoEncontrado = 0, espacioEncontrado = 0, enterEncontrado = 0;

    FILE* archivoEntrada;
    archivoEntrada = fopen(nomTexto, "r");

    if (archivoEntrada == NULL) {
        printf("Hubo un problema al abrir el archivo %s\n", nomTexto);
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
        resultado[i]='\0';
    }
    
    // copiamos el resultado en un puntero a char, para retornarlo al scope del main
    char* resultadoCopia = malloc((sizeof(char)*i)+1);
    strcpy(resultadoCopia, resultado);

    fclose(archivoEntrada);
    return resultadoCopia;
}

int recorrer_y_limpiar(char** textos, char* rutaArtista, char* nomArchivoDestino) {
    char *textoLimpio;
    int i=0;
    FILE* archivoDestino = fopen(nomArchivoDestino, "w");
    
    if (archivoDestino == NULL) {
        printf("Error: No se pudo abrir el archivo de destino\n");
        return -1;
    }
    while (textos[i] != NULL) {
        char* cadenasRutaTexto[] = {rutaArtista, "/", textos[i]};
        char* rutaTexto = armar_cadena(cadenasRutaTexto, 3);
        // reemplazamos el "enter" al final de cada oracion por un terminador
        rutaTexto[strlen(rutaTexto)-1] = '\0';

        textoLimpio = limpiar_texto(rutaTexto);
        if (textoLimpio == NULL) {
            return -2;
        }
        fputs(textoLimpio, archivoDestino);
        fputc('\n', archivoDestino);

        free(rutaTexto);
        free(textoLimpio);
        free(textos[i]);
        i++;
    }
    fclose(archivoDestino);
    return 0;
}

int llamar_python(char* args) {
    char* cadenasComando[] = {"python3 main.py ", args};
    char* comandoLlamadaPython = armar_cadena(cadenasComando, 2);
    if (system(comandoLlamadaPython) != 0) {
        return -1;
    }
    free(comandoLlamadaPython);
    return 0;
}
