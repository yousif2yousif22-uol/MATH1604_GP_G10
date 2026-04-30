"""
data_extraction_M1.py

Team Member 1 - Parsing Module

This file is responsible for:
1. Reading a respondent's answer file
2. Extracting their answers into a list
3. Saving that list into a new text file
"""

import os
import re


def extract_answers_sequence(file_path):
    """
    This function reads a quiz response file and extracts the selected answers.

    Each question has 4 options:
    - If one option is selected -> return 1, 2, 3, or 4
    - If none are selected -> return 0

    The final result should be a list of 100 numbers.
    """

    # check if the file exists before trying to open it
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # read all lines from the file
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    answers = []  # this will store the final answers
    i = 0  # index to go through lines

    # go through the file line by line
    while i < len(lines):
        line = lines[i].strip()

        # check if this line starts a new question
        if line.startswith("Question"):
            options = []
            j = i + 1

            # collect the next 4 answer lines
            while j < len(lines) and len(options) < 4:
                current_line = lines[j].strip()

                # answer lines always start with [
                if current_line.startswith("["):
                    options.append(current_line)

                j += 1

            # if we didn’t find exactly 4 options, something is wrong
            if len(options) != 4:
                raise ValueError(f"Question formatting error near line {i + 1}")

            selected = 0  # default = unanswered

            # loop through the 4 options to find which one is selected
            for index, option in enumerate(options):
                if "[x]" in option.lower():  # check for x (case insensitive)
                    selected = index + 1  # convert index (0-3) -> option (1-4)
                    break

            # add the result for this question
            answers.append(selected)

            # move to next question block
            i = j

        else:
            # if not a question line, just move to next line
            i += 1

    # final check: we should have exactly 100 answers
    if len(answers) != 100:
        raise ValueError(f"Expected 100 questions, but got {len(answers)}")

    return answers


def write_answers_sequence(answers, n, destination_path):
    """
    This function saves the extracted answers into a text file.

    Each answer is written on a new line.
    File name format: answers_list_respondent_n.txt
    """

    # basic checks to avoid errors later
    if not isinstance(answers, list):
        raise TypeError("answers must be a list")

    if len(answers) != 100:
        raise ValueError("answers list must contain 100 values")

    if not isinstance(n, int) or n <= 0:
        raise ValueError("respondent ID must be a positive integer")

    # create the output folder if it doesn’t exist
    os.makedirs(destination_path, exist_ok=True)

    # create full file path
    filename = f"answers_list_respondent_{n}.txt"
    file_path = os.path.join(destination_path, filename)

    # write answers to file (one per line)
    with open(file_path, "w", encoding="utf-8") as file:
        for answer in answers:
            file.write(str(answer) + "\n")


# simple test (only runs if this file is executed directly)
if __name__ == "__main__":
    try:
        # example input file
      project_folder = os.path.dirname(os.path.abspath(__file__))
      data_folder = os.path.join(project_folder, "data")
      output_folder = os.path.join(project_folder, "output")

      processed_count = 0
        
      for n in [1, 64]:
          input_file = os.path.join(data_folder, f"a{n}.txt")

          if not os.path.isfile(input_file):
              print(f"Skipping missing file: a{n}.txt")
              continue

          answers = extract_answers_sequence(input_file)
          write_answers_sequence(answers, n, output_folder)

          print(f"Processed respondent {n}")
          processed_count += 1

        print(f"Finished processing {processed_count} file(s).")

    except Exception as e:
        print("Error:", e)

    # I used a while loop here instead of a for loop because
    # the number of lines per question can vary slightly
