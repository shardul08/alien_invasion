import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class to represent a single alien in the fleet."""
	
	def __init__(self, ai_settings, screen):
		"""Initialize the alien and set its starting position."""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
	
		# Load an alien image and set its rect attribute.
		self.image = pygame.image.load('images/alien.png')
		self.rect = self.image.get_rect()
		
		# Start each new alien near the top left corner.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		# Store alien'sexact position
		self.x = float(self.rect.x)
		
	def blitme(self):
		"""Draw the alien at its current location."""
		self.screen.blit(self.image, self.rect)
