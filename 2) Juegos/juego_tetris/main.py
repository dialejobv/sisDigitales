import pygame
import random

# Configuración inicial
pygame.init()
pygame.display.set_caption("Tetris Multinivel")

# Constantes
ANCHO = 800
ALTO = 700
TAMANO_BLOQUE = 30
FILAS = 20
COLUMNAS = 10
COLORES = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0, 255),
    (0, 220, 220)
]

# Formas corregidas (todas como listas de listas)
FORMAS = [
    [[1], [1], [1], [1]],         # I vertical
    [[1, 1, 1, 1]],                # I horizontal
    [[2, 2], [2, 2]],               # O
    [[0, 3, 0], [3, 3, 3]],        # T
    [[0, 4, 4], [4, 4, 0]],        # S
    [[5, 5, 0], [0, 5, 5]],        # Z
    [[6, 6, 6], [0, 6, 0]],        # L
    [[7, 7, 7], [7, 0, 0]]         # J
]

class Pieza:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.forma = random.choice(FORMAS)
        self.color = random.randint(1, len(COLORES)-1)
        self.rotacion = 0

    def obtener_forma(self):
        # Asegurar que siempre devuelve lista de listas
        forma_actual = self.forma[self.rotacion % len(self.forma)]
        if isinstance(forma_actual[0], list):
            return forma_actual
        return [forma_actual]

def crear_grid(estado_bloques={}):
    return [[estado_bloques.get((x, y), 0) for x in range(COLUMNAS)] for y in range(FILAS)]

def verificar_colision(pieza, grid):
    forma = pieza.obtener_forma()
    for y, fila in enumerate(forma):
        for x, bloque in enumerate(fila):
            if bloque:
                nueva_x = pieza.x + x
                nueva_y = pieza.y + y
                if not (0 <= nueva_x < COLUMNAS) or nueva_y >= FILAS or (nueva_y >= 0 and grid[nueva_y][nueva_x]):
                    return True
    return False

def limpiar_lineas(grid, estado_bloques):
    lineas_limpias = 0
    for y in range(FILAS):
        if all(grid[y]):
            lineas_limpias += 1
            for yy in range(y, 0, -1):
                for x in range(COLUMNAS):
                    estado_bloques[(x, yy)] = estado_bloques.get((x, yy-1), 0)
    return lineas_limpias

def dibujar_ventana(ventana, grid, pieza_actual, siguiente_pieza, puntuacion, nivel):
    ventana.fill(COLORES[0])
    
    # Dibujar cuadrícula
    for y in range(FILAS):
        for x in range(COLUMNAS):
            pygame.draw.rect(ventana, COLORES[grid[y][x]],
                            (x*TAMANO_BLOQUE, y*TAMANO_BLOQUE,
                             TAMANO_BLOQUE-1, TAMANO_BLOQUE-1))
    
    # Dibujar pieza actual
    forma = pieza_actual.obtener_forma()
    for y, fila in enumerate(forma):
        for x, bloque in enumerate(fila):
            if bloque:
                pygame.draw.rect(ventana, COLORES[pieza_actual.color],
                                ((pieza_actual.x + x)*TAMANO_BLOQUE,
                                 (pieza_actual.y + y)*TAMANO_BLOQUE,
                                 TAMANO_BLOQUE-1, TAMANO_BLOQUE-1))
    
    # Dibujar siguiente pieza
    siguiente_x = ANCHO - 150
    siguiente_y = 100
    texto_siguiente = pygame.font.SysFont('arial', 30).render("Siguiente:", True, (255,255,255))
    ventana.blit(texto_siguiente, (siguiente_x, siguiente_y - 40))
    
    forma_siguiente = siguiente_pieza.obtener_forma()
    for y, fila in enumerate(forma_siguiente):
        for x, bloque in enumerate(fila):
            if bloque:
                pygame.draw.rect(ventana, COLORES[siguiente_pieza.color],
                                (siguiente_x + x*TAMANO_BLOQUE,
                                 siguiente_y + y*TAMANO_BLOQUE,
                                 TAMANO_BLOQUE-1, TAMANO_BLOQUE-1))
    
    # Mostrar puntuación y nivel
    fuente = pygame.font.SysFont('arial', 30)
    texto_puntuacion = fuente.render(f"Puntos: {puntuacion}", True, (255,255,255))
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, (255,255,255))
    ventana.blit(texto_puntuacion, (ANCHO - 150, ALTO - 100))
    ventana.blit(texto_nivel, (ANCHO - 150, ALTO - 70))

def main():
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    
    estado_bloques = {}
    puntuacion = 0
    nivel = 1
    velocidad_caida = 0.5
    
    pieza_actual = Pieza(COLUMNAS//2 - 2, 0)
    siguiente_pieza = Pieza(0, 0)
    
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        velocidad = 60 * velocidad_caida
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    pieza_actual.x -= 1
                    if verificar_colision(pieza_actual, crear_grid(estado_bloques)):
                        pieza_actual.x += 1
                if evento.key == pygame.K_RIGHT:
                    pieza_actual.x += 1
                    if verificar_colision(pieza_actual, crear_grid(estado_bloques)):
                        pieza_actual.x -= 1
                if evento.key == pygame.K_DOWN:
                    pieza_actual.y += 1
                    if verificar_colision(pieza_actual, crear_grid(estado_bloques)):
                        pieza_actual.y -= 1
                if evento.key == pygame.K_UP:
                    pieza_actual.rotacion += 1
                    if verificar_colision(pieza_actual, crear_grid(estado_bloques)):
                        pieza_actual.rotacion -= 1
        
        # Caída automática
        if pygame.time.get_ticks() % int(1000 / velocidad) == 0:
            pieza_actual.y += 1
            if verificar_colision(pieza_actual, crear_grid(estado_bloques)):
                pieza_actual.y -= 1
                forma = pieza_actual.obtener_forma()
                for y, fila in enumerate(forma):
                    for x, bloque in enumerate(fila):
                        if bloque:
                            estado_bloques[(pieza_actual.x + x, pieza_actual.y + y)] = pieza_actual.color
                
                lineas = limpiar_lineas(crear_grid(estado_bloques), estado_bloques)
                if lineas > 0:
                    puntuacion += (2 ** lineas) * 100 * nivel
                    if puntuacion // 500 > nivel - 1 and nivel < 3:
                        nivel += 1
                        velocidad_caida *= 1.5
                
                pieza_actual = siguiente_pieza
                siguiente_pieza = Pieza(0, 0)
                if verificar_colision(pieza_actual, crear_grid(estado_bloques)):
                    ejecutando = False
        
        dibujar_ventana(ventana, crear_grid(estado_bloques), pieza_actual, siguiente_pieza, puntuacion, nivel)
        pygame.display.update()

    # Game Over
    ventana.fill((0,0,0))
    fuente = pygame.font.SysFont('arial', 50)
    texto = fuente.render(f"Game Over - Puntos: {puntuacion}", True, (255,255,255))
    ventana.blit(texto, (ANCHO//2 - 200, ALTO//2 - 50))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()