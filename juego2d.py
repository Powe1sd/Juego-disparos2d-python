import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de Disparos 2D")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Cargar imágenes
background_img = pygame.image.load('fondo.jpeg')
player_img = pygame.image.load('nave.jpeg')
bullet_img = pygame.image.load('balas.jpeg')
enemy_img = pygame.image.load('meteoro.jpeg')

# Redimensionar imágenes
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
player_img = pygame.transform.scale(player_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

player_width, player_height = player_img.get_size()
bullet_width, bullet_height = bullet_img.get_size()
enemy_width, enemy_height = enemy_img.get_size()

# Cargar sonidos
shoot_sound = pygame.mixer.Sound('disparo.wav')
start_sound = pygame.mixer.Sound('intro.wav')

# Reproducir sonido de inicio
start_sound.play()

# Configuración del jugador
player_x = (screen_width // 2) - (player_width // 2)
player_y = screen_height - player_height - 10
player_speed = 5

# Configuración del proyectil
bullet_speed = 7
bullets = []

# Configuración del enemigo
initial_enemy_speed = 2
enemy_speed = initial_enemy_speed
enemies = []

# Fuente para el texto
font = pygame.font.SysFont(None, 36)

# Función para mostrar el puntaje
def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# Función para mostrar el mensaje de Game Over
def show_game_over():
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Espera 2 segundos antes de reiniciar

# Función para reiniciar el juego
def restart_game():
    global score, enemies, bullets, enemy_speed, player_x, player_y
    score = 0
    enemies.clear()
    bullets.clear()
    enemy_speed = initial_enemy_speed
    player_x = (screen_width // 2) - (player_width // 2)
    player_y = screen_height - player_height - 10

# Bucle principal del juego
running = True
score = 0
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + (player_width // 2) - (bullet_width // 2)
                bullet_y = player_y
                bullets.append([bullet_x, bullet_y])
                shoot_sound.play()  # Reproducir sonido de disparo

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                restart_game()
                game_over = False

    if not game_over:
        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - player_speed > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_speed < screen_width - player_width:
            player_x += player_speed

        # Movimiento del proyectil
        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Generación de enemigos
        if random.randint(1, 30) == 1:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = -enemy_height
            enemies.append([enemy_x, enemy_y])

        # Movimiento de los enemigos y colisión con jugador
        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > screen_height:
                enemies.remove(enemy)
            for bullet in bullets:
                if bullet[0] in range(enemy[0], enemy[0] + enemy_width) and bullet[1] in range(enemy[1], enemy[1] + enemy_height):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    # Aumentar la velocidad de los enemigos cada 10 puntos
                    if score % 10 == 0:
                        enemy_speed += 1

            # Colisión del jugador con los enemigos normales
            if (player_x < enemy[0] + enemy_width and
                player_x + player_width > enemy[0] and
                player_y < enemy[1] + enemy_height and
                player_y + player_height > enemy[1]):
                game_over = True
                show_game_over()
                break

        # Dibujar en la pantalla
        screen.blit(background_img, (0, 0))
        screen.blit(player_img, (player_x, player_y))
        for bullet in bullets:
            screen.blit(bullet_img, (bullet[0], bullet[1]))
        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0], enemy[1]))

        # Mostrar el puntaje
        show_score(score)

        # Mostrar Game Over si corresponde
        if game_over:
            show_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
