from PIL import Image, ImageDraw
import math
import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import types
import csv
from Levenshtein import distance as levenshtein_distance
import xml.etree.ElementTree as ET
import xml.dom.minidom
import matplotlib.pyplot as plt
import shutil
import sys

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