from trdg.generators import (
    GeneratorFromStrings,
)
from tqdm.auto import tqdm
import os
import pandas as pd
import numpy as np
import random
import re


def color_gen():
    """Generates a random RGB color in hexadecimal format."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    hex_string = f"#{r:02x}{g:02x}{b:02x}"
    return hex_string


def generate_image(text, generator):
    """Generates an image with the given text and saves it along with its label.

    Args:
        text (str): The text to be displayed in the image.
        generator (GeneratorFromStrings): The image generator object.
    """

    img, lbl = next(generator)  # Get the next image and its label from the generator
    current_index = len(os.listdir("output")) - 1  # Determine the image index
    image_filename = f"output/image{current_index}.png"

    img.save(image_filename)  # Save the image

    with open("output/labels.txt", "a") as f:  # Open labels file in append mode
        f.write(f"{image_filename} {lbl}\n")  # Write filename and label


# Main image generation logic
if __name__ == "__main__":
    NUM_IMAGES_TO_SAVE = 90  # Number of images to generate

    # Load text from the source file
    all_combinations = []
    with open("source.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:
                line = " ".join(line.split())  # Normalize spacing
                all_combinations.append(line)

    print(len(all_combinations))  # Print the number of text lines

    # Select a random sample of texts for image generation
    all_texts = random.sample(all_combinations, NUM_IMAGES_TO_SAVE)

    # Create output folders if they don't exist
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists("output/labels.txt"):
        open("output/labels.txt", "w").close()  # Create an empty labels file

    # Generate images in batches of 10
    for i in range(0, NUM_IMAGES_TO_SAVE, 10):
        # Slice the list of texts into a batch of 10
        texts_batch = all_texts[i : i + 10]

        # Create a new image generator specifically for the current batch
        generator = GeneratorFromStrings(
            texts_batch,
            blur=2,  # Add a slight blur effect
            size=random.randint(40, 60),  # Vary the text size randomly
            language="cn",  # Configure for Chinese characters
            random_blur=True,  # Enable random variations in blur
            random_skew=True,  # Introduce random skewing of the text
            orientation=random.randint(
                0, 1
            ),  # Randomly choose horizontal/vertical orientation
            skewing_angle=10,  # Degree of potential skewing
            background_type=1,  # Select background type (refer to trdg documentation)
            text_color=color_gen(),  # Assign a random text color
            is_handwritten=False,  # Specify machine-printed style
        )

        # Process each text within the batch
        for text in texts_batch:
            generate_image(
                text, generator
            )  # Create and save an image using the current generator
