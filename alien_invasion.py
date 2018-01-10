""""import sys"""

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
"""from alien import Alien"""
import game_functions as gf

def run_game():
	# Initialize game and create screen object.
	# Initialize pygame, settings and screen objects.
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	# Set background colour.
	#bg_color = (230,  230, 230)
	
	# Make a ship.
	ship = Ship(ai_settings, screen)
	# Make a group to store bullets in.
	bullets = Group()
	"""#Make an  alien.
	alien = Alien(ai_settings, screen)"""
	# Make a group of aliens.
	aliens = Group()
	
	# Create a fleet of aliens.
	gf.create_fleet(ai_settings, screen, aliens)
	
	# Start the main loop for the game.
	while True:
		
		"""# Watch for keyboard and mouse events.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()"""
		gf.check_events(ai_settings, screen, ship, bullets)
		ship.update()
		"""bullets.update()
		
		#Get rid of bullets that have disappeared.
		for bullet in bullets.copy():
			if bullet.rect.bottom <= 0:
				bullets.remove(bullet)
		#print(len(bullets))"""
		"""# Redraw the screen during each pass through the loop.
		screen.fill(ai_settings.bg_color)
		ship.blitme()
		
		# Make the most recently drawn screen visible.
		pygame.display.flip()"""
		gf.update_bullets(bullets)
		gf.update_aliens(ai_settings, aliens)
		gf.update_screen(ai_settings, screen, ship, aliens, bullets)

run_game()
