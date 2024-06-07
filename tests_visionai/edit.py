import os
import cv2
import numpy as np
import shutil


from matching import crop, merge


def adjust_contrast(image, contrast_factor):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = np.mean(gray)
    return cv2.convertScaleAbs(image, alpha=contrast_factor, beta=mean * (1 - contrast_factor))


def adjust_brightness(image, brightness_factor):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:,:,2] = np.clip(hsv[:,:,2] * brightness_factor, 0, 255)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def apply_blur(image, kernel_size):
    
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def apply_speckle_noise(image, variance):
    h, w, c = image.shape
    noise = np.random.randn(h, w, c) * variance
    noisy_image = image + image * noise
    return np.clip(noisy_image, 0, 255).astype(np.uint8)


def apply_salt_and_pepper_noise(image, amount):
    h, w, _ = image.shape
    num_salt = np.ceil(amount * image.size * 0.5)
    salt_coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    image[salt_coords[0], salt_coords[1], :] = 255

    num_pepper = np.ceil(amount * image.size * 0.5)
    pepper_coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    image[pepper_coords[0], pepper_coords[1], :] = 0

    return image


def apply_gaussian_noise(image, mean=0, sigma=25):
    h, w, c = image.shape
    gaussian = np.random.normal(mean, sigma, (h, w, c))
    noisy_image = image + gaussian
    return np.clip(noisy_image, 0, 255).astype(np.uint8)

def generate_contrast_levels(images_path, edited_path, num_levels):
    
    if not os.path.exists(edited_path):
        os.makedirs(edited_path)

    image = cv2.imread(images_path)

    max_contrast_factor = 1.0
    min_contrast_factor = 0.0

    contrast_step = (max_contrast_factor - min_contrast_factor) / (num_levels - 1)

    for i in range(num_levels):
        contrast_factor = max_contrast_factor - i * contrast_step
        contrast_adjusted_image = adjust_contrast(image, contrast_factor)
        output_path = os.path.join(edited_path, f"contrast_level_{i+1}.jpg")
        cv2.imwrite(output_path, contrast_adjusted_image)
        

def generate_brightness_levels(images_path, edited_path, num_levels):
    
    if not os.path.exists(edited_path):
        os.makedirs(edited_path)

    image = cv2.imread(images_path)

    max_brightness_factor = 1.0
    min_brightness_factor = 0.0

    brightness_step = (max_brightness_factor - min_brightness_factor) / (num_levels - 1)

    for i in range(num_levels):
        brightness_factor = max_brightness_factor - i * brightness_step
        brightness_adjusted_image = adjust_brightness(image, brightness_factor)
        output_path = os.path.join(edited_path, f"brightness_level_{i+1}.jpg")
        cv2.imwrite(output_path, brightness_adjusted_image)
        
def generate_blur_levels(images_path, edited_path, num_levels):

    if not os.path.exists(edited_path):
        os.makedirs(edited_path)

        image = cv2.imread(images_path)

        max_kernel_size = 75  # You can adjust this value as needed
        min_kernel_size = 1

        kernel_size_step = max_kernel_size / (num_levels - 1)

        for i in range(num_levels):
            kernel_size = max(min(int(i * kernel_size_step), max_kernel_size), min_kernel_size)
            kernel_size = kernel_size + 1 if kernel_size % 2 == 0 else kernel_size  # Ensure odd kernel size
            blurred_image = apply_blur(image, kernel_size)
            output_path = os.path.join(edited_path, f"blur_level_{i+1}.jpg")
            cv2.imwrite(output_path, blurred_image)


def generate_noise_levels(images_path, edited_path, num_levels):
    if not os.path.exists(edited_path):
        os.makedirs(edited_path)

    image = cv2.imread(images_path)

    max_noise_variance = 25
    max_sp_amount = 0.5
    max_gaussian_sigma = 500

    noise_variance_step = max_noise_variance / (num_levels - 1)
    sp_amount_step = max_sp_amount / (num_levels - 1)
    gaussian_sigma_step = max_gaussian_sigma / (num_levels - 1)

    for i in range(num_levels):
        noise_variance = i * noise_variance_step
        sp_amount = i * sp_amount_step
        gaussian_sigma = i * gaussian_sigma_step

        speckle_noisy_image = apply_speckle_noise(image.copy(), noise_variance)
        salt_pepper_noisy_image = apply_salt_and_pepper_noise(image.copy(), sp_amount)
        gaussian_noisy_image = apply_gaussian_noise(image.copy(), sigma=gaussian_sigma)

        speckle_edited_path = os.path.join(edited_path, "speckle_noise")
        salt_pepper_edited_path = os.path.join(edited_path, "salt_and_pepper_noise")
        gaussian_edited_path = os.path.join(edited_path, "gaussian_noise")

        os.makedirs(speckle_edited_path, exist_ok=True)
        os.makedirs(salt_pepper_edited_path, exist_ok=True)
        os.makedirs(gaussian_edited_path, exist_ok=True)

        cv2.imwrite(os.path.join(speckle_edited_path, f"speckle_noise_level_{i+1}.jpg"), speckle_noisy_image)
        cv2.imwrite(os.path.join(salt_pepper_edited_path, f"salt_and_pepper_noise_level_{i+1}.jpg"), salt_pepper_noisy_image)
        cv2.imwrite(os.path.join(gaussian_edited_path, f"gaussian_noise_level_{i+1}.jpg"), gaussian_noisy_image)



images_path = "clean_data"
crops_path = "crops"
merged_path = "merged_images"
merged_image = merged_path + "/combined_image.jpg"
edited_path = "edited"
num_levels = 25
cropping = False

try:
    shutil.rmtree(edited_path)
    shutil.rmtree(crops_path)
    shutil.rmtree(merged_path)
    
except OSError as e:
    print ("No folder to remove")


if cropping:
    crop(images_path, crops_path)
    ids = merge(crops_path, merged_path)

else:
    ids = merge(images_path, merged_path)



generate_brightness_levels(merged_image, edited_path + '/brightness', num_levels)
generate_contrast_levels(merged_image, edited_path + '/contrast', num_levels)
generate_blur_levels(merged_image, edited_path + '/blur', num_levels)
generate_noise_levels(merged_image, edited_path, num_levels)
