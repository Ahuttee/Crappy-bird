import pygame_sdl2 as pygame
from random import randint
pygame.init()
winx, winy = 1080, 1920
win = pygame.display.set_mode((winx, winy))
font = pygame.font.SysFont("DejaVuSans", 128)
font2 = pygame.font.SysFont("DejaVuSans", 64)
bird = pygame.Rect(winx/4, winy/2, 128, 128)
clock = pygame.time.Clock()
WHITE = (255,255,255)
GREEN = (0,200,0)
text = font.render("Clicc to start", 0, WHITE)


started = False
hit = False
velocity = 7.5
jump_count = 10
jump = False	
score = 0


class pipe(object):
	def __init__(self, x, y, size, win):
		self.width = size/2
		self.win = win
		self.gap = pygame.Rect(x+self.width, y, self.width, size)
		self.upper_pipe = pygame.Rect(x, 0, self.width, y)
		self.lower_pipe = pygame.Rect(x, y+size, self.width, win.get_height()-y+size)
		self.movement_speed = 13.5
		self.passed = False
	def update(self):
		pygame.draw.rect(win, GREEN, self.lower_pipe)
		pygame.draw.rect(win, GREEN, self.upper_pipe)

		
pipes = []
												
def summon_pipe():
	global pipes
	randY = randint(winy*0.05, winy*0.75)
	pipes.append(pipe(winx*1.10, randY, winy*0.25, win))
count = 0

restart_delay = 40

def update():
	global started, hit, velocity, jump, jump_count,text, count, score, restart_delay
	if started:		
		text = font.render(f"{score}", 0, WHITE)
		
		if count % 55 == 0:
			summon_pipe()
		count += 1
		
		#Falling movement of bird
		bird.y += velocity
		velocity += 1.5
		if bird.y >= winy-128:
			hit = True
	
		#Jumping action
		if jump:
			if jump_count > 0:
				bird.y -= 0.45*jump_count**2
				jump_count -= 1
			else:
				jump_count = 12
				jump = False
		#Check if the bird has passed through or collided with a pipe
		
		for pipe in pipes:
			if bird.colliderect(pipe.gap):
				if not pipe.passed:
					score += 1
					pipe.passed = True
					
			if bird.colliderect(pipe.upper_pipe) or bird.colliderect(pipe.lower_pipe):
				hit = True
				started = False
				
			#Move pipes
					
			pipe.gap.x -= pipe.movement_speed
			pipe.upper_pipe.x -= pipe.movement_speed
			pipe.lower_pipe.x -= pipe.movement_speed
		
			#Removes pipe from existence once it goes off screen	
			if pipe.gap.x <= -pipe.width:
				pipes.pop(pipes.index(pipe))
			
	#update pipes		
	for pipe in pipes:
		pipe.update()

	if hit:
		#Game over text

		text = font.render("LOL u suck", 0, WHITE)
		score_label = font2.render(f"score: {score}", 0, WHITE)
	
		started = False
		win.blit(score_label, ((winx-score_label.get_width())/2, winy/3.5))
			
		#Bird falling movement
		bird.y += velocity
		velocity += 3
		bird.clamp_ip(win.get_rect())
		
		restart_delay -= 1

while True:
	win.fill((0,0,0))
	clock.tick(30)
	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			pygame.quit()
		if ev.type == pygame.MOUSEBUTTONDOWN:
			if not started and not hit:
				text = font.render(f"{score}", 0, WHITE)
				started = True
				jump = True
				jump_count = 12
				velocity = 7.5
			elif hit and not started and restart_delay <= 0:
				text = font.render("Clicc to start", 0, WHITE)
				bird.x = winx/4
				bird.y = winy/2
				started = False
				hit = False
				score = 0
				pipes = []
				restart_delay = 40

			elif started and not hit and bird.y > 0:
				jump = True
				jump_count = 12
				velocity = 7.5
	update()
	win.blit(text, ((winx-text.get_width())/2, winy/6))
	win.fill(WHITE, bird)
	pygame.display.update()