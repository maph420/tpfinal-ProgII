def word_occurrence_dict(listaPals):
    ocurrencias = {}
    i=0
    palIzq = ""
    palDer = ""
    for word in listaPals:
        if i>0:
            palIzq = listaPals[i - 1]
       
        if i < len(listaPals)-1:
            palDer = listaPals[i + 1]
       
        if word not in ocurrencias:
            ocurrencias[word] = ({}, {})

        if palIzq != "":
            if palIzq not in ocurrencias[word][0]:
                ocurrencias[word][0][palIzq] = 1
            else:
                ocurrencias[word][0][palIzq] += 1
        if palDer != "":
            if palDer not in ocurrencias[word][1]:
                ocurrencias[word][1][palDer] = 1
            else:
                ocurrencias[word][1][palDer] += 1
        i+=1
    return ocurrencias

# Example usage:
str = "la indomita luz se hizo carne en mi y lo deje todo por esta soledad y leo revistas en la tempestad hice el sacrificio abrace la cruz al amanecer rezo rezo rezo rezo por vos mori sin morir y me abrace al dolor y lo deje todo por esta soledad"
word_list = str.split()
result = word_occurrence_dict(word_list)
for key, val in result.items():
    print(key,"->",val)

