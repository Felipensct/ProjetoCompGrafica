from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

# Variáveis globais para controle da câmera
camera_x = 0.0
camera_y = 2.0
camera_z = 10.0
angle_x = 0.0
angle_y = 0.0
last_mouse_x = 0
last_mouse_y = 0
mouse_buttons = [False] * 3

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    
    # Configuração da primeira lâmpada (frente - próxima ao quadro)
    glPushMatrix()
    light_position0 = [0.0, 3.4, -2.0, 1.0]  
    light_direction0 = [0.0, -1.0, 0.0]      
    glLightfv(GL_LIGHT0, GL_POSITION, light_position0)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_direction0)
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 75.0)
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 1.0)

    # Redução de 20% na intensidade da luz
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])  # Antes era 0.5
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])  # Antes era 1.0
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.56, 0.56, 0.56, 1.0])  # Antes era 0.7

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.02)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0)
    glPopMatrix()
    
    # Configuração da segunda lâmpada (fundo da sala)
    glPushMatrix()
    light_position1 = [0.0, 3.4, 2.0, 1.0]   
    light_direction1 = [0.0, -1.0, 0.0]      
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, light_direction1)
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 80.0)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 1.0)
    
    # Redução de 20% na intensidade da luz
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.32, 0.32, 0.28, 1.0])  # Antes era 0.4
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.72, 0.72, 0.64, 1.0])  # Antes era 0.9
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.4, 0.4, 0.36, 1.0])  # Antes era 0.5
    
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0.4)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.01)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.0)
    glPopMatrix()
    
    # Material geral também reduzido em 20%
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.72, 0.72, 0.72, 1.0])  # Antes era 0.9
    glMaterialf(GL_FRONT, GL_SHININESS, 25.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800.0/600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_ceiling_lamp(x, y, z):
    # Base da lâmpada
    glColor3f(0.8, 0.8, 0.8)  # Cor metálica mais clara
    glPushMatrix()
    glTranslatef(x, y, z)
    draw_cube(0, 0, 0, 0.4, 0.1, 0.4)  # Base quadrada
    glPopMatrix()
    
    # Difusor da lâmpada (mais brilhante)
    glColor4f(1.0, 1.0, 0.95, 0.9)  # Quase branco com alta luminosidade
    glPushMatrix()
    glTranslatef(x, y - 0.1, z)
    draw_cube(0, 0, 0, 0.35, 0.05, 0.35)  # Difusor
    glPopMatrix()

def draw_cube(x, y, z, width, height, depth):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(width, height, depth)
    glutSolidCube(1.0)  # Usando cubo sólido do GLUT
    glPopMatrix()

def draw_professor(x, y, z):
    base_height = -0.5  # Mesma altura do piso
    
    # Cores para o professor
    suit_color = (0.2, 0.2, 0.3)  # Cor do terno
    skin_color = (0.8, 0.7, 0.6)  # Cor da pele
    
    # Cabeça
    glColor3fv(skin_color)
    glPushMatrix()
    glTranslatef(x, base_height + 1.7, z)  # Altura total ~1.75m
    glutSolidSphere(0.15, 20, 20)  # Cabeça esférica
    glPopMatrix()
    
    # Pescoço
    glColor3fv(skin_color)
    glPushMatrix()
    glTranslatef(x, base_height + 1.55, z)
    draw_cube(0, 0, 0, 0.1, 0.1, 0.1)
    glPopMatrix()
    
    # Tronco (terno)
    glColor3fv(suit_color)
    glPushMatrix()
    glTranslatef(x, base_height + 1.2, z)
    draw_cube(0, 0, 0, 0.35, 0.6, 0.25)  # Corpo mais largo que a cabeça
    glPopMatrix()
    
    # Braços
    # Braço direito
    glPushMatrix()
    glTranslatef(x + 0.25, base_height + 1.3, z)
    glRotatef(15, 0, 0, 1)  # Rotação leve do braço
    draw_cube(0, 0, 0, 0.1, 0.4, 0.1)
    glPopMatrix()
    
    # Braço esquerdo
    glPushMatrix()
    glTranslatef(x - 0.25, base_height + 1.3, z)
    glRotatef(-15, 0, 0, 1)  # Rotação leve do braço
    draw_cube(0, 0, 0, 0.1, 0.4, 0.1)
    glPopMatrix()
    
    # Pernas
    glColor3f(0.2, 0.2, 0.2)  # Cor da calça
    # Perna direita
    glPushMatrix()
    glTranslatef(x + 0.1, base_height + 0.5, z)
    draw_cube(0, 0, 0, 0.15, 0.8, 0.15)
    glPopMatrix()
    
    # Perna esquerda
    glPushMatrix()
    glTranslatef(x - 0.1, base_height + 0.5, z)
    draw_cube(0, 0, 0, 0.15, 0.8, 0.15)
    glPopMatrix()
    
    # Sapatos
    glColor3f(0.1, 0.1, 0.1)  # Preto
    # Sapato direito
    glPushMatrix()
    glTranslatef(x + 0.1, base_height + 0.05, z + 0.05)
    draw_cube(0, 0, 0, 0.15, 0.1, 0.25)
    glPopMatrix()
    
    # Sapato esquerdo
    glPushMatrix()
    glTranslatef(x - 0.1, base_height + 0.05, z + 0.05)
    draw_cube(0, 0, 0, 0.15, 0.1, 0.25)
    glPopMatrix()

def draw_floor():
    # Piso em bege uniforme
    glPushMatrix()
    glTranslatef(0.0, -0.5, 0.0)
    
    glColor3f(0.96, 0.87, 0.70)  # Cor bege
    
    # Desenha um único quadrado grande para o piso
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-10.0, 0.0, -10.0)
    glVertex3f(10.0, 0.0, -10.0)
    glVertex3f(10.0, 0.0, 10.0)
    glVertex3f(-10.0, 0.0, 10.0)
    glEnd()
    
    glPopMatrix()

