from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
import math

# Variáveis globais
window_width = 800
window_height = 600
pacman_x = 400
pacman_y = 300
pacman_size = 20
pacman_direction = [0, 0]
pacman_speed = 5

# Cenário (1: parede, 0: caminho)
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Fantasmas
ghosts = [
    {'x': 100, 'y': 100, 'dx': 2, 'dy': 0, 'color': (1, 0, 0)},  # Vermelho
    {'x': 700, 'y': 100, 'dx': -2, 'dy': 0, 'color': (1, 0.5, 0)},  # Laranja
    {'x': 100, 'y': 500, 'dx': 0, 'dy': 2, 'color': (0, 1, 1)},  # Ciano
    {'x': 700, 'y': 500, 'dx': 0, 'dy': -2, 'color': (1, 0.75, 0.8)}  # Rosa
]

# Comida
food_items = []
food_size = 8

# Estado do jogo
score = 0
lives = 3
game_state = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER

def init_food():
    global food_items
    food_items = []
    
    # Calcula o tamanho de cada célula do labirinto
    cell_width = window_width // len(maze[0])
    cell_height = window_height // len(maze)
    
    # Espaçamento para centralizar as bolinhas nas células
    offset_x = cell_width // 2
    offset_y = cell_height // 2
    
    # Adiciona uma bolinha no centro de cada célula que é caminho (0)
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 0:  # Se for um caminho
                food_items.append({
                    'x': x * cell_width + offset_x,
                    'y': (len(maze) - 1 - y) * cell_height + offset_y,  # Inverte Y para corresponder à coordenada OpenGL
                    'active': True
                })

def draw_maze():
    cell_width = window_width // len(maze[0])
    cell_height = window_height // len(maze)
    
    glColor3f(0, 0, 1)  # Azul para as paredes
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:  # Se for parede
                glBegin(GL_QUADS)
                glVertex2f(x * cell_width, y * cell_height)
                glVertex2f((x + 1) * cell_width, y * cell_height)
                glVertex2f((x + 1) * cell_width, (y + 1) * cell_height)
                glVertex2f(x * cell_width, (y + 1) * cell_height)
                glEnd()

def check_wall_collision(x, y):
    cell_width = window_width // len(maze[0])
    cell_height = window_height // len(maze)
    
    # Converte coordenadas da tela para índices da matriz
    maze_x = int(x // cell_width)
    maze_y = int(y // cell_height)
    
    # Verifica se está dentro dos limites
    if maze_x < 0 or maze_x >= len(maze[0]) or maze_y < 0 or maze_y >= len(maze):
        return True
        
    return maze[maze_y][maze_x] == 1

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))

def draw_menu():
    glColor3f(1, 1, 1)
    draw_text(window_width/2 - 100, window_height/2 + 50, "PAC-MAN")
    draw_text(window_width/2 - 100, window_height/2, "Pressione ENTER para jogar")
    draw_text(window_width/2 - 100, window_height/2 - 50, "ESC para sair")

def draw_game_over():
    glColor3f(1, 0, 0)
    draw_text(window_width/2 - 100, window_height/2, "GAME OVER")
    draw_text(window_width/2 - 150, window_height/2 - 50, f"Pontuacao Final: {score}")
    draw_text(window_width/2 - 150, window_height/2 - 100, "Pressione ENTER para reiniciar")

# Adicione estas variáveis globais para controlar a animação da boca
mouth_angle = 0  # Ângulo atual da boca
mouth_speed = 5  # Velocidade da animação
mouth_opening = True  # Direção da animação (abrindo ou fechando)
max_mouth_angle = 45  # Ângulo máximo de abertura (em graus)

def draw_pacman():
    global mouth_angle, mouth_opening
    
    # Atualiza o ângulo da boca
    if mouth_opening:
        mouth_angle += mouth_speed
        if mouth_angle >= max_mouth_angle:
            mouth_opening = False
    else:
        mouth_angle -= mouth_speed
        if mouth_angle <= 0:
            mouth_opening = True
            
    # Calcula a direção do Pac-Man baseado no movimento
    direction_angle = 0
    if pacman_direction[0] > 0:  # Direita
        direction_angle = 0
    elif pacman_direction[0] < 0:  # Esquerda
        direction_angle = 180
    elif pacman_direction[1] > 0:  # Cima
        direction_angle = 90
    elif pacman_direction[1] < 0:  # Baixo
        direction_angle = 270
        
    glColor3f(1, 1, 0)  # Amarelo
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(pacman_x, pacman_y)  # Centro do Pac-Man
    
    # Desenha o Pac-Man como uma sequência de triângulos em leque
    start_angle = math.radians(direction_angle + mouth_angle)
    end_angle = math.radians(direction_angle + 360 - mouth_angle)
    
    # Número de segmentos para formar o círculo
    segments = 32
    
    # Adiciona o primeiro ponto
    angle = start_angle
    glVertex2f(pacman_x + pacman_size * math.cos(angle),
               pacman_y + pacman_size * math.sin(angle))
               
    # Desenha o arco
    for i in range(segments + 1):
        if angle <= end_angle:
            glVertex2f(pacman_x + pacman_size * math.cos(angle),
                      pacman_y + pacman_size * math.sin(angle))
        angle = start_angle + (end_angle - start_angle) * i / segments
        
    glEnd()

