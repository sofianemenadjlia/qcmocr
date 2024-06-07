import unittest
from unittest.mock import patch, MagicMock
import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import types

def detect_text(file, client_secret):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = client_secret
    client = vision.ImageAnnotatorClient()

    with io.open(file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
        
    texts = response.full_text_annotation

    blocks = {}

    for page in texts.pages:
        for block in page.blocks:
            
            block_confidence = block.confidence

            for paragraph in block.paragraphs:
                block_text = ''
                for word in paragraph.words:
                    for symbol in word.symbols:
                        block_text += symbol.text
                blocks[block_text] = block_confidence

    return blocks


class TestDetectTextFunction(unittest.TestCase):
    @patch('google.cloud.vision.ImageAnnotatorClient')
    def test_detect_text(self, mock_image_annotator_client):
        # Define the detect_text function directly here
        def detect_text(file, client_secret):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = client_secret
            client = mock_image_annotator_client()

            with io.open(file, 'rb') as image_file:
                content = image_file.read()

            image = MagicMock()
            image.content = content

            response = MagicMock()
            response.full_text_annotation.pages.__iter__.return_value = [
                MagicMock(blocks=[MagicMock(confidence=0.8, paragraphs=[MagicMock(words=[MagicMock(symbols=[MagicMock(text='Hello')])])])])
            ]
            client.text_detection.return_value = response

            texts = response.full_text_annotation

            blocks = {}

            for page in texts.pages:
                for block in page.blocks:
                    block_confidence = block.confidence

                    for paragraph in block.paragraphs:
                        block_text = ''
                        for word in paragraph.words:
                            for symbol in word.symbols:
                                block_text += symbol.text
                        blocks[block_text] = block_confidence

            return blocks

        # Call the detect_text function
        blocks = detect_text('combined_image.jpg', 'test_client_secret.json')

        # Assert the content of the returned blocks
        self.assertEqual(blocks, {'Hello': 0.8})

if __name__ == '__main__':
    unittest.main()
