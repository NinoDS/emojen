import colorsys
import random
from PIL import Image, ImageDraw

# Constants
EMOJI_SIZE = 200
BACKGROUND_SIZE = 300

# Define a color palette with visually pleasing colors
COLOR_PALETTE = [
    (255, 0, 0),       # Red
    (255, 165, 0),     # Orange
    (255, 255, 0),     # Yellow
    (0, 255, 0),       # Green
    (30, 144, 255),    # Dodger Blue
    (147, 112, 219),   # Medium Purple
    (255, 0, 255),     # Magenta
    (255, 192, 203),   # Pink
    (255, 99, 71),     # Tomato
    (255, 215, 0),     # Gold
    (218, 112, 214),   # Orchid
    (128, 0, 128),     # Purple
]

def generate_random_gradient():
    # Predefined RGB values
    colors = [
        (51, 255, 255),   # Cyan
        (0, 255, 204),    # Green Cyan
        (204, 255, 51),   # Lime Green
        (255, 153, 0),    # Orange
        (255, 0, 204),    # Pink
        (204, 0, 255)     # Purple
    ]

    # Randomly select the first color from the predefined list
    color1 = colors[random.randint(0, len(colors)-1)]

    # Determine the index of the next color in the list
    index = (colors.index(color1) + random.randint(1,2)) % len(colors)

    # Retrieve the next color
    color2 = colors[index]

    return color2, color1



def generate_emoji_path(emoji_char):
    # Generate the emoji path for the provided character
    filename = "-".join(['{:x}'.format(ord(emoji_char[i])) for i in range(len(emoji_char))]) + ".png"
    filepath = f"node_modules/emojiimages/imgs/{filename}"
    return filepath

def generate_background():
    # Generate a random gradient background from the upper left to the bottom right
    background = Image.new("RGB", (BACKGROUND_SIZE, BACKGROUND_SIZE))
    draw = ImageDraw.Draw(background)
    color1, color2 = generate_random_gradient()
    for x in range(BACKGROUND_SIZE):
        for y in range(BACKGROUND_SIZE):
            ratio = (BACKGROUND_SIZE - x + y) / (BACKGROUND_SIZE + BACKGROUND_SIZE)
            r, g, b = interpolate_color(color1, color2, ratio)
            draw.point((x, y), fill=(int(r), int(g), int(b)))
    return background

def interpolate_color(color1, color2, ratio, factor=1.5):
    # Interpolate two colors based on a ratio and factor
    r = int(color1[0] + (color2[0] - color1[0]) * ratio * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * ratio * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * ratio * factor)
    return r, g, b


def place_emoji_on_background(background, emoji_path):
    # Place the emoji image in the middle of the background
    emoji = Image.open(emoji_path).convert("RGBA")  # Convert to RGBA format
    emoji = emoji.resize((EMOJI_SIZE, EMOJI_SIZE), Image.LANCZOS)  # Use LANCZOS for resizing
    x = (BACKGROUND_SIZE - EMOJI_SIZE) // 2
    y = (BACKGROUND_SIZE - EMOJI_SIZE) // 2
    background.paste(emoji, (x, y), emoji)
    return background

# User input for the emoji character
emoji_char = input("Enter the emoji character: ")

for i in range(10):
    # Generate random gradient background
    background = generate_background()

    # Generate emoji path for the provided character
    emoji_path = generate_emoji_path(emoji_char)

    # Place the emoji on the background
    final_image = place_emoji_on_background(background, emoji_path)

    # Save the final image
    final_image.save(f"background_with_emoji_{i}.png")
    print(f"Saved background_with_emoji_{i}.png")
