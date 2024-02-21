import os
import random
import re

LANGUAGE = "en"
text_files = os.listdir(f"source/{LANGUAGE}/")

# Create a new text file to store the results
with open("results.txt", "w", encoding="utf-8") as results_file:

    # Loop through each text file
    for text_file in text_files:

        # Open the text file
        with open(f"source/{LANGUAGE}/" + text_file, "r", encoding="utf-8") as t:
            current_line = ""
            max_chunk_size = random.randint(10, 100)

            # Read text file line by line
            for line in t:
                line = line.strip()
                line = line.replace("\n", " ")
                line = re.sub(r"\s+", " ", line)

                new_line = current_line + line

                # Check if adding this line would exceed the max chunk size
                if len(new_line) > max_chunk_size:
                    # Write the current chunk of text
                    results_file.write(current_line + "\n")
                    current_line = line  # Start a new chunk with the current line
                    max_chunk_size = random.randint(10, 100)  # New random size
                else:
                    current_line = new_line  # Continue building the string

            # Write out any remaining text at the end of the file
            if current_line:
                results_file.write(current_line + "\n")
