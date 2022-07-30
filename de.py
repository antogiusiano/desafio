class Tablero(object):

    def __init__(self, ancho: int, alto: int):
        self.ancho = ancho
        self.alto = alto
        self._tablero = None

    @property
    def tablero(self):
        if not self._tablero:
            self._tablero = [[True for column in range(self.alto)] for row in range(self.ancho)]
        return self._tablero
    
    def dibujar_bloque(self, x: int, y: int):
        if x < 0 or y <0:
            raise IndexError(f"La combinacion de x,y:{x},{y} esta fuera de rango.")
        self.tablero[x][y] = False
    
    def obtener_celda(self, x: int, y: int):
        if x < 0 or y <0:
            raise IndexError(f"La combinacion de x,y:{x},{y} esta fuera de rango.")
        return self.tablero[x][y]

    def hay_celda_disponible(self, x: int, y: int):
            return 0<=x<self.ancho and 0<=y<self.alto and self.tablero[x][y]
        
    def copiar(self):
        return Tablero(self.ancho, self.alto)