def draw_cylinder(x, y, z, radius, height):
    glPushMatrix()
    glTranslatef(x, y, z)
    quad = gluNewQuadric()
    gluCylinder(quad, radius, radius, height, 20, 20)
    glPopMatrix()

def draw_desk(x, y, z):
    # Altura ajustada para ficar exatamente no chão
    base_height = -0.5  # Mesma altura do piso
    desk_height = 0.75  # Altura total da carteira
    
    # Tampo da carteira
    glColor3f(0.4, 0.25, 0.1)  # Marrom mais claro
    draw_cube(x, base_height + desk_height, z, 0.6, 0.04, 0.4)
    
    # Suporte para livros
    glColor3f(0.35, 0.2, 0.05)
    draw_cube(x, base_height + desk_height + 0.05, z + 0.15, 0.6, 0.08, 0.04)
    
    # Pernas da carteira
    glColor3f(0.3, 0.15, 0.05)  # Marrom mais escuro
    leg_offset_x = 0.25
    leg_offset_z = 0.15
    leg_height = desk_height / 2
    
    for i in [-1, 1]:
        for j in [-1, 1]:
            # Posiciona as pernas tocando exatamente o chão
            draw_cube(x + (i * leg_offset_x), 
                     base_height + leg_height, 
                     z + (j * leg_offset_z), 
                     0.04, desk_height, 0.04)
            
def draw_chair(x, y, z):
    # Altura ajustada para ficar exatamente no chão
    base_height = -0.5  # Mesma altura do piso
    chair_height = 0.45  # Altura total da cadeira
    
    # Assento
    glColor3f(0.35, 0.2, 0.05)
    draw_cube(x, base_height + chair_height, z, 
             0.4, 0.04, 0.4)
    
    # Encosto
    draw_cube(x, base_height + chair_height + 0.25, z + 0.18, 
             0.4, 0.3, 0.04)
    
    # Pernas
    glColor3f(0.3, 0.15, 0.05)
    leg_offset = 0.15
    leg_height = chair_height / 2
    
    for i in [-1, 1]:
        for j in [-1, 1]:
            # Posiciona as pernas tocando exatamente o chão
            draw_cube(x + (i * leg_offset), 
                     base_height + leg_height, 
                     z + (j * leg_offset), 
                     0.04, chair_height, 0.04)

def draw_teacher_desk(x, y, z):
    # Altura ajustada para ficar exatamente no chão
    base_height = -0.5  # Mesma altura do piso
    desk_height = 0.75  # Altura total da mesa
    
    # Tampo da mesa
    glColor3f(0.4, 0.25, 0.1)
    draw_cube(x, base_height + desk_height, z, 
             1.2, 0.05, 0.6)
    
    # Laterais
    glColor3f(0.35, 0.2, 0.05)
    draw_cube(x - 0.55, base_height + (desk_height/2), z, 
             0.05, desk_height, 0.55)
    draw_cube(x + 0.55, base_height + (desk_height/2), z, 
             0.05, desk_height, 0.55)
    
    # Painel frontal
    draw_cube(x, base_height + (desk_height/2), z, 
             1.1, desk_height - 0.1, 0.05)

