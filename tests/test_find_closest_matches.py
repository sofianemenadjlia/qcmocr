import unittest
from unittest.mock import patch
import csv
from Levenshtein import distance as levenshtein_distance

def find_closest_matches(processed_blocks, csv_file_path):
    csv_numbers = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row:
                csv_numbers.append(row[1])

    matches = []
    distances = []
    perfect_matched_csv = set()

    for block, id in processed_blocks.items():
        best_match_within_block = {}
        perfect_match_found = False

        available_csv_numbers = [num for num in csv_numbers if num not in perfect_matched_csv]

        eight_digit_substr = block
        closest_match = None
        closest_distance = float('inf')
        for csv_num in available_csv_numbers:
            dist = levenshtein_distance(eight_digit_substr, csv_num)
            if dist == 0:
                matches.append((eight_digit_substr, csv_num, 0, id))
                distances.append(0)
                closest_match = csv_num
                closest_distance = 0
                perfect_match_found = True
                perfect_matched_csv.add(csv_num)
                break 
            elif dist < closest_distance:
                closest_distance = dist
                closest_match = csv_num

        if closest_match is not None:
            if eight_digit_substr not in best_match_within_block or closest_distance < best_match_within_block[eight_digit_substr][1]:
                best_match_within_block[eight_digit_substr] = (closest_match, closest_distance)

        if perfect_match_found:
            continue

        if best_match_within_block:
            best_match = min(best_match_within_block.values(), key=lambda x: x[1])
            matches.append((block, best_match[0], best_match[1], id))
            distances.append(best_match[1])

    return matches, distances



class TestFindClosestMatchesFunction(unittest.TestCase):
    @patch('builtins.open')
    @patch('csv.reader')
    def test_find_closest_matches(self, mock_csv_reader, mock_open):
        # Mock CSV file path and data
        csv_file_path = 'test.csv'
        mock_open.return_value.__enter__.return_value = [
            ['TOTO Bobo', '22118398', 'toto.bobo@etu.u-bordeaux.fr']
        ]
        mock_csv_reader.return_value = [
            ['TUTU Bubu', '12345678', 'tutu.bubu@etu.u-bordeaux.fr']
        ]

        # Example input processed blocks
        processed_blocks = {
            '2218398': 'id1',
            '12345678': 'id2' 
        }

        # Call the find_closest_matches function
        matches, distances = find_closest_matches(processed_blocks, csv_file_path)
        print (matches)

        # Define the expected output
        expected_matches = [
            ('2218398', '22118398', 1, 'id1'),
            ('12345678', '12345678', 0, 'id2')
        ]
        expected_distances = [1, 1]

        # Assert the content of the returned matches and distances
        # self.assertEqual(matches, expected_matches)
        # self.assertEqual(distances, expected_distances)

if __name__ == '__main__':
    unittest.main()