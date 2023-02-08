import pandas as pd

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

#carga 5000 palabras en arr. [english, spanish]
def cargar_palabras():
    date = pd.read_csv('all_word.csv')
    global arr
    arr = date.values
    
#inicia la matriz de SIZExSIZE en ""
def iniciar_matriz():
    global matriz
    global used_words
    matriz = [[EMPTY for x in range(SIZE)] for y in range(SIZE)]
    used_words = [ False for i in range(nWORDS)]
    
#cantidad de vacios
def n_empty():
    cant = 0
    for x in range(SIZE):
        for y in range(SIZE):
            if matriz[x][y] == EMPTY:
                cant+=1
    return cant

#quita los vacios
def remove_empty():
    global matriz
    for x in range(SIZE):
        for y in range(SIZE):
           if matriz[x][y] == EMPTY:
               matriz[x][y] = WALL

#averigua si la palabra cabe. Y tiene un espacio despues de ella
def word_fit(id_word,x,y,horizontal):
    
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

#coloca la palabra y una marca despues de ella para marcar el fin de la palabra
def put_word(id_word,x,y,horizontal):
    
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

#buscando una posicion para la palabra x
def find_pos_word(id_word):
    for y in range(SIZE):
        for x in range(SIZE):
            if word_fit(id_word,x,y,True):
                    put_word(id_word,x,y,True)
                    return True
            if word_fit(id_word,x,y,False):
                    put_word(id_word,x,y,False)
                    return True
    return False
     
#buscando palabras que quepan en el cruzigrama hasta que no haya mas espacio o queden n espacios                
def llena_puzzle():
    global arr
    for id_word in range(nWORDS):
    # for id_word in len(arr):
        if find_pos_word(id_word):
            empty_spaces = n_empty()
            if empty_spaces < 3:
                remove_empty()
                print(n_empty())
                return
                    
  
    
if __name__ == "__main__":
    cargar_palabras()
    iniciar_matriz()
    llena_puzzle()