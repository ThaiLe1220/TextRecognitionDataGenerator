from trdg.generators import (
    GeneratorFromStrings,
)
from tqdm.auto import tqdm
import os
import pandas as pd
import numpy as np
import random
import re


NUM_IMAGES_TO_SAVE = 20  # Number of images to generate
LANGUAGE = "en"  # Language


def margin_gen():
    """
    Generates a single tuple of 4 random integers between 0 and 10 (inclusive).
    """
    return tuple(random.randint(0, 10) for _ in range(4))


def color_gen():
    """
    Generates a random RGB color in hexadecimal format.
    """
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    hex_string = f"#{r:02x}{g:02x}{b:02x}"
    return hex_string


def get_orientation_with_bias(bias_for_zero=0.7):
    """
    Generates a random integer 0 or 1 with a bias towards 0.
    """

    # Generate a random number between 0 and 1.
    random_number = random.random()

    # If the random number is less than the bias for 0, return 0.
    # Otherwise, return 1.
    if random_number < bias_for_zero:
        return 0
    else:
        return 1


def generate_image(text, generator):
    """
    Generates an image with the given text and saves it along with its label.
    """

    img, lbl = next(generator)  # Get the next image and its label from the generator
    current_index = (
        len(os.listdir(f"output/{LANGUAGE}")) - 1
    )  # Determine the image index
    image_filename = f"output/{LANGUAGE}/image{current_index}.png"

    img.save(image_filename)  # Save the image

    with open(
        f"output/{LANGUAGE}/labels.txt", "a", encoding="utf-8"
    ) as f:  # Open labels file in append mode
        f.write(f"{image_filename} {lbl}\n")  # Write filename and label


# Main image generation logic
if __name__ == "__main__":

    # Load text from the source file
    all_combinations = []
    with open(f"source/source-{LANGUAGE}.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:
                line = " ".join(line.split())  # Normalize spacing
                all_combinations.append(line)

    # print(len(all_combinations))  # Print the number of text lines

    # Select a random sample of texts for image generation
    all_texts = random.sample(all_combinations, NUM_IMAGES_TO_SAVE)

    # Create output folders if they don't exist
    output_folder = f"output/{LANGUAGE}"  # Store the complete output path
    os.makedirs(output_folder, exist_ok=True)  # Create all folders in the path

    # Create output folders if they don't exist
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists(f"output/{LANGUAGE}/labels.txt"):
        open(
            f"output/{LANGUAGE}/labels.txt", "w", encoding="utf-8"
        ).close()  # Create an empty labels file with UTF-8 encoding

    # Generate images in batches of 10
    for i in range(0, NUM_IMAGES_TO_SAVE, 5):
        # Slice the list of texts into a batch of 10
        texts_batch = all_texts[i : i + 5]

        # Create a new image generator specifically for the current batch
        generator = GeneratorFromStrings(
            texts_batch,
            blur=random.uniform(0, 2),  # Add a slight blur effect randomly
            size=random.randint(50, 100),  # Vary the text size randomly
            skewing_angle=random.randint(0, 20),  # Degree of potential skewing randomly
            language=LANGUAGE,  # Configure for Chinese characters
            orientation=get_orientation_with_bias(
                bias_for_zero=0.8
            ),  # Randomly choose horizontal/vertical orientation 80% bias for 0
            text_color=color_gen(),  # Assign a random text color
            is_handwritten=False,  # Specify machine-printed style
            background_type=random.randint(0, 3),
            distorsion_type=random.randint(0, 3),
            distorsion_orientation=random.randint(0, 1),
            margins=margin_gen(),
        )

        # Process each text within the batch
        for text in texts_batch:
            if len(text) > 40:  # Check if text length exceeds 20 characters
                generator.size = random.randint(100, 150)  # Assign a larger size range
                generator.blur = random.uniform(0, 0.5)  # Assign a smaller blur range

            elif len(text) > 80:  # Check if text length exceeds 20 characters
                generator.size = random.randint(150, 250)  # Assign a larger size range
                generator.blur = 0  # Assign a smaller blur range
                generator.distorsion_orientation = 0
                distorsion_type = 0

            generate_image(
                text, generator
            )  # Create and save an image using the current generator
