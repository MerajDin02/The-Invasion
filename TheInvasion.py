import pygame, random
from pygame.locals import *
from pygame import mixer

pygame.init()
mixer.init()

# Game window
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Invasion')

# FPS
fps = 60
clock = pygame.time.Clock()

# Colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Background
bg = pygame.image.load("C:\\Users\\12673\\AppData\\Local\\Programs\\Python\\Python311\\img\\bg.png")
def draw_bg():
	screen.blit(bg, (0, 0))

# Font
font = pygame.font.SysFont('Verdana', 40)

# Game Sounds
explosion_fx = pygame.mixer.Sound("C:\\Users\\12673\\AppData\\Local\\Programs\\Python\\Python311\\img\\explosion.wav")
explosion_fx.set_volume(0.15)

explosion2_fx = pygame.mixer.Sound("C:\\Users\\12673\\AppData\\Local\\Programs\\Python\\Python311\\img\\explosion2.wav")
explosion2_fx.set_volume(0.50)

laser_fx = pygame.mixer.Sound("C:\\Users\\12673\\AppData\\Local\\Programs\\Python\\Python311\\img\\laser.wav")
laser_fx.set_volume(0.15)

# Game Variables
rows = 5
cols = 5
alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0

# Text Function
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# Spaceship
class Spaceship(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("C:\\Users\\12673\\AppData\\Local\\Programs\\Python\\Python311\\img\\spaceship.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining = health
		self.last_shot = pygame.time.get_ticks()

	def update(self):
		# Movement Speed
		speed = 6.5
		# Cooldown in Milliseconds
		cooldown = 500
		game_over = 0

		# Keys for Moving
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += speed

		# Current Time
		time_now = pygame.time.get_ticks()
		# Key for Shooting
		if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
			laser_fx.play()
			bullet = Bullets(self.rect.centerx, self.rect.top)
			bullet_group.add(bullet)
			self.last_shot = time_now

		# Update Mask
		self.mask = pygame.mask.from_surface(self.image)


		# Health Bar
		pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
		elif self.health_remaining <= 0:
			explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
			explosion_group.add(explosion)
			self.kill()
			game_over = -1
		return game_over
	
# Aliens
class Aliens(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("C:\\Users\\12673\\AppData\\Local\\Programs\\Python\\Python311\\img\\alien" + str(random.randint(1, 5)) + ".png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.move_counter = 0
		self.move_direction = 1

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction

# Bullets
class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("C:\\Users\\12673\\AppData\\Local\\Programs\\Python\\Python311\\img\\bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()
		if pygame.sprite.spritecollide(self, alien_group, True):
			self.kill()
			explosion_fx.play()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
			explosion_group.add(explosion)

# Alien Bullets
class Alien_Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("C:\\Users\\12673\\AppData\\Local\\Programs\\Python\\Python311\\img\\alien_bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.y += 2
		if self.rect.top > screen_height:
			self.kill()
		if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
			self.kill()
			explosion2_fx.play()
			# Reduce Spaceship Health
			spaceship.health_remaining -= 1
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)

# Explosion
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"C:\\Users\\12673\\AppData\\Local\\Programs\\Python\\Python311\\img\\exp{num}.png")
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			# Append Image
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 3
		# Update Explosion Animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		# Delete Explosion when Animation Done
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

# Sprites
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

def create_aliens():
	# Generate Aliens
	for row in range(rows):
		for item in range(cols):
			alien = Aliens(100 + item * 100, 100 + row * 70)
			alien_group.add(alien)

create_aliens()

# Create Player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

run = True
while run:

	clock.tick(fps)

	# Draw Background
	draw_bg()

	if countdown == 0:
		# Create Random Alien Bullets
		# Record Current Time
		time_now = pygame.time.get_ticks()
		# Shoot
		if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
			attacking_alien = random.choice(alien_group.sprites())
			alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
			alien_bullet_group.add(alien_bullet)
			last_alien_shot = time_now

		# Check if all Enemies Killed
		if len(alien_group) == 0:
			game_over = 1

		if game_over == 0:
			# Update Spaceship
			game_over = spaceship.update()

			# Update Sprites
			bullet_group.update()
			alien_group.update()
			alien_bullet_group.update()
		else:
			if game_over == -1:
				draw_text('GAME OVER!', font, white, int(screen_width / 2 - 110), int(screen_height / 2 + 100))
			if game_over == 1:
				draw_text('YOU WIN!', font, white, int(screen_width / 2 - 110), int(screen_height / 2 + 100))

	if countdown > 0:
		draw_text('GET READY!', font, white, int(screen_width / 2 - 110), int(screen_height / 2 + 100))
		draw_text(str(countdown), font, white, int(screen_width / 2 - 10), int(screen_height / 2 + 150))
		count_timer = pygame.time.get_ticks()
		if count_timer - last_count > 1000:
			countdown -= 1
			last_count = count_timer

	# Update Explosion Group
	explosion_group.update()

	# Draw Sprites
	spaceship_group.draw(screen)
	bullet_group.draw(screen)
	alien_group.draw(screen)
	alien_bullet_group.draw(screen)
	explosion_group.draw(screen)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