def draw_ghost(ghost):
    glColor3f(*ghost['color'])
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(ghost['x'], ghost['y'])
    for i in range(31):
        angle = i * 2.0 * math.pi / 30
        glVertex2f(ghost['x'] + pacman_size * math.cos(angle),
                  ghost['y'] + pacman_size * math.sin(angle))
    glEnd()

def draw_food(food):
    if food['active']:
        glColor3f(1, 1, 1)  # Branco
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(food['x'], food['y'])
        
        # Desenha uma bolinha menor
        radius = food_size // 2  # Reduz o tamanho das bolinhas
        for i in range(12):  # Reduz o número de segmentos para um círculo mais simples
            angle = i * 2.0 * math.pi / 11
            glVertex2f(food['x'] + radius * math.cos(angle),
                      food['y'] + radius * math.sin(angle))
        glEnd()

def get_valid_directions(x, y):
    """Retorna as direções válidas (sem paredes) para uma posição"""
    cell_width = window_width // len(maze[0])
    cell_height = window_height // len(maze)
    
    valid_dirs = []
    # Direções: direita, esquerda, cima, baixo
    directions = [(cell_width, 0), (-cell_width, 0), (0, cell_height), (0, -cell_height)]
    
    for dx, dy in directions:
        if not check_wall_collision(x + dx, y + dy):
            valid_dirs.append((dx, dy))
    
    return valid_dirs

def choose_direction(ghost_x, ghost_y, target_x, target_y):
    """Escolhe a melhor direção para alcançar o alvo"""
    valid_dirs = get_valid_directions(ghost_x, ghost_y)
    best_dir = None
    min_dist = float('inf')
    
    for dx, dy in valid_dirs:
        new_x = ghost_x + dx
        new_y = ghost_y + dy
        # Calcula a distância até o alvo
        dist = math.sqrt((new_x - target_x)**2 + (new_y - target_y)**2)
        if dist < min_dist:
            min_dist = dist
            best_dir = (dx/5, dy/5)  # Reduz a velocidade do movimento
    
    # Se não encontrar direção válida, mantém a direção atual
    if best_dir is None:
        return ghost['dx'], ghost['dy']
    return best_dir

def check_collision(x1, y1, x2, y2, min_dist):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) < min_dist ** 2

def get_random_valid_position():
    """Retorna uma posição aleatória válida no mapa (em um caminho)"""
    cell_width = window_width // len(maze[0])
    cell_height = window_height // len(maze)
    
    while True:
        # Escolhe uma posição aleatória
        maze_x = random.randint(0, len(maze[0]) - 1)
        maze_y = random.randint(0, len(maze) - 1)
        
        # Verifica se é um caminho válido
        if maze[maze_y][maze_x] == 0:
            # Converte para coordenadas da tela e centraliza na célula
            screen_x = maze_x * cell_width + cell_width // 2
            screen_y = (len(maze) - 1 - maze_y) * cell_height + cell_height // 2
            return screen_x, screen_y
        
def reset_game():
    """Reinicia o jogo após morte do jogador"""
    global pacman_x, pacman_y, pacman_direction, ghosts
    
    # Reseta posição do Pac-Man
    pacman_x = window_width // 2
    pacman_y = window_height // 2
    pacman_direction = [0, 0]
    
    # Reseta posição dos fantasmas
    colors = [(1, 0, 0), (1, 0.5, 0), (0, 1, 1), (1, 0.75, 0.8)]  # Mantém as cores originais
    ghosts = []
    
    for color in colors:
        x, y = get_random_valid_position()
        ghosts.append({
            'x': x,
            'y': y,
            'dx': 0,
            'dy': 0,
            'color': color
        })

