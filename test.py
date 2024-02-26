# import pandas as pd

# # Read the data from the TSV file
# df = pd.read_csv("./source/en/news.tsv", delimiter="\t")

# # Extract the first 4 columns
# extracted_data = df.iloc[:, :4]

# # Write each column to a new text file
# for i in range(1, 4):
#     column_name = df.columns[i]

#     # Remove duplicates for the first two columns
#     if i <= 2:
#         data_to_write = extracted_data.iloc[:, i].drop_duplicates()
#     else:
#         data_to_write = extracted_data.iloc[:, i]

#     data_to_write.to_csv(f"extracted_news_{column_name}.txt", index=False)

# print("Extracted data and saved to separate text files!")


# def combine_and_dedupe_files(file1_path, file2_path, output_file_path):
#     """Combines two text files, removes duplicate lines, and saves the result.

#     Args:
#         file1_path (str): Path to the first text file.
#         file2_path (str): Path to the second text file.
#         output_file_path (str): Path to the output file where the combined content will be saved.
#     """

#     lines_seen = set()  # Keep track of lines to efficiently remove duplicates

#     with open(output_file_path, "w", encoding="utf-8") as outfile:
#         for filepath in [file1_path, file2_path]:
#             with open(filepath, "r", encoding="utf-8") as infile:
#                 for line in infile:
#                     if line not in lines_seen:  # If the line is unique
#                         outfile.write(line)
#                         lines_seen.add(line)


# combine_and_dedupe_files(
#     "extracted_news_col1.txt",
#     "extracted_news_col2.txt",
#     "combined_result.txt",
# )
