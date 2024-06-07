import os
import matplotlib.pyplot as plt
from matching import detect_text, process_text, find_closest_matches


def apply_functions_on_images(input_folders, csv_file_path, client_secret, max_distortion_level):
    
    matches_by_distortion = {folder.split('/')[-1]: [0] * max_distortion_level for folder in input_folders}

    for folder in input_folders:
        for filename in os.listdir(folder):
            if filename.endswith(".jpg"):
                image_path = os.path.join(folder, filename)

                distortion_level = int(filename.split("_")[-1].split(".")[0])

                blocks = detect_text(image_path, client_secret)
                processed_blocks = process_text(blocks)
                matches, _ = find_closest_matches(processed_blocks, csv_file_path)
                filtered_matches = [match for match in matches if match[-1] == 0]

                matches_by_distortion[folder.split('/')[-1]][distortion_level - 1] += len(filtered_matches)

    return matches_by_distortion


def plot_matches(matches_by_distortion):
    distortion_levels = range(1, len(matches_by_distortion['contrast']) + 1)  # Assuming all distortion lists have the same length

    plt.plot(distortion_levels, matches_by_distortion['contrast'], label='Contrast', color='blue')
    plt.plot(distortion_levels, matches_by_distortion['brightness'], label='Brightness', color='green')
    plt.plot(distortion_levels, matches_by_distortion['blur'], label='Blur', color='red')
    plt.plot(distortion_levels, matches_by_distortion['gaussian_noise'], label='Gaussian noise', color='magenta')
    plt.plot(distortion_levels, matches_by_distortion['salt_and_pepper_noise'], label='Salt and pepper noise', color='cyan')
    plt.plot(distortion_levels, matches_by_distortion['speckle_noise'], label='Speckle noise', color='orange')

    plt.xlabel('Distortion Level')
    plt.ylabel('Number of Perfect Matches')
    plt.title('Number of Perfect Matches vs. Distortion Level')
    plt.legend()

    plt.show()


input_folders = ["edited/contrast", "edited/brightness", "edited/blur", "edited/gaussian_noise", "edited/salt_and_pepper_noise", "edited/speckle_noise"]
csv_file_path = "student-list.csv"  # Path to the CSV file containing numbers
client_secret = "client_secrets.json"  # Path to the Google Vision API client secret
max_distortion_level = 25

matches_by_distortion = apply_functions_on_images(input_folders, csv_file_path, client_secret, max_distortion_level)

plot_matches(matches_by_distortion)
