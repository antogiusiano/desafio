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


class Serpiente(object):
    movimientos = {"R": [1, 0], "D": [0, 1], "L": [-1, 0], "U": [0, -1]}

    def __init__(self, serpiente: list):
        self.serpiente = serpiente

    def det(self, tablero: Tablero):
        nuevo_tablero = self.celdas_disponibles(tablero)
        movimientos = self.posibles_movimientos()
        det = []
        for m in movimientos:
            try:
                if nuevo_tablero.obtener_celda(*m[1]):
                    det.append(m[0])
            except IndexError:
                pass
        return det

    def posibles_movimientos(self):
        cabeza = self.serpiente[0]
        return [ (k, [cabeza[0]+v[0], cabeza[1] +v[1]]) 
                    for k,v in Serpiente.movimientos.items()]


    def celdas_disponibles(self, tablero: Tablero):
        nuevo_tablero = tablero.copiar()
        for i in range(len(self.serpiente)-1):
            body = self.serpiente[i]
            nuevo_tablero.dibujar_bloque(*body)
        return nuevo_tablero
    
    def movimiento_serpiente(self, direccion: str, tablero: Tablero):
        if direccion not in Serpiente.movimientos.keys():
            raise Exception(f"Movimiento \"{direccion}\" desconocido.")
        if direccion not in self.det(tablero):
            raise Exception(f"No puede moverse \"{direccion}\" hay algo que te bloquea")
        cabeza = self.serpiente[0]
        mover = Serpiente.movimientos[direccion]
        self.serpiente = [[cabeza[0] + mover[0], cabeza[1] + mover[1]]] + self.serpiente[:-1]
