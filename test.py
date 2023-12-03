words = "flaca no me claves tus punales por la espalda tan profundo no me duelen no me hacen mal
lejos en el centro de la tierra las raices del amor donde estaban quedaran
entre el no me olvides me deje nuestros abriles olvidados en el fondo del placard del cuarto de invitados eran tiempos dorados un pasado mejor
aunque casi me equivoco y te digo poco a poco no me mientas no me digas la verdad no te quedes callada no levantes la voz ni me pidas perdon
aunque casi te confieso que tambien he sido un perro companero
un perro ideal que aprendio a ladrar y a volver al hogar para poder comer
flaca no me claves tus punales por la espalda tan profundo no me duelen no me hacen mal
lejos en el centro de la tierra las raices del amor donde estaban quedaran
estoy vencido porque el mundo me hizo asi no puedo cambiar
soy el remedio sin receta y tu amor mi enfermedad
estoy vencido porque el cuerpo de los dos es mi debilidad
esta vez el dolor va a terminar"


n = 3  # o cualquier otro valor deseado
ngrams_dict = {}

for i in range(len(words) - n):
    key = tuple(words[i:i+n])
    value = ngrams_dict.get(key, [])
    if i + n < len(words):
        value.append(words[i + n])
    ngrams_dict[key] = value
