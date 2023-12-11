#include "funciones.h"

char* armar_cadena(char* palabras[], int cantPalabras) {
    char* comando = malloc(sizeof(char)*LONGITUD_MAX_COMANDO);
    // inicializar la cadena comando
    comando[0] = '\0';
    for (int i=0; i<cantPalabras; i++) {
        strcat(comando, palabras[i]);
    }
    return comando;
}

ListaTextos obtener_textos(char* rutaArtista) {
    int i=0;
    char linea[LONGITUD_MAX_LINEA];
    ListaTextos resultado;
    resultado.textos = NULL;
    resultado.longitud = 0;
    
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
        fclose(archivoNombres);
        return resultado;
    }

    resultado.textos = malloc(sizeof(char*) * 30);
    while (fgets(linea, LONGITUD_MAX_LINEA, archivoNombres)) {
        resultado.textos[i] = malloc(sizeof(char)*(strlen(linea)+1));
        strcpy(resultado.textos[i], linea);
        i++;
    }

    if (i == 0) {
        printf("Error: archivos.txt está vacío\n");
        free(comandoVolcarNombres);
        fclose(archivoNombres);
        free(resultado.textos);
        resultado.textos = NULL;
        resultado.longitud = 0;
        return resultado;
    }

    resultado.longitud = i;
    free(comandoVolcarNombres);
    fclose(archivoNombres);
    return resultado;
}

char* limpiar_texto(char* nomTexto) {
    char c, resultado[CANT_CARACTERES_MAX];
    int i = 0, estado = 0;
    /*
    estado 0 -> el caracter anterior fue un punto/enter o no hay caracter anterior
    estado 1 -> el caracter anterior fue alfanumerico/digito
    estado 2 -> el caracter anterior fue un espacio
    */
    FILE* archivoEntrada;
    archivoEntrada = fopen(nomTexto, "r");

    if (archivoEntrada == NULL) {
        printf("Hubo un problema al abrir el archivo %s\n", nomTexto);
        return NULL;
    }
    while ((c = fgetc(archivoEntrada)) != EOF) {
        if (isalpha(c) || isdigit(c)) {
            resultado[i] = tolower(c);
            estado = 1;
            i++;
        } else if (c == ' ') {
            if (estado == 1) {
                resultado[i] = c;
                i++;
            }
            estado = 2;
        } else if (c == '.') {
            resultado[i] = '\n';
            estado = 0;
            i++;
        } else if (c == '\n') {
            if (estado == 1) {
                resultado[i] = ' ';
                i++;
            }
            estado = 0;
        }
    }
    // modificamos el ultimo caracter de la cadena (un enter) por un terminador
    if (i>1) {
        resultado[i-1]='\0';
    }
    
    // copiamos el resultado en un puntero a char, para retornarlo al scope del main
    char* resultadoCopia = malloc((sizeof(char)*i)+1);
    strcpy(resultadoCopia, resultado);

    fclose(archivoEntrada);
    return resultadoCopia;
}

int recorrer_y_limpiar(ListaTextos listaTextos, char* rutaArtista, char* nomArchivoDestino) {
    char *textoLimpio;
    FILE* archivoDestino = fopen(nomArchivoDestino, "w");
    
    if (archivoDestino == NULL) {
        printf("Error: No se pudo abrir el archivo de destino\n");
        return -1;
    }

    for (int i=0; i < listaTextos.longitud; i++) {
        char* cadenasRutaTexto[] = {rutaArtista, "/", listaTextos.textos[i]};
        char* rutaTexto = armar_cadena(cadenasRutaTexto, 3);
        // reemplazamos el "enter" al final de cada oracion por un terminador
        rutaTexto[strlen(rutaTexto)-1] = '\0';

        textoLimpio = limpiar_texto(rutaTexto);

        if (textoLimpio != NULL) {
            fputs(textoLimpio, archivoDestino);
            fputc('\n', archivoDestino);
            free(textoLimpio);
        }
        free(rutaTexto);
        free(listaTextos.textos[i]);
        listaTextos.textos[i] = NULL;
    }
    free(listaTextos.textos);
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
