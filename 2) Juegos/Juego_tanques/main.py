import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Battle - Versión Corregida")

# Colores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Tank(pygame.sprite.Sprite):
    def __init__(self, color, x, y, is_player=True):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.health = 100
        self.is_player = is_player
        self.shoot_cooldown = 0
        self.direction = 0  # 0 = derecha, 180 = izquierda

    def update(self):
        if self.is_player:
            self.player_controls()
        else:
            self.enemy_ai()
            
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def player_controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = 180
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            
        self.rect.clamp_ip(screen.get_rect())

    def enemy_ai(self):
        if random.randint(0, 100) < 2:
            self.direction = random.choice([0, 180])
            
        if self.direction == 0:
            self.rect.x += self.speed // 2
        else:
            self.rect.x -= self.speed // 2
            
        if random.randint(0, 100) < 1 and self.shoot_cooldown == 0:
            self.shoot()

    def shoot(self):
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction, self.is_player)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.shoot_cooldown = 30  # Cooldown de 0.5 segundos (30 frames a 60 FPS)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, is_player_bullet):
        super().__init__()
        self.image = pygame.Surface((8, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.direction = direction
        self.is_player_bullet = is_player_bullet

    def update(self):
        angle = math.radians(self.direction)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)
        
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

# Configuración del juego
MAX_ENEMIES = 5
ENEMY_SPAWN_TIME = 2000  # 2 segundos entre apariciones
enemies_destroyed = 0
last_spawn = 0

# Grupos de sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Crear jugador
player = Tank(GREEN, WIDTH//2, HEIGHT-50)
all_sprites.add(player)

# Bucle principal
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Generar nuevos enemigos
    if len(enemies) < MAX_ENEMIES and current_time - last_spawn > ENEMY_SPAWN_TIME:
        enemy = Tank(RED, random.randint(50, WIDTH-50), random.randint(50, 200), False)
        all_sprites.add(enemy)
        enemies.add(enemy)
        last_spawn = current_time
    
    # Actualizar elementos
    all_sprites.update()

    # Colisiones balas-enemigos (solo balas del jugador)
    for bullet in bullets:
        if bullet.is_player_bullet:
            enemies_hit = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in enemies_hit:
                enemy.health -= 20
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()
                    enemies_destroyed += 1
                    player.health = min(player.health + 15, 100)

    # Colisiones balas-jugador (solo balas enemigas)
    for bullet in bullets:
        if not bullet.is_player_bullet and player.rect.colliderect(bullet.rect):
            player.health -= 10
            bullet.kill()
            if player.health <= 0:
                running = False

    # Dibujar
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # HUD
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Salud: {player.health}", True, WHITE)
    screen.blit(health_text, (10, 10))
    
    score_text = font.render(f"Enemigos Destruidos: {enemies_destroyed}", True, WHITE)
    screen.blit(score_text, (10, 50))
    
    pygame.display.flip()

pygame.quit()
