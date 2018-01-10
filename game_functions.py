import sys

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, ship, screen, bullets):
	"""Respond to keypresses."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		"""# Create a new bullet and add it to bullets group.
		if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)"""
		fire_bullet(ai_settings, ship, screen, bullets)	
	elif event.key == pygame.K_q:
			sys.exit()
		
def check_keyup_events(event, ship):
	"""Respond to key realeases."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		
def check_events(ai_settings, screen, ship, bullets):
	"""Respond to keypress and mouse events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:
			"""if event.key == pygame.K_RIGHT:
			# Move to right.
			ship.rect.centerx += 1"""
			"""ship.moving_right = True
			elif event.key == pygame.K_LEFT:
			ship.moving_left = True"""
			check_keydown_events(event, ai_settings, ship, screen, bullets)

		elif event.type == pygame.KEYUP:
			"""if event.key == pygame.K_RIGHT:
			ship.moving_right = False
			elif event.key == pygame.K_LEFT:
			ship.moving_left = False"""
			check_keyup_events(event, ship)	

def update_screen(ai_settings, screen, ship, aliens, bullets):
	"""Update images on the screen and flip to the new screen."""
	# Redraw the screen during each pass through the loop.
	screen.fill(ai_settings.bg_color)
	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	"""alien.blitme()"""
	aliens.draw(screen)
	
	# Make the most recently drawn screen visible.
	pygame.display.flip()
	
def update_bullets(bullets):
	"""Update position of bullets and get rid of old bullets."""
	# Update bullet position
	bullets.update()
	
	#Get rid of bullets that have disappeared.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
def fire_bullet(ai_settings, ship, screen, bullets):
	"""Fire a bullet if limit not reached yet."""
	# Create a new bullet and add it to bullets group.
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def create_fleet(ai_settings, screen, aliens):
	"""Create a fullfleet of aliens."""
	# Create an alien and find number of aliens in a row.
	# Spacing between each alien is one alien width.
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x/(2 * alien_width))
	
	# Create the first row of aliens.
	for alien_number in range(number_aliens_x):
		# Create an alien and place it in the row.
		alien = Alien(ai_settings, screen)
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		aliens.add(alien)
		
def update_aliens(ai_settings, aliens):
	"""
		Check if alien is in the edge of the screen,
		and then uodate the position of all the aliens in the fleet.
	"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
def check_fleet_edges(ai_settings, aliens):
	"""Respond appropriately if any alien has reached adge."""
	for alien in  aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
	
def change_fleet_direction(ai_settings, aliens):
	"""Drop the ento=ire fleetandchange alien's direction."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	 