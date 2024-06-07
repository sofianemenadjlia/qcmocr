import unittest
import os
from PIL import Image
import os
from google.cloud import vision
from google.cloud.vision_v1 import types




def merge(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    images_ids = [os.path.join(source_folder, img) for img in os.listdir(source_folder) if img.endswith('.jpg') and img.startswith('name')]
    ids = [img.split('-')[1].split('.jpg')[0] for img in images_ids]
    
    image_paths = []

    for filename in os.listdir(source_folder):
        if filename.endswith(".jpg"):
            image_paths.append(os.path.join(source_folder, filename))

    images = [Image.open(path) for path in image_paths]
    widths, heights = zip(*(img.size for img in images))

    total_height = sum(heights)
    max_width = max(widths)

    combined_image = Image.new("RGB", (max_width, total_height), color='white')

    y_offset = 0

    for img, height in zip(images, heights):
        combined_image.paste(img, (0, y_offset))
        y_offset += height

    combined_image_path = os.path.join(target_folder, "combined_image.jpg")
    combined_image.save(combined_image_path)

    print(f"Combined image saved to {combined_image_path}")

    for img in images:
        img.close()
    return ids

class TestMergeFunction(unittest.TestCase):
    def setUp(self):
        # Create temporary source and target folders
        self.source_folder = 'test_source_folder'
        self.target_folder = 'test_target_folder'
        os.makedirs(self.source_folder, exist_ok=True)
        os.makedirs(self.target_folder, exist_ok=True)

    def tearDown(self):
        # Remove temporary folders and their contents
        for folder in [self.source_folder, self.target_folder]:
            for filename in os.listdir(folder):
                os.remove(os.path.join(folder, filename))
            os.rmdir(folder)

    def create_test_image(self, filename, size):
        # Create a test image
        test_image_path = os.path.join(self.source_folder, filename)
        test_image = Image.new('RGB', size, color='white')
        test_image.save(test_image_path)

    def test_merge_function(self):
        # Create test images with different sizes
        self.create_test_image('name-1.jpg', (100, 50))
        self.create_test_image('name-2.jpg', (100, 70))
        self.create_test_image('name-3.jpg', (100, 80))

        # Call the merge function
        ids = merge(self.source_folder, self.target_folder)

        # Check if the combined image exists in the target folder
        combined_image_path = os.path.join(self.target_folder, "combined_image.jpg")
        self.assertTrue(os.path.exists(combined_image_path))

        # Open the combined image and check its dimensions
        combined_image = Image.open(combined_image_path)
        width, height = combined_image.size
        self.assertEqual(width, 100)  # Width should be maximum of individual images
        self.assertEqual(height, 200)  # Height should be sum of individual images

        # Check the returned IDs
        expected_ids = ['1', '2', '3']
        self.assertEqual(ids, expected_ids)

if __name__ == '__main__':
    unittest.main()