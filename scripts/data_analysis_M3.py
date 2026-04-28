import matplotlib.pyplot as plt
from data_extraction_M1 import extract_answers_sequence

#This function works out the mean answer for each of the 100 questions
def generate_means_sequence(collated_answers_path):

    # Opens the file for the collated answers
    with open(collated_answers_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into respondents
    respondents = [r.strip() for r in text.split("*") if r.strip()]

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

    # Read file
    with open(collated_answers_path, "r", encoding="utf-8") as f:
        text = f.read()

    respondents = [r.strip() for r in text.split("*") if r.strip()]

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
    
