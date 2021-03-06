import sys
from time import sleep

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
		
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
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
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, mouse_x, mouse_y, ship, aliens, bullets)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	"""Update images on the screen and flip to the new screen."""
	# Redraw the screen during each pass through the loop.
	screen.fill(ai_settings.bg_color)
	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	"""alien.blitme()"""
	aliens.draw(screen)
	# Draw the score information.
	sb.show_score()
	# Draw the play button if the game is inactive.
	if not stats.game_active:
		play_button.draw_button()		
	
	# Make the most recently drawn screen visible.
	pygame.display.flip()
	
def update_bullets(aliens, bullets, ship, stats, sb, ai_settings, screen):
	"""Update position of bullets and get rid of old bullets."""
	# Update bullet position
	bullets.update()
	#Get rid of bullets that have disappeared.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collision(aliens, bullets, ship, stats, sb, ai_settings, screen)
	
def check_bullet_alien_collision(aliens, bullets, ship, stats, sb, ai_settings, screen):
	"""Respond to bullet-alien collision."""
	# Remove any bullet and alien that have collided.
	# Check for any bullets that have hit the aliens.
	# If so, get rid of the bullet and the alien.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	# Create new fleet.
	if len(aliens) == 0:
		# Destroy existing bullets, speed up the game, and create a new fleet.
		bullets.empty()
		ai_settings.increase_speed()
		# Increase level.
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)
			
def fire_bullet(ai_settings, ship, screen, bullets):
	"""Fire a bullet if limit not reached yet."""
	# Create a new bullet and add it to bullets group.
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full fleet of aliens."""
	# Create an alien and find number of aliens in a row.
	# Spacing between each alien is one alien width.
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height) - 1
	
	# Create the fleet of aliens.
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			# Create an alien and place it in the row.
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
		
def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens that fit in a row."""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x/(2 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_setting, ship_height, alien_height):
	"""Determine the number of roes of alien that fit in the screen."""
	available_space_y = (ai_setting.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row."""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

		
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""
		Check if alien is in the edge of the screen,
		and then uodate the position of all the aliens in the fleet.
	"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	# Look for alien-shp collision.
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
		#print("Ship hit!!!")
	# Look for the aliens hitting the botom of the screen.
	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
	
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

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Respond to ship being hit by alien."""
	if stats.ships_left > 0:
		# Decrement ships_left
		stats.ships_left -= 1
		
		# Update scoreboard.
		sb.prep_ships()
		
		# Empty the list of aliens and bullet.
		aliens.empty()
		bullets.empty()
		
		# Create a newfleet and center the ship.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		# Pause
		sleep(0.5)
	else:
		stats.game_active =False
		pygame.mouse.set_visible(True)
	
def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Check if any aliens have reached the bottom  of the screen."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this same as ship hit
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break

def check_play_button(ai_settings, screen, stats, sb, play_button, mouse_x, mouse_y, ship, aliens, bullets):
	"""Start a new game when the player clicks the lay button."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# Reset game settings.
		ai_settings.initialize_dynamic_settings()
		# Hide the mouse cursor.
		pygame.mouse.set_visible(False)
		# Reset game statistics.
		stats.reset_stats()
		stats.game_active = True
		
		# Reset scoreboard images.
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# Emptythe list of aliens and bulets.
		aliens.empty()
		bullets.empty()
			
		# Create a new fleet and center the sheep.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def check_high_score(stats, sb):
	"""Check if there is a new high score."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
