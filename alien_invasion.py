""""import sys"""

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
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
	# Make the play button.
	play_button = Button(ai_settings, screen, 'Play')
	# Set background colour.
	#bg_color = (230,  230, 230)
	
	# Create an instance to store game statistics
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	# Make a ship.
	ship = Ship(ai_settings, screen)
	# Make a group to store bullets in.
	bullets = Group()
	"""#Make an  alien.
	alien = Alien(ai_settings, screen)"""
	# Make a group of aliens.
	aliens = Group()
	
	# Create a fleet of aliens.
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# Start the main loop for the game.
	while True:
		
		"""# Watch for keyboard and mouse events.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()"""
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
		if stats.game_active:
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
			gf.update_bullets(aliens, bullets, ship, stats, sb, ai_settings, screen)
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