def update_game():
    global pacman_x, pacman_y, score, lives, game_state

    if game_state != "PLAYING":
        return

    # Atualiza posição do Pac-Man
    new_x = pacman_x + pacman_direction[0]
    new_y = pacman_y + pacman_direction[1]
    
    # Verifica colisão com paredes antes de mover
    if not check_wall_collision(new_x, new_y):
        pacman_x = new_x
        pacman_y = new_y

    # Atualiza fantasmas
    ghost_speed = 2 
    
    for i, ghost in enumerate(ghosts):
        # Calcula a direção para o Pac-Man
        dx = 0
        dy = 0
        
        # Se o Pac-Man estiver à direita do fantasma
        if pacman_x > ghost['x']:
            dx = ghost_speed
        # Se o Pac-Man estiver à esquerda do fantasma
        elif pacman_x < ghost['x']:
            dx = -ghost_speed
            
        # Se o Pac-Man estiver acima do fantasma
        if pacman_y > ghost['y']:
            dy = ghost_speed
        # Se o Pac-Man estiver abaixo do fantasma
        elif pacman_y < ghost['y']:
            dy = -ghost_speed
            
        # Tenta mover na direção escolhida
        new_ghost_x = ghost['x'] + dx
        new_ghost_y = ghost['y'] + dy
        
        # Verifica colisão com paredes
        wall_collision = check_wall_collision(new_ghost_x, new_ghost_y)
        
        # Verifica colisão com outros fantasmas
        ghost_collision = False
        for j, other_ghost in enumerate(ghosts):
            if i != j:  # Não verifica colisão consigo mesmo
                if check_collision(new_ghost_x, new_ghost_y, 
                                 other_ghost['x'], other_ghost['y'], 
                                 pacman_size * 2):
                    ghost_collision = True
                    break
        
        # Se houver colisão com parede ou outro fantasma
        if wall_collision or ghost_collision:
            new_ghost_y = ghost['y']
            if check_wall_collision(new_ghost_x, new_ghost_y):
                new_ghost_x = ghost['x']
                new_ghost_y = ghost['y'] + dy
                if check_wall_collision(new_ghost_x, new_ghost_y):
                    new_ghost_x = ghost['x']
                    new_ghost_y = ghost['y']
        
        # Atualiza a posição do fantasma
        ghost['x'] = new_ghost_x
        ghost['y'] = new_ghost_y
            
        # Colisão com Pac-Man
        if check_collision(pacman_x, pacman_y, ghost['x'], ghost['y'], pacman_size * 2):
            lives -= 1
            if lives <= 0:
                game_state = "GAME_OVER"
            else:
                reset_game()

    # Colisão com comida
    for food in food_items:
        if food['active'] and check_collision(pacman_x, pacman_y, food['x'], food['y'], pacman_size + food_size):
            food['active'] = False
            score += 10

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    if game_state == "MENU":
        draw_menu()
    elif game_state == "GAME_OVER":
        draw_game_over()
    else:
        # Desenha o labirinto
        draw_maze()
        
        # Desenha elementos do jogo
        draw_pacman()
        for ghost in ghosts:
            draw_ghost(ghost)
        for food in food_items:
            draw_food(food)
            
        # Desenha HUD
        glColor3f(1, 1, 1)
        draw_text(10, window_height - 30, f"Score: {score}")
        draw_text(10, window_height - 60, f"Lives: {lives}")
        
        if game_state == "PAUSED":
            draw_text(window_width/2 - 50, window_height/2, "PAUSADO")

    glutSwapBuffers()

def keyboard(key, x, y):
    global game_state, pacman_direction, score, lives

    if isinstance(key, bytes):
        key = key.decode('utf-8').upper()
    
    if key == '\r':  # ENTER
        if game_state == "MENU" or game_state == "GAME_OVER":
            game_state = "PLAYING"
            score = 0
            lives = 3
            reset_game()  # Reinicia posições
            init_food()
    elif key == 'P':
        if game_state == "PLAYING":
            game_state = "PAUSED"
        elif game_state == "PAUSED":
            game_state = "PLAYING"
    elif key == '\x1b':  # ESC
        sys.exit(0)

def special_keys(key, x, y):
    global pacman_direction
    
    if game_state != "PLAYING":
        return

    if key == GLUT_KEY_LEFT:
        pacman_direction = [-pacman_speed, 0]
    elif key == GLUT_KEY_RIGHT:
        pacman_direction = [pacman_speed, 0]
    elif key == GLUT_KEY_UP:
        pacman_direction = [0, pacman_speed]
    elif key == GLUT_KEY_DOWN:
        pacman_direction = [0, -pacman_speed]

def timer(value):
    update_game()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # 60 FPS aproximadamente

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(50, 50)
    glutCreateWindow(b"Pac-Man")

    glClearColor(0, 0, 0, 1)
    gluOrtho2D(0, window_width, 0, window_height)

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(0, timer, 0)

    init_food()
    glutMainLoop()

if __name__ == "__main__":
    main()