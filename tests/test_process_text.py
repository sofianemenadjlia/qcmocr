import unittest

def process_text(blocks, ids):
    processed_blocks = {}
    id = 0

    for block, confidence in blocks.items():
        
        cleaned_text = ''.join([c for c in block if c.isdigit()])
        num_digits = len(cleaned_text)

        for i in range(0, num_digits, 8):
            chunk = cleaned_text[i:i+8]
            if len(chunk) >= 4 and chunk not in processed_blocks.keys():
                processed_blocks[chunk] = ids[id]
                id += 1
                
    return processed_blocks


class TestProcessTextFunction(unittest.TestCase):
    def test_process_text(self):
        # Example input blocks and IDs
        blocks = {
            '1234567890': 0.8,
            'abc123def456ghi': 0.7,
            '78901234': 0.9
        }
        ids = ['id1', 'id2', 'id3']

        # Call the process_text function
        processed_blocks = process_text(blocks, ids)

        # Define the expected output
        expected_processed_blocks = {
            '12345678': 'id1',
            '123456' : 'id2',
            '78901234': 'id3'
        }

        # Assert the content of the returned processed_blocks
        self.assertEqual(processed_blocks, expected_processed_blocks)

        # Additional assertion to check the length of processed blocks
        for block, _ in processed_blocks.items():
            self.assertTrue(4 <= len(block) <= 8, f"Length of processed block '{block}' is not between 4 and 8.")

if __name__ == '__main__':
    unittest.main()