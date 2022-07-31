import unittest


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




class Juego(object):

    def __init__(self, tablero: list, serpiente: list):
        self.tablero = Tablero(*tablero)
        self.serpiente = Serpiente(serpiente)

    def movimiento_serpiente(self, direccion):
        self.serpiente.movimiento_serpiente(direccion, self.tablero)

    def movimientos(self):
        return self.serpiente.det(self.tablero)

    def copiar(self):
        return Juego([self.tablero.ancho, self.tablero.alto], self.serpiente.serpiente)



def numeroDeCaminosDiferentesDisponibles(tablero, serpient, profundidad):
    juego = Juego(tablero, serpient)
    return caminos_disponibles(juego, profundidad)
    

def caminos_disponibles(juego: Juego, profundidad):
    if profundidad == 1:
        return len(juego.movimientos())  
    if profundidad == 0:
        return 0
    total_caminos = 0  
    for mover in juego.movimientos():
        copiar_juego = juego.copiar()
        copiar_juego.movimiento_serpiente(mover)
        total_caminos += caminos_disponibles(copiar_juego, profundidad - 1)
    return total_caminos


# Realizacion de pruebas

class TestDesafio(unittest.TestCase):

    def test1(self):
        n = 1
        tablero = [4,3]
        serpiente = [[2,2],  [3,2],  [3,1],  [3,0],  [2,0],  [1,0],  [0,0]]
        profundidad = 3
        resultado = 7

        caminos = numeroDeCaminosDiferentesDisponibles(tablero, serpiente, profundidad)
        self.assertEqual(resultado, caminos, f"El resultado deberia ser {resultado} en lugar de {caminos}")
        print_results(n, tablero, serpiente, profundidad, caminos)

    def test2(self):
        n = 2
        tablero = [2, 3]
        serpiente = [[0,2],  [0,1],  [0,0],  [1,0],  [1,1],  [1,2]]
        profundidad = 10
        resultado = 1

        caminos = numeroDeCaminosDiferentesDisponibles(tablero, serpiente, profundidad)
        self.assertEqual(resultado, caminos, f"El resultado deberia ser {resultado} en lugar de {caminos}")
        print_results(n, tablero, serpiente, profundidad, caminos)

    def test3(self):
        n = 3
        tablero = [10, 10]
        serpiente = [[5,5],  [5,4],  [4,4],  [4,5]]
        profundidad = 4
        resultado = 81

        caminos = numeroDeCaminosDiferentesDisponibles(tablero, serpiente, profundidad)
        self.assertEqual(resultado, caminos, f"El resultado deberia ser {resultado} en lugar de {caminos}")
        print_results(n, tablero, serpiente, profundidad, caminos)

def print_results(n, tablero, serpiente, profundidad, caminos):
    print((f"Test {n}: \n\t- tablero: \"{tablero}\"\n\t- serpiente: \"{serpiente}\""
        f"\n\t- profundidad: \"{profundidad}\" \nTotal caminos disponibles: \"{caminos}\"\n\n"))

if __name__ == "__main__":
    unittest.main()