def draw_blackboard(x, y, z):
    # Quadro
    glColor3f(0.1, 0.3, 0.1)  # Verde escuro
    draw_cube(x, y, z, 4.0, 1.5, 0.05)
    
    # Moldura
    glColor3f(0.4, 0.25, 0.1)  # Marrom
    frame_thickness = 0.05
    # Superior
    draw_cube(x, y + 1.55, z, 4.1, frame_thickness, 0.07)
    # Inferior
    draw_cube(x, y - 1.55, z, 4.1, frame_thickness, 0.07)
    # Laterais
    draw_cube(x - 2.05, y, z, frame_thickness, 1.6, 0.07)
    draw_cube(x + 2.05, y, z, frame_thickness, 1.6, 0.07)
    
    # Suporte para giz
    glColor3f(0.35, 0.35, 0.35)  # Cinza
    draw_cube(x, y - 1.45, z + 0.05, 0.5, 0.03, 0.1)

def draw_walls():
    # Piso com textura xadrez
    glColor3f(0.2, 0.2, 0.2)  # Cinza escuro
    tile_size = 1.0
    for i in range(-5, 6):
        for j in range(-5, 6):
            if (i + j) % 2 == 0:
                glColor3f(0.2, 0.2, 0.2)  # Cinza escuro
            else:
                glColor3f(0.25, 0.25, 0.25)  # Cinza um pouco mais claro
            draw_cube(i * tile_size, -0.5, j * tile_size, 
                     tile_size/2, 0.1, tile_size/2)

    # Paredes com rodapé
    glColor3f(0.9, 0.9, 0.85)  # Cor creme para as paredes
    # Parede do fundo
    draw_cube(0.0, 2.0, -5.0, 10.0, 4.0, 0.2)
    # Parede da esquerda
    draw_cube(-5.0, 2.0, 0.0, 0.2, 4.0, 10.0)
    # Parede da direita
    draw_cube(5.0, 2.0, 0.0, 0.2, 4.0, 10.0)
    
    # Rodapés
    glColor3f(0.3, 0.2, 0.1)  # Marrom escuro
    # Rodapé do fundo
    draw_cube(0.0, 0.1, -4.9, 10.0, 0.2, 0.1)
    # Rodapé da esquerda
    draw_cube(-4.9, 0.1, 0.0, 0.1, 0.2, 10.0)
    # Rodapé da direita
    draw_cube(4.9, 0.1, 0.0, 0.1, 0.2, 10.0)

