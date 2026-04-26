"""
data_preparation_M2.py

This module contains the Team Member 2 functions for the MATH1604 group project.
It downloads raw respondent answer files from the cloud and collates the downloaded
files into one output file for later analysis.
"""

import os
import urllib.request
import urllib.error


def download_answer_files(cloud_url, path_to_data_folder, total_respondents):
    """
    Download respondent answer files from a cloud URL and save them locally.

    The cloud files are assumed to be named a1.txt, a2.txt, ..., aN.txt.
    Downloaded files are saved in the local data folder as
    answers_respondent_1.txt, answers_respondent_2.txt, ..., answers_respondent_N.txt.

    Parameters
    ----------
    cloud_url : str
        The base URL containing the respondent files.
    path_to_data_folder : str
        The local folder path where the downloaded files should be saved.
    total_respondents : int
        The number of respondent files to attempt to download.

    Returns
    -------
    None
        The function writes downloaded files into path_to_data_folder.

    Raises
    ------
    ValueError
        If total_respondents is not a positive integer.
    """

    if not isinstance(total_respondents, int) or total_respondents <= 0:
        raise ValueError("total_respondents must be a positive integer.")

    os.makedirs(path_to_data_folder, exist_ok=True)
    cloud_url = cloud_url.rstrip("/")

    for respondent_id in range(1, total_respondents + 1):
        source_url = f"{cloud_url}/a{respondent_id}.txt"
        output_filename = f"answers_respondent_{respondent_id}.txt"
        output_path = os.path.join(path_to_data_folder, output_filename)

        try:
            urllib.request.urlretrieve(source_url, output_path)
            print(f"Downloaded: a{respondent_id}.txt -> {output_path}")

        except urllib.error.HTTPError as error:
            print(f"Could not download a{respondent_id}.txt: HTTP error {error.code}")

        except urllib.error.URLError as error:
            print(f"Could not download a{respondent_id}.txt: URL error {error.reason}")


def collate_answer_files(data_folder_path):
    """
    Collate downloaded respondent answer files into one output file.

    The function reads files named answers_respondent_1.txt,
    answers_respondent_2.txt, ... from the given data folder. It combines their
    contents into output/collated_answers.txt. Each respondent section is separated
    by a line containing one asterisk (*).

    Parameters
    ----------
    data_folder_path : str
        The folder containing the downloaded respondent files.

    Returns
    -------
    None
        The function writes the collated file to output/collated_answers.txt.

    Raises
    ------
    FileNotFoundError
        If data_folder_path does not exist.
    """

    if not os.path.isdir(data_folder_path):
        raise FileNotFoundError(f"The folder does not exist: {data_folder_path}")

    os.makedirs("output", exist_ok=True)

    respondent_files = []

    for filename in os.listdir(data_folder_path):
        if filename.startswith("answers_respondent_") and filename.endswith(".txt"):
            respondent_files.append(filename)

    respondent_files.sort(
        key=lambda name: int(
            name.replace("answers_respondent_", "").replace(".txt", "")
        )
    )

    output_path = os.path.join("output", "collated_answers.txt")

    with open(output_path, "w", encoding="utf-8") as output_file:
        for index, filename in enumerate(respondent_files):
            file_path = os.path.join(data_folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as input_file:
                output_file.write(input_file.read().strip())

            if index != len(respondent_files) - 1:
                output_file.write("\n*\n")

    print(f"Collated {len(respondent_files)} files into {output_path}")
