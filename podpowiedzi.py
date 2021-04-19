
from damerau_levenshtein import *
import re
from clp3 import clp
teksty = ('Koty to fajne zfierzęta', 'Idę na ple', 'Czego ode mnie cshceszz?')


def podpowiedzi(line_list):
    #funkcja wewnętrzna do generowania podpowiedzi
    def word_corrector(word):
        word_length = len(word)
        #tworzę lekką wersję słownika do sprawdzania - tylko słowa zaczynające się na tę samą literę oraz dłuższe/krótsze o max 2 litery od wpisanego słowa
        light_SJP = [w for w in SJP if w[0] == word[0] and abs(len(w) - word_length) <= 2]
        distances = dict()
        c = 0
        for entry in light_SJP:
            #liczona odległość edycyjna dla każdego kandydata
            distances[entry] = final_damerau(word, entry)
            # licznik obrazujęcy postępy w liczeniu
            c += 1
            #print(c)
        #kandydaci są sortowane według odległości
        sortedList = sorted(distances.items(), key=lambda x: x[1])
        #i wybieram 5 pierszwych
        mozliwe_podpowiedzi = [x for x in sortedList[:20]]
        #print(mozliwe_podpowiedzi)
        you_could_mean = dict()
        #następnie każdy jest sprawdzany, czy pojawia się na liście frekwencyjnej
        for x in mozliwe_podpowiedzi:
            waga = x[1]
            #jeśli tak to jego waga jest zwiększana
            if x[0] in lista_frekw:
                if lista_frekw[x[0]] >= 9000:
                    waga -= 0.3
                elif lista_frekw[x[0]] >= 3000:
                    waga -= 0.2
                else:
                    waga -= 0.1
            else:
                #jeśli się nie pojawia to sprowadzam go do formy podstawowej i sprawdzam znowu
                try:
                    if clp(x[0]):
                        id = clp(x[0])[0]
                        f_podst = clp.bform(id)
                        if f_podst in lista_frekw:
                            if lista_frekw[f_podst] >= 9000:
                                waga -= 0.3
                            elif lista_frekw[f_podst] >= 3000:
                                waga -= 0.2
                            else:
                                waga -= 0.1
                except:
                    print('Złapano wyjątek', x[0], id)
            you_could_mean[x[0]] = waga
        you_meant = sorted(you_could_mean.items(), key=lambda x: x[1])
        #kandydat o największej wadze (odległość edycyjna + liczba_wystąpień/10000 (z listy frekwencyjnej)
        return you_meant[0][0]

    #Tworzę słownik SJP, zajmuje to najwięcej czasu, ma 100K linijek
    SJP = SJP_maker()
    #Następnie tworzę listę frekwencyjną 2000 najczęsciej występujący słów w języku polskim
    lista_frekw = frequency_list_maker('sjp/lista_frekwencyjna_stara.txt')
    for line in line_list:
        final_answer = line
        #Linijka jest oczyszczana
        clean_line = line_cleaner(line)
        podpowiedz = ''
        for word in clean_line:
            #sprawdzam czy słowo znajduje się w SJP, lub jest znakiem nie-alfanumerycznym
            if word in SJP or not word.isalpha():
                podpowiedz += word
            #niezaleznie od wielkosci liter
            elif word.lower() in SJP:
                podpowiedz += word
            elif word.capitalize() in SJP:
                podpowiedz += word
            else:
                #jeśli słowo nie występuje w SJP to należy je poprawić
                corrected_word = word_corrector(word)
                podpowiedz += corrected_word
        print('You typed in:', line)
        if line == podpowiedz:
            print('Looks like all the words you used are in our dictionaries')
        else:
            print("I think you meant:\n", podpowiedz)
    return 0

#Funkcja tworząca liste słów z SJP
def SJP_maker():
    with open('sjp/odm.txt', 'r', encoding='utf8') as dane:
        SJP = []
        for line in dane:
            SJP.extend(words_from_line(line))
    return SJP
#Funkcja tworząca listę frekwencyjną z pliku
def frequency_list_maker(file):
    with open(file, 'r', encoding='utf8') as data:
        #w pliku jest tylko jedna linijka, stąd return od razu
        for line in data:
            c = 0
            words = re.split('[=\n ]', line)
            frequency_dict = dict()
            dict_keys = words[::2]
            dict_val = words[1::2]
            dict_values = [int(i) for i in dict_val]
            frequency_dict = dict(zip(dict_keys, dict_values))
            return frequency_dict

#Funkcja oczyszczająca linijkę
def line_cleaner(line):
    words = re.split('(\W+)', line)
    return words

def words_from_line(line):
    '''Dzieli string w miejsach gdzie występuje , lub znak nowej linii, do analizy słownika'''
    words = re.split('[,\n]', line)
    return [w.strip() for w in words if w]


print(podpowiedzi(('cchcesz cos zjesc?', 'Mam tego juz nprawde doscg', 'Przczoły to warzne zfierzęta')))
