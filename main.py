import pygame
import os
import random
pygame.init()


WHITE = (255,255,255)
RED = (255,0,0)
WIDTH = 1200
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.flip()
pygame.display.set_caption('Flappy Bird UWU')
CLOCK = pygame.time.Clock()

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'background_pic.png')), (WIDTH,HEIGHT)).convert_alpha()
BIRD_NEUTRAL = pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'bird.png')),(60,60)).convert_alpha()
BIRD_UP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'bird.png')),(70,70)), 30).convert_alpha()
PIPE_image_up = pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'pipe.png')), (100,250)).convert_alpha()
PIPE_image_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'pipe.png')), (100,300)), 180).convert_alpha()
dead_sound = pygame.mixer.Sound(os.path.join('sounds', 'idiot.wav'))
flap_sound = pygame.mixer.Sound(os.path.join('sounds', 'flap.wav'))
point_sound = pygame.mixer.Sound(os.path.join('sounds', 'point.wav'))

FONT_INIT = pygame.font.SysFont('Comic Sans MS', 100)
lose_font_init = pygame.font.SysFont('Comic Sans MS', 60)




class Player:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.image = BIRD_NEUTRAL
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.gravity = 3
		self.vel = 0
		self.up_acceleration = 0.2
		self.down_acceleration = 0.1
		self.jump_height = 10
		self.mask = pygame.mask.from_surface(self.image)
		

	def draw(self):
		SCREEN.blit(self.image, (self.x, self.y))

	def jump(self):
		self.y -= self.jump_height
		self.vel = 9


def load_tilted_birds(x):
	temp = []
	for i in range(12):
		temp.append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'bird.png')),(70,70)), (-30-(5*x))).convert_alpha())
		x += 1
	return temp

def width_of_loaded_birds(tilted_birds_list):
	temp = []
	for item in tilted_birds_list:
		temp.append(item.get_width())
	return temp


def height_of_loaded_birds(tilted_birds_list):
	temp = []
	for item in tilted_birds_list:
		temp.append(item.get_height())
	return temp


class Pipe:
	spacing = 500

	def __init__(self, x):
		self.x = x
		self.speed = 4
		self.up = PIPE_image_up
		self.up_y = HEIGHT - self.up.get_height() - 63 # where to blit the tube pointing up / height of the tube pointing up as well
		self.down = PIPE_image_down
		self.down_y = 0
		self.width = self.up.get_width() # same width for both tubes
		self.height = self.down.get_height()
		self.bird_passed = False
		self.mask_down = pygame.mask.from_surface(self.down)
		self.mask_up = pygame.mask.from_surface(self.up)

	def transform(self, size, dx):
		temp = Pipe(self.x + dx)
		temp.up = pygame.transform.scale(temp.up, (100, size))
		temp.up_y = HEIGHT - temp.up.get_height() - 63
		temp.mask_up = pygame.mask.from_surface(temp.up)
		temp.down = pygame.transform.scale(temp.down, (100, HEIGHT - 250 - size))
		temp.height = temp.down.get_height()
		temp.mask_down = pygame.mask.from_surface(temp.down)
		return temp


	def draw_pipe(self):
		SCREEN.blit(self.up, (self.x, self.up_y))
		SCREEN.blit(self.down, (self.x, self.down_y))

	def move_pipe(self):
		self.x -= self.speed

	def load_pipes(self, how_many):
		temp = []
		for i in range (how_many):
			temp.append(self.transform(300 + (20 *random.randint(-10,10)), (i+1)*Pipe.spacing))
		return temp

	def collide(self, bird):
		bird_mask = bird.mask
		top_mask = pygame.mask.from_surface(self.down)
		bottom_mask = pygame.mask.from_surface(self.up)

		top_offset = (self.x - bird.x, -round(bird.y))
		bottom_offset = (self.x - bird.x, self.up_y - round(bird.y))

		b_point = bird_mask.overlap(bottom_mask, bottom_offset)
		t_point = bird_mask.overlap(top_mask, top_offset)

		if t_point or b_point:
			return True
		
		return False

	
def main():
	
	flappy_bird = Player(WIDTH//2 - 200, HEIGHT//2)
	test = Pipe(600)
	pipe1 = test.load_pipes(4)
	

	FPS = 100
	RUN = True
	score = 0
	score_width = 0
	bird_down_list = load_tilted_birds(0)
	count = 0

	ran_into_pipes = False


	bird_up_width = BIRD_UP.get_width()
	bird_up_height = BIRD_UP.get_height()



	while RUN:

		CLOCK.tick(FPS)

		SCREEN.blit(BACKGROUND, (0,0))


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False

			if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) and (not ran_into_pipes):
				flap_sound.play()
				flappy_bird.jump()
				flappy_bird.image = BIRD_UP
				flappy_bird.width = bird_up_width
				flappy_bird.height = bird_up_height
				flappy_bird.mask = pygame.mask.from_surface(flappy_bird.image)
				count = 0
	
	

		flappy_bird.y -= flappy_bird.vel 
		flappy_bird.y += flappy_bird.gravity
		
		
		if flappy_bird.vel > 0:
			flappy_bird.vel -= flappy_bird.up_acceleration
		else:
			flappy_bird.vel -= flappy_bird.down_acceleration
			
			flappy_bird.image = bird_down_list[count]
			flappy_bird.mask = pygame.mask.from_surface(flappy_bird.image)
			flappy_bird.width = width_of_loaded_birds(bird_down_list)[count]
			flappy_bird.height = height_of_loaded_birds(bird_down_list)[count]
			if count < len(bird_down_list)-1:
				count += 1
		
		for item in pipe1:
			item.draw_pipe()
			item.move_pipe()
			if item.x < -100:
				pipe1.remove(item)
				temp = pipe1[-1]
				pipe1 += temp.load_pipes(1)

			if item.collide(flappy_bird) and (not ran_into_pipes):
				ran_into_pipes = True
				for item in pipe1:
					item.speed = 0
				dead_sound.play()

			elif ((item.x + 0.5*item.width <= flappy_bird.x + 0.5*flappy_bird.width <= item.x + item.width) and (not item.bird_passed)) and (item.height<= flappy_bird.y + 0.5*flappy_bird.height <= item.up_y):
				score += 1
				item.bird_passed = True
				point_sound.play()

		
		flappy_bird.draw()
		

		if flappy_bird.y + flappy_bird.height >= HEIGHT - 43:
			ran_into_pipes = True
			flappy_bird.vel = 0
			flappy_bird.gravity = 0
			flappy_bird.up_acceleration = 0
			flappy_bird.down_acceleration = 0
			for item in pipe1:
				item.speed = 0

		if ran_into_pipes == True:

			lose_font = lose_font_init.render('A to restart, Escape to quit', 1, RED)
			lose_width = lose_font.get_width()
			SCREEN.blit(lose_font, (WIDTH//2 - lose_width//2 , HEIGHT//2))

			keys = pygame.key.get_pressed()
			if keys[pygame.K_a]:
				RUN = False
				main()
			if keys[pygame.K_ESCAPE]:
				RUN = False




		FONT = FONT_INIT.render(str(score), 1, WHITE)
		score_width = FONT.get_width()
		SCREEN.blit(FONT, (WIDTH//2 - score_width//2 , 50))




			
		pygame.display.update()


if __name__ == '__main__':
	main()
