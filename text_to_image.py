# from PIL import Image, ImageDraw, ImageFont

# # Define image properties
# image_size = (100, 150)
# background_color = (255, 255, 255)  # RGB color for the background
# text_color = (0, 0, 0)  # RGB color for the text
# font_size = 15
# font_path = r"D:\ticker_new\Times New Roman\times new roman.ttf"  # Replace with the path to your desired font file
# text = "2023-07-18"  # Replace with your desired text

# # Create a new image with the specified background color
# image = Image.new('RGB', image_size, background_color)

# # Create a draw object
# draw = ImageDraw.Draw(image)

# # Define the font and load it with the specified size
# font = ImageFont.truetype(font_path, font_size)

# # Calculate the position to center the text
# text_width, text_height = draw.textsize(text, font=font)
# position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

# # Draw the text on the image
# draw.text(position, text, font=font, fill=text_color)

# # Apply visual effects (optional)
# # Example: Adding a border
# border_color = (0, 0, 255)  # RGB color for the border
# border_size = 5
# border_box = [(0, 0), (image_size[0] - 1, image_size[1] - 1)]
# draw.rectangle(border_box, outline=border_color, width=border_size)

# # Display the image
# image.show()
from PIL import Image, ImageDraw, ImageFont

def create_text_image(text, font_size=12, image_size=(400, 200), text_color=(0, 0, 0), background_color=(255, 255, 255), font_path=None):
    # Create a new image with the specified size and background color
    image = Image.new("RGB", image_size, background_color)

    # Create a draw object
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the position to center the text
    text_width, text_height = draw.textsize(text, font=font)
    position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

    # Draw the text on the image
    draw.text(position, text, font=font, fill=text_color)

    return image

# Example usage
text = "Hello, World!"
font_size = 36
image_size = (800, 400)
text_color = (0, 0, 0)  # Black
background_color = (255, 255, 255)  # White
font_path = r"D:\ticker_new\Times New Roman\times new roman bold.ttf"  # Replace with the path to your desired font file

image = create_text_image(text, font_size, image_size, text_color, background_color, font_path)
image.show()  # Display the image
