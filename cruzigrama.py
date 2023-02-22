import pandas as pd
import random
import json


class Cruzigrama:
    
    WALL = "&"
    EMPTY = ""
    SIZE = 12
    nWORDS = 5000
        
    def __init__(self):
        self.resp = []
        self.arr = pd.read_csv('./data/all_word.csv').values    # carga 5000 palabras en arr. [english, spanish] 
        self.matriz = [[  {'letra':self.EMPTY, 'begin': False} for x in range(self.SIZE)] for y in range(self.SIZE) ]
        self.used_words = [False for i in range(self.nWORDS)]   
    
    def n_empty(self):  
        return sum(1 for x in range(self.SIZE) for y in range(self.SIZE) if self.matriz[x][y]['letra'] == self.EMPTY)
    
    def remove_empty(self):  # quita los vacios
        self.matriz = [[ {'letra': self.WALL, 'begin': letra['begin']} if letra['letra'] == self.EMPTY else letra for y, letra in enumerate(fila)] for x, fila in enumerate( self.matriz)]
                
    def in_borderx(self,x):
      return x == self.SIZE - 1 

    def in_bordery(self,y):
         return y == self.SIZE - 1
       
    def word_fit(self,id_word, x, y,horizontal): #averigua si la palabra cabe. Y tiene un espacio despues de ella
        
        if horizontal:
            dx = 1
            dy = 0
        else:
            dx = 0
            dy = 1

        word = self.arr[id_word][0]
        
        #si la primera posicion se a usado retorna false
        if self.matriz[x][y]['begin']:
            return False
        
        # si alguna letra se salio de la matriz o si la letra no esta vacia pero la letra no es igual a la que estaba puesta retorna falso
        for i in range(len(word)):
            if  (x + dx*i > self.SIZE - 1 or  y + dy*i > self.SIZE - 1) or self.matriz[x + dx*i ][y + dy*i ]['letra'] != self.EMPTY and  self.matriz[ x + dx*i ][ y + dy*i ]['letra'] != word[i]:
                return False

        #sino esta en el borde deberia haber un espacio en blanco al final o un muro
        if horizontal and not self.in_borderx(x + dx*(len(word)-1)) and ( self.matriz[x + dx*len(word)][y]['letra'] not in [self.EMPTY,self.WALL] ):
            return False
        if not horizontal and not self.in_bordery(y + dy*(len(word)-1)) and (self.matriz[x][y + dy*len(word)]['letra']  not in [self.EMPTY,self.WALL]  ):
            return False

        # if horizontal and x + dx*len(word) > SIZE or not horizontal and y + dy*len(word) > SIZE:
        #     return False

        return True
    
    def put_word(self,id_word, x, y,horizontal): #coloca la palabra y una marca despues de ella para marcar el fin de la palabra

        if horizontal:
            dx = 1
            dy = 0
            
        else:
            dy = 1
            dx = 0

        self.matriz[x][y]['begin'] = True
        
        # coloca la palabra en matriz
        word = self.arr[id_word][0]
        question = self.arr[id_word][1]

        for i in range(len(word)):
            self.matriz[x + dx*i ][y + dy*i ]['letra'] = word[i]

        # coloca WALL al final de la palabra si no esta en el borde
        xf = x + dx*len(word)
        yf = y + dy*len(word)
        if xf in range(self.SIZE) and yf in range(self.SIZE):
            self.matriz[xf][yf]['letra'] = self.WALL

        self.used_words[id_word] = True

        self.resp.append({
            'word': word,
            'question': question,
            'orientacion': "H" if horizontal else 'V',
            'cord': {
                'x': x,
                'y': y
            }
        })
        
    def find_pos_word(self, id_word):  # buscando una posicion para la palabra x
     for y in range(self.SIZE):
        for x in range(self.SIZE):
            if self.word_fit(id_word, x, y,True):
                    self.put_word(id_word, x, y,True)
                    return True
            if self.word_fit(id_word, x, y,False):
                    self.put_word(id_word, x, y,False)
                    return True
     return False

    def to_file(self):
        print('To file')
        aux = sorted(self.resp, key=lambda x: (x['cord']['x'], x['cord']['y']))  # ordenando por cordenadas
        for i, elem in enumerate(aux):
            elem['n'] = i                                                        # colocandole un numero a las preguntas

        with open('./resp/resp.json', "w") as file:
            json.dump(aux, file)
            
    def sort_resp(self):
         aux = sorted(self.resp, key=lambda x: (x['cord']['x'], x['cord']['y']))  # ordenando por cordenadas
         for i, elem in enumerate(aux):
            elem['n'] = i
         return aux

    def llena_puzzle(self):  # buscando palabras que quepan en el cruzigrama hasta que no haya mas espacio o queden n espacios
        while self.n_empty() > 2:
            id_word = random.randint(0, self.nWORDS-1)
            if not self.used_words[id_word]:
                self.find_pos_word(id_word)
        self.remove_empty()
        # self.to_file()
        respuesta = self.sort_resp()
        print(respuesta)
        print('--------')
        return respuesta
        
        

 