def draw_windows():
    # Janelas na parede direita
    window_frame_color = (0.4, 0.4, 0.4)
    window_glass_color = (0.6, 0.8, 1.0, 0.3)
    
    for i in range(3):
        # Moldura da janela
        glColor3fv(window_frame_color)
        x = 4.9  # Próximo à parede direita
        y = 2.0  # Altura média
        z = -3.0 + (i * 2.5)  # Espaçamento entre janelas
        
        # Moldura superior e inferior
        draw_cube(x, y + 0.8, z, 0.1, 0.1, 1.5)
        draw_cube(x, y - 0.8, z, 0.1, 0.1, 1.5)
        # Moldura lateral
        draw_cube(x, y, z + 0.75, 0.1, 1.7, 0.1)
        draw_cube(x, y, z - 0.75, 0.1, 1.7, 0.1)
        
        # Vidro da janela
        glColor4fv(window_glass_color)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        draw_cube(x, y, z, 0.05, 1.5, 1.4)
        glDisable(GL_BLEND)

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    glTranslatef(-camera_x, -camera_y, -camera_z)
    glRotatef(angle_x, 1.0, 0.0, 0.0)
    glRotatef(angle_y, 0.0, 1.0, 0.0)
    
    # Atualizar posições das luzes após as transformações da câmera
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 3.4, -2.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, -1.0, 0.0])
    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 3.4, 2.0, 1.0])
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [0.0, -1.0, 0.0])

    # Desenha o piso primeiro
    draw_floor()
    
    # Paredes
    glColor3f(0.9, 0.9, 0.85)  # Cor creme para as paredes
    # Parede do fundo
    draw_cube(0.0, 1.5, -5.0, 10.0, 4.0, 0.2)
    # Paredes laterais
    draw_cube(-5.0, 1.5, 0.0, 0.2, 4.0, 10.0)
    draw_cube(5.0, 1.5, 0.0, 0.2, 4.0, 10.0)
    
    # Teto
    glColor3f(0.95, 0.95, 0.95)  # Branco levemente acinzentado
    draw_cube(0.0, 3.5, 0.0, 10.0, 0.1, 10.0)
    
    # Lâmpadas no teto
    draw_ceiling_lamp(0.0, 3.4, -2.0)  # Lâmpada frontal
    draw_ceiling_lamp(0.0, 3.4, 2.0)   # Lâmpada do fundo
    
    # Rodapés
    glColor3f(0.3, 0.2, 0.1)
    draw_cube(0.0, -0.3, -5.0, 10.0, 0.4, 0.1)  # Fundo
    draw_cube(-5.0, -0.3, 0.0, 0.1, 0.4, 10.0)  # Esquerda
    draw_cube(5.0, -0.3, 0.0, 0.1, 0.4, 10.0)   # Direita
    
    # Quadro negro
    glColor3f(0.1, 0.3, 0.1)
    draw_cube(0.0, 1.5, -4.8, 4.0, 1.5, 0.1)
    
    # Moldura do quadro
    glColor3f(0.4, 0.25, 0.1)  # Marrom
    # Superior
    draw_cube(0.0, 2.3, -4.8, 4.1, 0.1, 0.12)
    # Inferior
    draw_cube(0.0, 0.7, -4.8, 4.1, 0.1, 0.12)
    # Laterais
    draw_cube(-2.05, 1.5, -4.8, 0.1, 1.7, 0.12)
    draw_cube(2.05, 1.5, -4.8, 0.1, 1.7, 0.12)
    
    # Suporte para giz
    glColor3f(0.35, 0.35, 0.35)
    draw_cube(0.0, 0.8, -4.75, 0.5, 0.05, 0.15)
    
    # Mesa do professor
    draw_teacher_desk(-3.0, 0.0, -3.0)
    
    # Professor
    draw_professor(-2.2, 0.0, -3.0)
    
    # Grade de carteiras e cadeiras
    for i in range(4):
        for j in range(3):
            x = -2.0 + (j * 2)
            z = -1.0 + (i * 1.5)
            draw_desk(x, 0.0, z)
            draw_chair(x, 0.0, z + 0.3)
    
    # Janelas na parede direita
    window_frame_color = (0.4, 0.4, 0.4)
    window_glass_color = (0.6, 0.8, 1.0, 0.3)
    
    for i in range(3):
        # Moldura da janela
        glColor3fv(window_frame_color)
        x = 4.9  # Próximo à parede direita
        y = 2.0  # Altura média
        z = -3.0 + (i * 2.5)  # Espaçamento entre janelas
        
        # Moldura superior e inferior
        draw_cube(x, y + 0.8, z, 0.1, 0.1, 1.5)
        draw_cube(x, y - 0.8, z, 0.1, 0.1, 1.5)
        # Moldura lateral
        draw_cube(x, y, z + 0.75, 0.1, 1.7, 0.1)
        draw_cube(x, y, z - 0.75, 0.1, 1.7, 0.1)
        
        # Vidro da janela
        glColor4fv(window_glass_color)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        draw_cube(x, y, z, 0.05, 1.5, 1.4)
        glDisable(GL_BLEND)

    glutSwapBuffers()

def reshape(w, h):
    if h == 0:
        h = 1
    
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def mouse_button(button, state, x, y):
    global last_mouse_x, last_mouse_y
    if button < 3:
        mouse_buttons[button] = (state == GLUT_DOWN)
    last_mouse_x = x
    last_mouse_y = y

def mouse_motion(x, y):
    global angle_x, angle_y, last_mouse_x, last_mouse_y
    
    dx = x - last_mouse_x
    dy = y - last_mouse_y
    
    if mouse_buttons[0]:  # Rotação
        angle_y += dx * 0.5
        angle_x += dy * 0.5
    
    last_mouse_x = x
    last_mouse_y = y
    glutPostRedisplay()

def keyboard(key, x, y):
    global camera_x, camera_y, camera_z
    
    if key == b'w':
        camera_z -= 0.5
    elif key == b's':
        camera_z += 0.5
    elif key == b'a':
        camera_x -= 0.5
    elif key == b'd':
        camera_x += 0.5
    elif key == b'q':  # Zoom in
        camera_z -= 0.5
    elif key == b'e':  # Zoom out
        camera_z += 0.5
    elif key == b'r':  # Reset view
        camera_x = 0.0
        camera_y = 2.0
        camera_z = 10.0
        global angle_x, angle_y
        angle_x = 0.0
        angle_y = 0.0
    
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Sala de Aula 3D")
    
    init()
    
    glutDisplayFunc(draw_scene)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse_button)
    glutMotionFunc(mouse_motion)
    glutKeyboardFunc(keyboard)
    
    glutMainLoop()

if __name__ == "__main__":
    main()