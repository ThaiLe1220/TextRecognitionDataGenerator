from trdg.generators import (
    GeneratorFromStrings,
)
from tqdm.auto import tqdm
import os
import pandas as pd
import numpy as np
import random
import re


NUM_IMAGES_TO_SAVE = 10000  # Number of images to generate
LANGUAGE = "en"  # Language


def margin_gen():
    """
    Generates a single tuple of 4 random integers between 0 and 10 (inclusive).
    """
    return tuple(random.randint(0, 20) for _ in range(4))


def color_gen():
    """
    Generates a random RGB color in hexadecimal format.
    """
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    hex_string = f"#{r:02x}{g:02x}{b:02x}"
    return hex_string


def get_orientation_with_bias(bias_for_zero=0.9):
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
        len(os.listdir(f"output1/{LANGUAGE}")) - 1
    )  # Determine the image index
    image_filename = f"output1/{LANGUAGE}/image{current_index}.png"

    img.save(image_filename)  # Save the image

    with open(
        f"output1/{LANGUAGE}/labels.txt", "a", encoding="utf-8"
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

    # Create output1 folders if they don't exist
    output1_folder = f"output1/{LANGUAGE}"  # Store the complete output1 path
    os.makedirs(output1_folder, exist_ok=True)  # Create all folders in the path

    # Create output1 folders if they don't exist
    if not os.path.exists("output1"):
        os.makedirs("output1")
    if not os.path.exists(f"output1/{LANGUAGE}/labels.txt"):
        open(
            f"output1/{LANGUAGE}/labels.txt", "w", encoding="utf-8"
        ).close()  # Create an empty labels file with UTF-8 encoding

    # Generate images in batches of 5
    for i in range(0, NUM_IMAGES_TO_SAVE, 5):
        # Slice the list of texts into a batch of 5
        texts_batch = all_texts[i : i + 5]

        # Create a new image generator specifically for the current batch
        generator = GeneratorFromStrings(
            texts_batch,  # A batch of text strings to be used in the generated images
            blur=random.randint(0, 1),
            skewing_angle=random.randint(0, 30),  # Randomly skew text up to 30 degrees
            random_skew=True,
            language=LANGUAGE,
            # orientation=get_orientation_with_bias(bias_for_zero=0.9),
            text_color=color_gen(),  # Assign a randomly generated text color
            is_handwritten=True,  # Specify a machine-printed font style
            background_type=random.randint(0, 3),  # Select a random background type
            distorsion_type=random.randint(0, 3),  # Select a random distortion type
            distorsion_orientation=random.randint(0, 2),  # distortion orientation
            margins=margin_gen(),  # Get randomly generated margins for the text
            alignment=random.randint(0, 2),  # Select a random alignment
            character_spacing=random.randint(0, 1),  # Select a random character spacing
            space_width=random.uniform(1, 2),  # Select a random space width
        )

        # Process each text within the batch
        for text in texts_batch:
            if generator.background_type == 3:
                distorsion_type = random.randint(0, 2)

            if len(text) > 40:
                generator.size = random.randint(150, 225)

                if len(text) > 80:
                    continue

            else:
                generator.size = random.randint(75, 150)

            # Attempt image generation and handle potential errors
            try:
                generate_image(text, generator)
                print(f"Img created -[{len(text)}]- '{text}'")

            except Exception as e:
                print(f"Image generation failed for text: {text}. Error: {e}")
