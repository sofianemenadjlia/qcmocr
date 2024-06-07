import unittest
import os
from PIL import Image

def crop(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for filename in os.listdir(source_folder):
        if filename.endswith('.jpg') and filename.startswith('name'):
            file_path = os.path.join(source_folder, filename)
            
            with Image.open(file_path) as img:
                width, height = img.size
                new_width = width // 2
                vertical_crop = (new_width, 0, width, height)
                
                img_cropped = img.crop(vertical_crop)
                
                width, height = img_cropped.size
                new_height = height - (height * 70 // 100)
                horizontal_crop = (0, new_height, width, height)
                
                img_cropped = img_cropped.crop(horizontal_crop)
                
                img_cropped = img_cropped.convert("RGB")
                
                target_path = os.path.join(target_folder, filename) 
                img_cropped.save(target_path)

    print("Cropping completed.")


class TestCropFunction(unittest.TestCase):
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

    def test_crop_function(self):
        # Create a test image
        test_image_path = os.path.join(self.source_folder, 'name_test.jpg')
        test_image = Image.new('RGB', (100, 100), color='white')
        test_image.save(test_image_path)

        # Call the crop function
        crop(self.source_folder, self.target_folder)

        # Check if the cropped image exists in the target folder
        cropped_image_path = os.path.join(self.target_folder, 'name_test.jpg')
        self.assertTrue(os.path.exists(cropped_image_path))

        # Open the cropped image and check its dimensions
        cropped_image = Image.open(cropped_image_path)
        width, height = cropped_image.size
        self.assertEqual(width, 50)  # Width should be half of original
        self.assertEqual(height, 70)  # Height should be 70% of original

if __name__ == '__main__':
    unittest.main()
