import pygame
from pygame.locals import *
import sys
from game import *

FPS = 30 #frames per second
MOVE_TIME = 500 #moves will be displayed for 1 second
SCREEN_SIZE = (500, 500)

def main():

	pygame.init()

	screen = pygame.display.set_mode(SCREEN_SIZE)
	clock = pygame.time.Clock()
	pygame.display.set_caption("PyMemory")

	game = Game(SCREEN_SIZE[0], SCREEN_SIZE[1])
	game.draw_all(screen)
	game.generate_moves()
	game.update_score(screen)
	game.draw_credits(screen)

	elapsed = 0
	i = 0
	last = 0
	drawn = False
	pause = False

	while 1:
		elapsed += clock.tick(FPS)

		if game.current_player == 0: #CPU turn
			if pause == False: 
				if drawn == False:
					game.delete_cpu_move(screen, game.cpu_moves[last])
					game.draw_cpu_move(screen, game.cpu_moves[i])
					drawn = True
				if elapsed >= MOVE_TIME:
					last = i
					i += 1
					if i > len(game.cpu_moves) - 1:
						game.toggle_turn()
					game.delete_cpu_move(screen, game.cpu_moves[last])
					elapsed = 0
					drawn = False
					pause = True
			else:
				if elapsed >= MOVE_TIME:
					pause = False
					elapsed = 0

			pygame.event.clear([pygame.KEYDOWN, pygame.KEYUP]) #ignore events when clicking during CPU turn
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)

		elif game.current_player == 1: #Player turn
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == K_ESCAPE:
						sys.exit(0)
					elif event.key == K_UP:
						game.draw_to(screen, 0)
					elif event.key == K_RIGHT:
						game.draw_to(screen, 1)
					elif event.key == K_DOWN:
						game.draw_to(screen, 2)
					elif event.key == K_LEFT:
						game.draw_to(screen, 3)
				elif event.type == pygame.KEYUP:
					if event.key == K_UP:
						game.draw_from(screen, 0)
					elif event.key == K_RIGHT:
						game.draw_from(screen, 1)
					elif event.key == K_DOWN:
						game.draw_from(screen, 2)
					elif event.key == K_LEFT:
						game.draw_from(screen, 3)

					if len(game.cpu_moves) == len(game.player_moves):
						game.check_solution()
						game.generate_moves()
						game.toggle_turn()
						game.update_score(screen)
						elapsed = 0
						i = 0
						last = 0
						drawn = False

		pygame.display.flip()

if __name__== "__main__":
    main()