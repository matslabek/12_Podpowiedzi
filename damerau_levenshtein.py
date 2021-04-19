import re, numpy as num
############# ODLEGLOŚC EDYCYJNA #################

#funkcja zamieniająca dwuznaki na znak pojedynczy, do sprawdzania błędów ortografinczych
def no_digraphs(word):
    x = re.sub('rz', 'ʐ', word)
    y = re.sub('ch', 'ɣ', x)
    x = re.sub('ni', 'ň', y)
    y = re.sub('ci', 'č', x)
    x = re.sub('si', 'ɕ', y)
    y = re.sub ('zi', 'ʑ', x)
    x = re.sub ('om', 'ã', x)
    return x

def damerau_levenshtein(word1, word2):

    nw1, nw2 = word1.lower(), word2.lower()
    #flaga do błędów czeskich
    czech = False

    #słownik do sprawdzania błędów ortograficznych
    orthographics = {'ż': 'ʐ', 'h': 'ɣ','ń': 'ň', 'ć': 'č', 'ś': 'š','ź': 'ʑ', 'ó': 'u', 'ą': 'ã',
                     'ʐ': 'ż', 'ɣ': 'h','ň': 'ń', 'č': 'ć', 'š': 'ś','ʑ': 'ź', 'u': 'ó', 'ã': 'ą'}
    #słownik do sprawdzania braku polskich znaków
    diacritics = {'ą': 'a', 'ę': 'e','ń': 'n', 'ć': 'c', 'ś': 's','ź': 'z', 'ż': 'z', 'ó': 'o', 'ł': 'l',
                     'a': 'ą', 'e': 'ę', 'n': 'ń', 'c': 'ć', 's': 'ś','z': 'ź', 'o': 'ó', 'l': 'ł'}

    #stworzenie początkowej macierzy
    matrix = num.zeros((len(nw1) + 1, len(nw2) + 1))
    for x in range(len(nw1) + 1):
        matrix[x][0] = x
    for y in range(len(nw2) + 1):
        matrix[0][y] = y

    #wypełnienie macierzy wartościami, w dwóch pętlach
    for x in range(1, len(nw1) + 1):
        for y in range(1, len(nw2) + 1):
            # jeżeli znaki takie same, metryka liczona według zwykłego wzoru levenshteina
            if (nw1[x - 1] == nw2[y - 1]):
                matrix[x][y] = min(
                    matrix[x-1, y]+1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] +1
                )
            #gdy znak nie są takie same
            #rozważam przypadek zamiany sąsiadujących liter("czeskie błędy"), waga 0.5
            elif (x < len(nw1) and y < len(nw2) and ((nw1[x-1] == nw2[y] and nw1[x] == nw2[y-1]) or \
            (nw1[x-1] == nw2[y-2] and nw1[x-2] == nw2[y-1]))):
                #sprawdzam flagę, jeżeli jest podniesiona, to znaczy, że dany błąd został już policzony,
                #aby go nie zdublować, przyjmuję, że znaki się zgadzają i opuszczam flagę
                if czech:
                    czech = False
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1],
                        matrix[x, y - 1] + 1
                    )
                #flaga opuszczona, błąd nie został jeszcze uwzględniony
                else:
                    #dodaje wagę 0.5 i podnoszę flagę
                    czech = True
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 0.5,
                        matrix[x, y - 1] + 1
                    )

            # przypadek braku znaku diakrytycznego, waga 0.2
            # sprawdzam, czy litery występują w słowniku diakrytyków i do siebie pasują
            elif (nw1[x-1] in diacritics and nw2[y-1] in diacritics and diacritics[nw1[x - 1]] == nw2[y - 1]):
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 0.2,
                        matrix[x, y - 1] + 1
                    )
            # przypadek błędów ortograficznych, waga 0.5
            # sprawdzam, czy obie litery występują w słowniku ortograficznym i do siebie pasują
            elif (nw1[x -1] in orthographics and nw2[y-1] in orthographics and orthographics[nw1[x-1]] == nw2[y-1]):
                    matrix[x, y] = min(
                        matrix[x-1, y]+1,
                        matrix[x-1, y-1] + 0.5,
                        matrix[x, y-1]+1
                    )
            # przypadek bazowy - litery się nie zgadzają - to znów zwykła metryka levenshteina
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    # pomocniczne wypisanie macierzy
    # print_matrix(matrix, len(nw1), len(nw2))
    # odległość to skrajna komórka w macierzy
    distance = (matrix[len(nw1),len(nw2)])
    return distance

# odległość damerau liczę dla dwóch przypadków, z dwuznakami oraz bez nich
def final_damerau(w1, w2):
    x = damerau_levenshtein(w1, w2)
    y = damerau_levenshtein(no_digraphs(w1), w2)
    #zwracam mniejszą z dwóch odległości
    return min(x,y)

# pomocnicze wypisanie macierzy ma ekran
def print_matrix(matrix, a, b):
    for x in range(a + 1):
        for y in range(b + 1):
            print((matrix[x][y]), end=" ")
        print()