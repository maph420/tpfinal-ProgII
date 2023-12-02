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
char** obtener_textos(char* rutaArtista) {
    char linea[LONGITUD_MAX_LINEA], comandoVolcarNombres[50];
    char** textos = malloc(sizeof(char *)*10);
    int i=0;
    FILE* archivoNombres;

    strcpy(comandoVolcarNombres, "ls ");
    strcat(comandoVolcarNombres, rutaArtista);
    strcat(comandoVolcarNombres, " > archivos.txt");
    system(comandoVolcarNombres);

    archivoNombres = fopen("archivos.txt", "r");
    
    if (archivoNombres == NULL) {
        printf("Error al abrir el archivo. Revisar argumento pasado.\n");
        exit(-1);
    }
    
    while( fgets(linea, LONGITUD_MAX_LINEA, archivoNombres)) {
        textos[i] = malloc(sizeof(char)*50);
        strcpy(textos[i], linea);
        i++;
    }
    // aseguramos de colocar una marca que indique el fin de la lista
    textos[i] = NULL;
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
        exit(-1);
    }
    while ( (c = fgetc(archivoEntrada)) != EOF) {

        if (c >= 'A' && c <= 'Z') {
            resultado[i++] = tolower(c);
            puntoEncontrado = 0;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        }
        
        else if ((c >= 'a' && c <= 'z')) {
            resultado[i++] = c;
            puntoEncontrado = 0;
            espacioEncontrado = 0;
            enterEncontrado = 0;
        }

        else if ((c>= '0' && c<= '9')) {
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
    char comandoLlamadaPython[40];
    strcpy(comandoLlamadaPython, "python3 main.py ");
    strcat(comandoLlamadaPython, args);
    system(comandoLlamadaPython);
}

int main(int argc, char** argv) {

    char rutaArtista[100], nomArchivoDestino[100], rutaTexto[100], *textoProcesado;
    FILE* archivoDestino;

    if (argc != 2) {
        printf("Numero de argumentos incorrecta.\nUso: ./main nombre_de_artista\n");
        return 0;
    }
    
    strcpy(rutaArtista, RUTA_A_LEER);
    strcat(rutaArtista, argv[1]);

    strcpy(nomArchivoDestino, RUTA_A_ESCRIBIR);
    strcat(nomArchivoDestino, argv[1]);
    strcat(nomArchivoDestino, ".txt");
    archivoDestino = fopen(nomArchivoDestino, "w");

    if (archivoDestino == NULL) {
        printf("Hubo un error al abrir el archivo\n");
        return -1;
    }

    char** textos = obtener_textos(rutaArtista);
    int i=0;
    while (textos[i] != NULL) {
        strcpy(rutaTexto, rutaArtista);
        strcat(rutaTexto, "/");
        strcat(rutaTexto, textos[i]);

        rutaTexto[strlen(rutaTexto)-1] = '\0';
        textoProcesado = procesar_texto(rutaTexto);
        fputs(textoProcesado, archivoDestino);
        fputc('\n', archivoDestino);

        free(textoProcesado);
        free(textos[i]);
        i++;
    }
    free(textos);
    fclose(archivoDestino);

    llamar_python(argv[1]);
    
    return 0;
}