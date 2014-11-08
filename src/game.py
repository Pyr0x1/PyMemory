import pygame
from pygame.locals import *
from colors import *
from random import randrange

class Game:
	""" Main game class, handling game drawing and logic """

	def __init__(self, width, height):
		""" Initializes data structures """

		self.screen_size = (width, height)
		self.player_square_size = self.screen_size[0] / 10
		self.square_size = self.player_square_size / 2

		self.positions = ((self.screen_size[0] / 2, self.screen_size[1] / 5),
						 (4 * self.screen_size[0] / 5, self.screen_size[1] / 2),
						 (self.screen_size[0] / 2, self.screen_size[1] - self.screen_size[1] / 5),
						 (self.screen_size[0] / 5, self.screen_size[1] / 2))

		self.squares = [Rect(self.positions[0][0] - self.square_size / 2, self.positions[0][1] - self.square_size / 2, self.square_size, self.square_size),
					   Rect(self.positions[1][0] - self.square_size / 2, self.positions[1][1] - self.square_size / 2, self.square_size, self.square_size),
					   Rect(self.positions[2][0] - self.square_size / 2, self.positions[2][1] - self.square_size / 2, self.square_size, self.square_size),
					   Rect(self.positions[3][0] - self.square_size / 2, self.positions[3][1] - self.square_size / 2, self.square_size, self.square_size)]

		self.player_square = Rect(self.screen_size[0] / 2 - self.player_square_size / 2, self.screen_size[1] / 2 - self.player_square_size / 2, self.player_square_size, self.player_square_size)

		self.player_square_surface = pygame.Surface((self.player_square_size, self.player_square_size))
		self.square_surface = pygame.Surface((self.square_size, self.square_size))
		self.cpu_surface = pygame.Surface((self.player_square_size, self.player_square_size))

		self.lines_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA, 32)
		self.lines_surface = self.lines_surface.convert_alpha()
		pygame.draw.lines(self.lines_surface, GREY, True, [self.squares[0].center, self.squares[1].center, self.squares[2].center, self.squares[3].center], 5)

		self.font = pygame.font.Font("../data/visitor.ttf", self.screen_size[0] / 5)
		self.credits_font = pygame.font.Font("../data/visitor.ttf", 20)
		self.text = self.font.render(str(0), True, WHITE)

		self.movement = 0
		self.pressed = [False, False, False, False]
		self.level = 1
		self.cpu_moves = []
		self.player_moves = []
		self.current_player = 0

	def draw_all (self, screen):
		""" Draws all game elements (to be used only at the beginning, then use special purpose drawing methods) """

		screen.fill(BLACK)
		screen.blit(self.lines_surface, (0, 0))
		self.square_surface.fill(GREY)
		self.player_square_surface.fill(WHITE)
		screen.blit(self.player_square_surface, self.player_square)
		for square in self.squares:
			screen.blit(self.square_surface, square)

	def draw_to (self, screen, direction):
		""" Special purpose drawing method to draw the movement of player square to a direction """

		if all(item == False for item in self.pressed):
			screen.blit(self.lines_surface, (0, 0))
			self.player_square_surface.fill(BLACK)
			screen.blit(self.player_square_surface, self.player_square)
			if direction == 0:
				self.movement = - (self.player_square.centery - self.positions[0][1])
				self.player_square.move_ip(0, self.movement)
			elif direction == 1:
				self.movement = self.player_square.centerx - self.positions[3][0]
				self.player_square.move_ip(self.movement, 0)
			elif direction == 2:
				self.movement = self.player_square.centery - self.positions[0][1]
				self.player_square.move_ip(0, self.movement)
			elif direction == 3:
				self.movement = - (self.player_square.centery - self.positions[0][1])
				self.player_square.move_ip(self.movement, 0)
			self.player_square_surface.fill(WHITE)
			screen.blit(self.player_square_surface, self.player_square)
			self.pressed[direction] = True

	def draw_from (self, screen, direction):
		""" Special purpose drawing method to draw the movement of player square back to its original position """

		if len([item for item in self.pressed if item == True]) == 1 and self.pressed[direction] == True:
			self.player_square_surface.fill(BLACK)
			screen.blit(self.player_square_surface, self.player_square)
			screen.blit(self.lines_surface, (0, 0))
			if direction == 0:
				self.player_square.move_ip(0, - self.movement)
			elif direction == 1:
				self.player_square.move_ip(- self.movement, 0)
			elif direction == 2:
				self.player_square.move_ip(0, - self.movement)
			elif direction == 3:
				self.player_square.move_ip(- self.movement, 0)
			self.player_square_surface.fill(WHITE)
			screen.blit(self.player_square_surface, self.player_square)
			screen.blit(self.square_surface, self.squares[direction])
			self.pressed[direction] = False
			self.add_player_move(direction)

	def draw_cpu_move (self, screen, direction):
		""" Draws the cpu move in the corresponding direction """

		self.cpu_surface.fill(GREEN)
		coords = (self.squares[direction].centerx - self.player_square_size / 2, self.squares[direction].centery - self.player_square_size / 2)
		screen.blit(self.cpu_surface, coords)

	def delete_cpu_move (self, screen, direction):
		""" Undoes the cpu move """

		coords = (self.squares[direction].centerx - self.player_square_size / 2, self.squares[direction].centery - self.player_square_size / 2)

		self.cpu_surface.fill(BLACK)
		screen.blit(self.cpu_surface, coords)
		screen.blit(self.lines_surface, (0, 0))
		screen.blit(self.square_surface, self.squares[direction])

	def generate_moves (self):
		""" Generates a list with random moves that the player has to reproduce """

		for i in range(self.level):
			self.cpu_moves.append(randrange(4))

	def add_player_move (self, move):
		""" Saves the player move into the list of player moves """

		self.player_moves.append(move)

	def __clear_moves (self):
		""" Resets move lists to play another turn """

		self.cpu_moves = []
		self.player_moves = []

	def check_solution (self):
		""" Checks if the player performed the right moves """

		if cmp(self.cpu_moves, self.player_moves) == 0:
			self.level += 1
			self.__clear_moves()
			return True
		else:
			self.level = 1
			self.__clear_moves()
			return False

	def toggle_turn (self):
		""" Changes player turn """

		if self.current_player == 0:
			self.current_player = 1
		elif self.current_player == 1:
			self.current_player = 0

		return self.current_player

	def update_score (self, screen):
		""" Updates score shown on screen """

		old_text_pos = self.text.get_rect()
		self.text = self.font.render(str(self.level - 1), True, WHITE)
		text_surface = pygame.Surface((old_text_pos.width, old_text_pos.height))
		text_surface.fill(BLACK)
		screen.blit(text_surface, (self.square_size, self.square_size))
		screen.blit(self.text, (self.square_size, self.square_size))

	def draw_credits (self, screen):
		""" Writes credits on the bottom of the window """

		credits = self.credits_font.render("Created by Pyrox", True, WHITE)
		credits_rect = credits.get_rect()
		credits_rect.centerx = self.screen_size[0] / 2
		credits_rect.centery = self.screen_size[1] - self.positions[0][1] + 2 * self.positions[0][1] / 3
		screen.blit(credits, credits_rect)

		version = self.credits_font.render("v0.1", True, WHITE)
		version_rect = version.get_rect()
		version_rect.left = self.square_size
		version_rect.centery = credits_rect.centery
		screen.blit(version, version_rect)