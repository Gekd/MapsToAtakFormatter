import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests

class ImageCreation:
    """Class to create images with numbers.
	This class downloads a font from a given URL and uses the Pillow library to generate images. 
	The images have a transparent background, rounded corners, and are saved to the specified directory.
    
    Attributes:
		image_height 	(int): The height of the image in pixels.
		font_url 		(str): The URL to download the font from.
		font_height 	(int): The height of the font in pixels.
        
    Methods:
		get_font(url, height): Fetch the font file from the URL and return a PIL ImageFont object.
		draw(number, name, color, dir_path): Draw image with number.
    """
    def __init__(self, image_height, font_url, font_height):
        self.height = image_height
        self.font_url = font_url
        self.font_height = font_height
        self.font = self.get_font(font_url, font_height)
        self.colors = {
            "blue" : (60, 160, 230),
            "red" : (145, 40, 40),
            "white" : (255, 255, 255),
            "yellow" : (255, 255, 30),
            "black" : (0, 0, 0),
            "green" : (55, 165, 50),
            }


    def get_font(self, url, height) -> ImageFont:
        """Fetch the font file from the URL and return a PIL ImageFont object."""
        response = requests.get(url, timeout=10)
        return ImageFont.truetype(BytesIO(response.content), height)


    def draw(self, number, name, color, dir_path):
        """Draw image with number.

        Keyword arguments:
    		number -- the number to be drawn on the image
    		name -- the name of the image file (without the extension)
    		color -- the color name of the image's background
    		height -- the height of the image in pixels
    		dir_path -- the directory path where the image will be saved
    	"""

    	# Width to height ratio of the font, you might need to adjust it for different fonts
        char_width = 0.55

    	# Calculate the width of the image based on how many digits the number has
        number_length = len(str(abs(number)))
    	# 8px is for padding
        image_width = round(self.font_height*number_length*char_width) + 8

    	# Create new image with transparent background
        img = Image.new('RGB', (image_width,self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

    	# W-1 and H-1 are used to avoid drawing outside the image
        draw.rounded_rectangle((0, 0, image_width-1, self.height-1),
                               fill=self.colors[color],
                               outline=self.colors["white"],
                               width=1,
                               radius=4)

		# Draw the number in the center of the image
        draw.text((4, 4), str(number),
                  font=self.font,
                # Black is used for white and yellow numbers, white is used for other darker colors
                  fill=self.colors["black"] if color in ["white", "yellow"] else self.colors["white"])

    	# Save the image
        img.save(os.path.join(dir_path, str(name) + '.png'))
