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

    img, lbl = next(generator)  # Get the next image/label pair
    current_index = len(os.listdir("output")) - 1
    image_filename = f"output/image{current_index}.png"

    img.save(image_filename)

    with open("output/labels.txt", "a") as f:
        f.write(f"{image_filename} {lbl}\n")


# Main image generation logic
if __name__ == "__main__":
    NUM_IMAGES_TO_SAVE = 90

    # now given word list and number list, get all combinations
    all_combinations = []  # Initialize an empty list to store text lines

    with open(
        "source.txt", "r", encoding="utf-8"
    ) as file:  # Open the file in read mode
        for line in file:
            line = line.strip()

            if line:
                line = " ".join(line.split())
                all_combinations.append(line)

    print(len(all_combinations))  # Check how many items are in the list
    all_texts = random.sample(all_combinations, NUM_IMAGES_TO_SAVE)

    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists("output/labels.txt"):
        open("output/labels.txt", "w").close()

    for i in range(0, NUM_IMAGES_TO_SAVE, 10):
        texts_batch = all_texts[i : i + 10]  # Slice 10 sequential texts

        generator = GeneratorFromStrings(
            texts_batch,  # Use the current batch of texts
            blur=2,
            size=random.randint(50, 60),
            language="cn",
            random_blur=True,
            random_skew=True,
            orientation=random.randint(0, 1),
            skewing_angle=10,
            background_type=1,
            text_color=color_gen(),
            is_handwritten=False,
        )

        for text in texts_batch:  # Process each text in the batch
            generate_image(text, generator)
