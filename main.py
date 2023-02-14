import pandas as pd
import random
import json
arr = []
matriz = []  # primer elemnto son las x, despues las yWALL
matriz_word_init = []
words = []
WALL = "&"
SIZE = 12
EMPTY = ""
nWORDS = 5000
used_words = []
resp = []  # array de json donde estan todas las palabras


def cargar_palabras():  # carga 5000 palabras en arr. [english, spanish]
    date = pd.read_csv('./data/all_word.csv')
    global arr
    arr = date.values


def iniciar_matriz():  # inicia la matriz de SIZExSIZE en ""
    global matriz
    global used_words
    global matriz_word_init
    matriz = [[EMPTY for x in range(SIZE)] for y in range(SIZE)]
    matriz_word_init = [[False for x in range(SIZE)] for y in range(SIZE)]
    used_words = [False for i in range(nWORDS)]


def n_empty():  # cantidad de vacios
    cant = 0
    for x in range(SIZE):
        for y in range(SIZE):
            if matriz[x][y] == EMPTY:
                cant += 1
    return cant


def remove_empty():  # quita los vacios
    global matriz
    for x in range(SIZE):
        for y in range(SIZE):
           if matriz[x][y] == EMPTY:
               matriz[x][y] = WALL


def in_borderx(x):
      if x == SIZE - 1:
           return True
      else:
           return False
       
def in_bordery(y):
      if y == SIZE - 1:
           return True
      else:
           return False

def word_fit(id_word, x, y,horizontal): #averigua si la palabra cabe. Y tiene un espacio despues de ella

    dx = 0
    dy = 0
    if horizontal:
        dx = 1
    else:
        dy = 1

    word = arr[id_word][0]
    
    #si la primera posicion se a usado retorna false
    if matriz_word_init[x][y]:
         return False
    
    # si alguna letra se salio de la matriz o si la letra no esta vacia pero la letra no es igual a la que estaba puesta retorna falso
    for i in range(len(word)):
        if  (x + dx*i > SIZE - 1 or  y + dy*i > SIZE - 1) or matriz[x + dx*i ][y + dy*i ] != EMPTY and  matriz[ x + dx*i ][ y + dy*i ] != word[i]:
            return False

    #sino esta en el borde deberia haber un espacio en blanco al final o un muro
    if horizontal and not in_borderx(x + dx*(len(word)-1)) and ( matriz[x + dx*len(word)][y] not in [EMPTY,WALL] ):
        return False
    if not horizontal and not in_bordery(y + dy*(len(word)-1)) and (matriz[x][y + dy*len(word)]  not in [EMPTY,WALL]  ):
        return False

    # if horizontal and x + dx*len(word) > SIZE or not horizontal and y + dy*len(word) > SIZE:
    #     return False

    return True

def put_word(id_word, x, y,horizontal): #coloca la palabra y una marca despues de ella para marcar el fin de la palabra

    global matriz
    global words
    global used_words
    dx = 0
    dy = 0
    if horizontal:
        dx = 1
    else:
        dy = 1

    matriz_word_init[x][y] = True
    
    # coloca la palabra en matriz
    word = arr[id_word][0]
    question = arr[id_word][1]

    for i in range(len(word)):
        matriz[x + dx*i ][y + dy*i ] = word[i]

    # coloca WALL al final de la palabra si no esta en el borde
    xf = x + dx*len(word)
    yf = y + dy*len(word)
    if xf in range(SIZE) and yf in range(SIZE):
        matriz[xf][yf] = WALL

    used_words[id_word] = True

    resp.append({
        'word': word,
        'question': question,
        'orientacion': "H" if horizontal else 'V',
        'cord': {
            'x': x,
            'y': y
        }
    })


def find_pos_word(id_word):  # buscando una posicion para la palabra x
    for y in range(SIZE):
        for x in range(SIZE):
            if word_fit(id_word, x, y,True):
                    put_word(id_word, x, y,True)
                    return True
            if word_fit(id_word, x, y,False):
                    put_word(id_word, x, y,False)
                    return True
    return False


def to_file():
    print('To file')
    aux = sorted(resp, key=lambda x: (x['cord']['x'], x['cord']['y']))  # ordenando por cordenadas
    for i, elem in enumerate(aux):
        elem['n'] = i

    with open('./resp/resp.json', "w") as file:
        json.dump(aux, file)


def llena_puzzle():  # buscando palabras que quepan en el cruzigrama hasta que no haya mas espacio o queden n espacios
    global arr
    while n_empty() > 2:
        id_word = random.randint(0, nWORDS-1)
        if not used_words[id_word]:
            find_pos_word(id_word)
    remove_empty()
    to_file()


if __name__ == "__main__":
    cargar_palabras()
    iniciar_matriz()
    llena_puzzle()
