import pygame, sys, random
from pygame.math import Vector2 

class SNAKE: 
  def __init__(self):
    self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
    self.direction = Vector2(1,0)
    self.new_block = False

    self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
    self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
    self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
    self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

    self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
    self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
    self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
    self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

    self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
    self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

    self.body_vertical_bow = pygame.image.load('Graphics/body_vertical_bow.png').convert_alpha()
    self.body_horizontal_bow = pygame.image.load('Graphics/body_horizontal_bow.png').convert_alpha()
    self.body_left_bow = pygame.image.load('Graphics/body_left_bow.png').convert_alpha()
    self.body_right_bow = pygame.image.load('Graphics/body_right_bow.png').convert_alpha()

    self.body_tr_bow = pygame.image.load('Graphics/body_tr_bow.png').convert_alpha()
    self.body_tl_bow = pygame.image.load('Graphics/body_tl_bow.png').convert_alpha()
    self.body_br_bow = pygame.image.load('Graphics/body_br_bow.png').convert_alpha()
    self.body_bl_bow = pygame.image.load('Graphics/body_bl_bow.png').convert_alpha()

    self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
    self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
    self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
    self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()


  def draw_snake(self):
    for block in self.body:
      x_pos = int(block.x * cell_size)
      y_pos = int(block.y * cell_size)
      block_rect = pygame.Rect(x_pos , y_pos,cell_size,cell_size )
      pygame.draw.rect(screen, (127,174,231), block_rect) 

  def move_snake(self):
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
    self.fruit.draw_fruit()
    self.snake.draw_snake()
  
  def check_collision(self):
    snake_head = self.snake.body[0]
    fx = self.fruit.pos.x
    fy = self.fruit.pos.y

    if self.fruit.size_cells == (1,1):
      if snake_head == Vector2(fx, fy):
        self.fruit.randomize()
        self.snake.add_block()

    else:
      if snake_head == Vector2(fx, fy) or snake_head == Vector2(fx, fy + 1):
        self.fruit.randomize()
        self.snake.add_block()

  def check_fail(self):
    if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
      self.game_over()
    
    for block in self.snake.body[1:]:
      if block == self.snake.body[0]:
        self.game_over()
  
  def game_over(self):
    pygame.quit()
    sys.exit()


pygame.init()
cell_size = 40 
cell_number = 20 

screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()

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