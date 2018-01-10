class Settings():
	"""A class to store all settings for Alien Invasion."""
	
	def __init__(self):
		"""Initialize game settings"""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 710
		self.bg_color = (230, 230, 230)
		
		# Ship seetings
		self.ship_speed_factor = 1.5
		
		# Bullet settings
		self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 250,0,0
		self.bullets_allowed = 3
		
		# Alien settings
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10
		# Fleet direction 1 is right, -1 is left
		self.fleet_direction = 	1
