import pandas as pd
import random

arr = []
matriz = [] #primer elemnto son las x, despues las yWALL
words = []
words_horizontal = []
words_vertical = []
WALL = "&"
SIZE = 12
EMPTY = ""
nWORDS = 5000
used_words = []

def cargar_palabras(): #carga 5000 palabras en arr. [english, spanish]
    date = pd.read_csv('all_word.csv')
    global arr
    arr = date.values
    
def iniciar_matriz(): #inicia la matriz de SIZExSIZE en ""
    global matriz
    global used_words
    matriz = [[EMPTY for x in range(SIZE)] for y in range(SIZE)]
    used_words = [ False for i in range(nWORDS)]
    
def n_empty(): #cantidad de vacios
    cant = 0
    for x in range(SIZE):
        for y in range(SIZE):
            if matriz[x][y] == EMPTY:
                cant+=1
    return cant

def remove_empty(): #quita los vacios
    global matriz
    for x in range(SIZE):
        for y in range(SIZE):
           if matriz[x][y] == EMPTY:
               matriz[x][y] = WALL

def word_fit(id_word,x,y,horizontal): #averigua si la palabra cabe. Y tiene un espacio despues de ella
    
    dx = 0
    dy = 0
    if horizontal:
        dx=1
    else:
        dy = 1
        
    word = arr[id_word][0]
        
    for i in range(len(word)):
        if  (x + dx*i > 11 or  y + dy*i > 11) or matriz[ x + dx*i ][ y + dy*i ] != EMPTY and  matriz[ x + dx*i ][ y + dy*i ] != word[i]:
            return False
    
    if horizontal and x + dx*len(word) > SIZE or not horizontal and y + dy*len(word) > SIZE:
        return False  
    
    return True

def put_word(id_word,x,y,horizontal): #coloca la palabra y una marca despues de ella para marcar el fin de la palabra
    
    global matriz
    global words
    global used_words
    dx = 0
    dy = 0
    if horizontal:
        dx=1
    else:
        dy = 1
    
    #coloca la palabra en matriz
    word = arr[id_word][0]
    for i in range(len(word)):
        matriz[ x + dx*i ][ y + dy*i ] = word[i]
        
    #coloca WALL al final de la palabra si no esta en el borde
    xf = x + dx*len(word)
    yf = y + dy*len(word)
    if xf in range(SIZE) and yf in range(SIZE):
        matriz[xf][yf] = WALL
        
    used_words[id_word] = True
        
    if horizontal:
        words_horizontal.append(id_word)
    else:
        words_vertical.append(id_word)

def find_pos_word(id_word): #buscando una posicion para la palabra x
    for y in range(SIZE):
        for x in range(SIZE):
            if word_fit(id_word,x,y,True):
                    put_word(id_word,x,y,True)
                    return True
            if word_fit(id_word,x,y,False):
                    put_word(id_word,x,y,False)
                    return True
    return False
     
def llena_puzzle(): #buscando palabras que quepan en el cruzigrama hasta que no haya mas espacio o queden n espacios
    global arr
    while n_empty() > 2 :
        id_word = random.randint(0,nWORDS-1)
        find_pos_word(id_word)
    remove_empty()
    
if __name__ == "__main__":
    cargar_palabras()
    iniciar_matriz()
    llena_puzzle()