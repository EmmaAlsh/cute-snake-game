import pygame, sys, random
from pygame.math import Vector2

def load_graphic(path):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (cell_size,cell_size))
    return image

class SNAKE: 
  def __init__(self):
    self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
    self.direction = Vector2(1,0)

    self.turn_frames = 0  # cuántos frames mostrar el bow de curva
    self.turn_bow = None  # qué gráfico bow de curva mostrar

    self.previous_direction = Vector2(1,0)
    self.just_turned = False

    self.new_block = False

    self.head_up = load_graphic('Graphics/head_up.png')
    self.head_down = load_graphic('Graphics/head_down.png')
    self.head_right = load_graphic('Graphics/head_right.png')
    self.head_left = load_graphic('Graphics/head_left.png')

    self.tail_up = load_graphic('Graphics/tail_up.png')
    self.tail_down = load_graphic('Graphics/tail_down.png')
    self.tail_right = load_graphic('Graphics/tail_right.png')
    self.tail_left = load_graphic('Graphics/tail_left.png')

    self.body_vertical = load_graphic('Graphics/body_vertical.png')
    self.body_horizontal = load_graphic('Graphics/body_horizontal.png')

    self.body_up_bow = load_graphic('Graphics/body_vertical_bow.png')
    self.body_down_bow = load_graphic('Graphics/body_down_bow.png')
    self.body_left_bow = load_graphic('Graphics/body_left_bow.png')
    self.body_right_bow = load_graphic('Graphics/body_right_bow.png')

    self.body_tr_bow = load_graphic('Graphics/body_tr_bow.png')
    self.body_tl_bow = load_graphic('Graphics/body_tl_bow.png')
    self.body_br_bow = load_graphic('Graphics/body_br_bow.png')
    self.body_bl_bow = load_graphic('Graphics/body_bl_bow.png')

    self.body_tr = load_graphic('Graphics/body_tr.png')
    self.body_tl = load_graphic('Graphics/body_tl.png')
    self.body_br = load_graphic('Graphics/body_br.png')
    self.body_bl = load_graphic('Graphics/body_bl.png')

    self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

  def draw_snake(self):
    self.update_head_graphics()
    self.update_tail_graphics()
    for index, block in enumerate(self.body):
        x_pos = int(block.x * cell_size)
        y_pos = int(block.y * cell_size)
        block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        if index == 0:
          screen.blit(self.head, block_rect)
        elif index == len(self.body) - 1:
          screen.blit(self.tail, block_rect)
        else:
          previous_block = self.body[index + 1] - block  # hacia la cola
          next_block     = self.body[index - 1] - block  # hacia la cabeza
          is_curve = previous_block.x != next_block.x and previous_block.y != next_block.y
          if index == 1:
            if self.turn_frames > 0 and is_curve:
              if   (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                  screen.blit(self.body_tl_bow, block_rect)
              elif (previous_block.x == -1 and next_block.y ==  1) or (previous_block.y ==  1 and next_block.x == -1):
                  screen.blit(self.body_bl_bow, block_rect)
              elif (previous_block.x ==  1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x ==  1):
                  screen.blit(self.body_tr_bow, block_rect)
              elif (previous_block.x ==  1 and next_block.y ==  1) or (previous_block.y ==  1 and next_block.x ==  1):
                  screen.blit(self.body_br_bow, block_rect)
            else: 
              if self.previous_direction == Vector2(0, -1):
                  screen.blit(self.body_up_bow, block_rect)
              elif self.previous_direction == Vector2(0, 1):
                  screen.blit(self.body_down_bow, block_rect)
              elif self.previous_direction == Vector2(-1, 0):
                  screen.blit(self.body_left_bow, block_rect)
              elif self.previous_direction == Vector2(1, 0):
                  screen.blit(self.body_right_bow, block_rect)
          else:
            # Resto del cuerpo → gráficos normales
            if not is_curve:
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                else:
                    screen.blit(self.body_horizontal, block_rect)
            else:
                if   (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                    screen.blit(self.body_tl, block_rect)
                elif (previous_block.x == -1 and next_block.y ==  1) or (previous_block.y ==  1 and next_block.x == -1):
                    screen.blit(self.body_bl, block_rect)
                elif (previous_block.x ==  1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x ==  1):
                    screen.blit(self.body_tr, block_rect)
                elif (previous_block.x ==  1 and next_block.y ==  1) or (previous_block.y ==  1 and next_block.x ==  1):
                    screen.blit(self.body_br, block_rect)
  
  def update_head_graphics(self): 
    head_relation = self.body[1] - self.body[0]
    if head_relation == Vector2(1,0): self.head = self.head_left 
    elif head_relation == Vector2(-1,0): self.head = self.head_right
    elif head_relation == Vector2(0,1): self.head = self.head_up
    elif head_relation == Vector2(0,-1): self.head = self.head_down

  def update_tail_graphics(self):
    tail_relation = self.body[-2] - self.body[-1]
    if tail_relation == Vector2(1,0): self.tail = self.tail_left
    elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
    elif tail_relation == Vector2(0,1): self.tail = self.tail_up
    elif tail_relation == Vector2(0,-1): self.tail = self.tail_down
    #for block in self.body:
    #  x_pos = int(block.x * cell_size)
    #  y_pos = int(block.y * cell_size)
    #  block_rect = pygame.Rect(x_pos , y_pos,cell_size,cell_size )
    #  pygame.draw.rect(screen, (127,174,231), block_rect) 

  def move_snake(self):

    self.just_turned = self.direction != self.previous_direction
    if self.just_turned:
        self.turn_frames = 3  # mostrá el bow de curva por 3 frames
    elif self.turn_frames > 0:
        self.turn_frames -= 1
    self.previous_direction = self.direction.copy()

    if self.new_block == True: 
      body_copy = self.body[:] 
      body_copy.insert(0, body_copy[0] + self.direction)
      self.body = body_copy[:]
      self.new_block = False

    else:
      body_copy = self.body[:-1]
      body_copy.insert(0, body_copy[0] + self.direction)
      self.body = body_copy[:]
  
  def add_block(self):
    self.new_block = True

  def play_crunch_sound(self):
    self.crunch_sound.play()

class FRUIT:
  def __init__(self):
    self.load_images()
    self.randomize()

  def load_images(self):
    cookie = pygame.image.load('Graphics/cookie.png').convert_alpha()
    icecream = pygame.image.load('Graphics/icecream.png').convert_alpha()
    chocolate = pygame.image.load('Graphics/chocolate.png').convert_alpha()

    self.cookie = pygame.transform.scale(cookie, (40,40))
    self.icecream = pygame.transform.scale(icecream, (70,70))
    self.chocolate = pygame.transform.scale(chocolate, (70,70))

  def randomize(self):
    self.x = random.randint(0, cell_number - 1)
    self.y = random.randint(0, cell_number - 2)  # por si es 2 celdas verticales

    self.pos = Vector2(self.x, self.y)

    self.type = random.choice(["cookie", "big"])

    if self.type == "cookie":
      self.current_image = self.cookie
      self.size_cells = (1,1)
    else:
      self.current_image = random.choice([self.icecream, self.chocolate])
      self.size_cells = (1,2)

  def draw_fruit(self):
    # posición base (top-left celda)
    x = int(self.pos.x * cell_size)
    y = int(self.pos.y * cell_size)

    if self.size_cells == (1,1):
      rect = pygame.Rect(x, y, cell_size, cell_size)
      image_rect = self.current_image.get_rect(center=rect.center)
      screen.blit(self.current_image, image_rect)

    else:
      # ocupa 2 celdas pero UNA sola imagen
      rect = pygame.Rect(x, y, cell_size, cell_size * 2)
      image_rect = self.current_image.get_rect(center=rect.center)
      screen.blit(self.current_image, image_rect)
      
class MAIN: 
  def __init__(self):
    self.snake = SNAKE()
    self.fruit = FRUIT()
  
  def update(self):
    self.snake.move_snake()
    self.check_collision()
    self.check_fail()

  def draw_elements(self):
    self.draw_grass()
    self.fruit.draw_fruit()
    self.snake.draw_snake()
    self.draw_score()
  
  def check_collision(self):
    snake_head = self.snake.body[0]
    fx = self.fruit.pos.x
    fy = self.fruit.pos.y

    if self.fruit.size_cells == (1,1):
      if snake_head == Vector2(fx, fy):
        self.fruit.randomize()
        self.snake.add_block()
        self.snake.play_crunch_sound()

      for block in self.snake.body[1:]:
        if block == self.fruit.pos:
          self.fruit.randomize()

    else:
      if snake_head == Vector2(fx, fy) or snake_head == Vector2(fx, fy + 1):
        self.fruit.randomize()
        self.snake.add_block()
        self.snake.play_crunch_sound()
      for block in self.snake.body[1:]:
        if block == self.fruit.pos:
          self.fruit.randomize()

  def check_fail(self):
    if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
      self.game_over()
    
    for block in self.snake.body[1:]:
      if block == self.snake.body[0]:
        self.game_over()
  
  def game_over(self):
    pygame.quit()
    sys.exit()

  def draw_grass(self):
    grass_color = (210,208,87)
    for row in range(cell_number):
      if row % 2 == 0: 
        for col in range(cell_number):
          if col % 2 == 0:
            grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
            pygame.draw.rect(screen,grass_color,grass_rect)
      else: 
        for col in range(cell_number):
          if col % 2 != 0:
            grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
            pygame.draw.rect(screen,grass_color,grass_rect)
  
  def draw_score(self):
    score_text = str(len(self.snake.body) - 3)
    score_surface = game_font.render(score_text,True,(56,74,12))
    score_x = int(cell_size * cell_number - 60)
    score_y = int(cell_size * cell_number - 40)
    score_rect = score_surface.get_rect(center = (score_x,score_y))
    screen.blit(score_surface,score_rect)
    

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40 
cell_number = 20 

screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Font/Fraunces.ttf',25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True: 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    if event.type == SCREEN_UPDATE:
      main_game.update()

    if event.type == pygame.KEYDOWN: 
      if event.key == pygame.K_UP:
        if main_game.snake.direction.y != 1: 
          main_game.snake.direction = Vector2(0,-1)

      if event.key == pygame.K_DOWN:
        if main_game.snake.direction.y != -1:
          main_game.snake.direction = Vector2(0,1)

      if event.key == pygame.K_LEFT:
        if main_game.snake.direction.x != 1:
          main_game.snake.direction = Vector2(-1,0)

      if event.key == pygame.K_RIGHT:
        if main_game.snake.direction.x != -1:
          main_game.snake.direction = Vector2(1,0)

  screen.fill((214,212,94))
  main_game.draw_elements()
  pygame.display.update()
  clock.tick(60)