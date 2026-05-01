import matplotlib.pyplot as plt
from data_extraction_M1 import extract_answers_sequence
import re

#This function works out the mean answer for each of the 100 questions
def generate_means_sequence(collated_answers_path):
    """
    This function works out the mean answer value for each question across all the respondents.
    It reads the collated answers file and each respondents answers are parsed using the function from the M1 module
    For each of the 100 questions, this function calculates the mean of the selected answers, excluding unanswered questions.
    It returns a list of floats, with length 100 where each element represents the mean answer value for each question.
    It will also return an error if the collated answers file cannot be found or if an error occurs while reading the file
    """
    # Opens the file for the collated answers
    with open(collated_answers_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into respondents
    respondents = [
    r.strip()
    for r in re.split(r"\n\s*\*\s*\n", text)
    if r.strip()
]

    all_sequences = []
  
    for respondent in respondents:
        # Write respondent temporarily to file 
        temp_path = "temp_respondent.txt"
        with open(temp_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(respondent)
        sequence = extract_answers_sequence(temp_path)
        all_sequences.append(sequence)

    means = []

    for i in range(100):
        values = []
        for seq in all_sequences:
            if seq[i] != 0:
                values.append(seq[i])

        if values:
            means.append(sum(values) / len(values))
        else:
            means.append(0.0)

    return means


def visualize_data(collated_answers_path, n):
    """
    This function visualises the data from the collated answers file.
    It reads the file and generates a plot based on the selected mode:
    1. if n ==1, it displays a scatter plot of the mean answer for each question
    2. if n ==2, it displays a line plot of all respondent answer sequences on the same axes
    3. if n is not 1 or 2, it prints an error message
    The function depends on the generate_means_sequence (for n ==1) and extract_answers_sequence from M1.
    """

    # Read file
    with open(collated_answers_path, "r", encoding="utf-8") as f:
        text = f.read()

    respondents = [
    r.strip()
    for r in re.split(r"\n\s*\*\s*\n", text)
    if r.strip()
]

    all_sequences = []

    # Extract sequences using M1
    for respondent in respondents:
        temp_path = "temp_respondent.txt"
        with open(temp_path, "w", encoding="utf-8") as temp_file:
            temp_file.write(respondent)

        sequence = extract_answers_sequence(temp_path)
        all_sequences.append(sequence)

    x = list(range(1, 101))

    if n == 1:
        means = generate_means_sequence(collated_answers_path)

        plt.scatter(x, means)
        plt.xlabel("Question number")
        plt.ylabel("Mean answer")
        plt.title("Mean Answer per Question")
        plt.show()

    elif n == 2:
        for seq in all_sequences:
            plt.plot(x, seq, alpha=0.5)

        plt.xlabel("Question number")
        plt.ylabel("Answer value")
        plt.title("All Respondent Answer Sequences")
        plt.show()

    else:
        print("Error: n must be 1 or 2")
    
