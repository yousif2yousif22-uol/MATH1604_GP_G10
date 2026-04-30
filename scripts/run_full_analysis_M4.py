"""
run_full_analysis_M4.py
---
this script integrates all modules from the team to run the full analysis:
    - downloading and collating answer files, from M2
    - extracting answer sequences from each answer file, from M1
    - statistics and visualizations, from M3
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_extraction_M1 import extract_answers_sequence, write_answers_sequence
from data_preparation_M2 import download_answer_files, collate_answer_files
from data_analysis_M3 import generate_means_sequence, visualize_data

CLOUD_URL = "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"
NUM_RESPONDENTS = 70


# paths
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(repo_root, "data")
output_folder = os.path.join(repo_root, "output")
collated_file = os.path.join(output_folder, "collated_answers.txt")


# set up
def setup_folders():
    """
    ensuring that the data/ and output/ folders exist,
    creates them if they dont.
    """
    os.makedirs(data_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    print("folders are ready!")

# step 1
def step1_download_collate():
    """
    step 1: using M2's module to download all answer files and collate into one.
    """
    print("\nStep 1: downloading answer files from cloud.")
    download_answer_files(CLOUD_URL, data_folder, NUM_RESPONDENTS)
    print("download complete!")

    print("Step 1: collating answer files.")
    original_dir = os.getcwd()
    os.chdir(repo_root)
    collate_answer_files(data_folder)
    os.chdir(original_dir)
    print(f"collated file saved to {collated_file}")

# step 2
def step2_extract_seq():
    """
    step 2: looping through all answer files in the data folder, using
    # M1's extract_answers_sequence() to parse files, and saves using 
    write_answers_sequence()

    noting that, M1's write_answers_sequence() takes three parameters
    (destination_path was added)
    """
    print("\nStep 2: extracting answer sequences.")

    all_sequences = []

    for n in range(1, NUM_RESPONDENTS + 1):
        file_path = os.path.join(data_folder, f"answers_respondent_{n}.txt")

        if not os.path.exists(file_path):
            print(f" file not found! answers_respondent_{n}.txt - will be skipped.")
            continue

        sequence = extract_answers_sequence(file_path)
        write_answers_sequence(sequence, n, output_folder)
        all_sequences.append(sequence)
        print(f"respondent {n}: extracted {len(sequence)} answers")

    print(f"extracted sequences for {len(all_sequences)} respondents")
    return all_sequences


def step3_analyse_visualize():
    """
    step 3: using M3's module to compute the mean answer per
    questions and visualizing results.

    - generate_means_sequence() returns the mean per question.
    - visualize_data() produces a scatter plot of means (n=1) and a line plot 
    of all individual answer sequences (n=2)
    """
    print("\nStep 3: computing means sequence.")
    means = generate_means_sequence(collated_file)
    print(f"means of {len(means)} questions computed.")

    print("Step 3: generating scatter plot (n=1).")
    visualize_data(collated_file, 1)

    print("Step 3: generating line plot (n=2).")
    visualize_data(collated_file, 2)

    print("visualization complete")


def main():
    """
    function for running the full analysis pipeline in order:
      - seting up folders
      - downloading and collating
      - extracting answer sequences from each file
      - analyzing and visualizing patterns
    """
    print("=" * 55)
    print("  MATH1604 - Python Quiz Response Analysis Pipeline")
    print("  Member 4 - Integration Script")
    print("=" * 55)

    setup_folders()
    step1_download_collate()
    step2_extract_seq()
    step3_analyse_visualize()

    print("\n" + "=" * 55)
    print("pipeline complete.")
    print("=" * 55)

if __name__ == "__main__":
    main()
