import os
import numpy as np
from PIL import Image

class LetterRecognizer:
    def __init__(self, folder_path):
        """
        Constructor to load pixel data for all letters from .npy files in a specified folder.
        
        :param folder_path: Path to the folder containing .npy files for letters.
        """
        self.en_letter_data_question = {}  # Dictionary to store English letter data
        self.jp_letter_data_question = {}  # Dictionary to store Japanese letter data
        self.en_letter_data_tf_answer = {}
        self.jp_letter_data_tf_answer = {}
        self.en_letter_data_mc_answer = {}
        self.jp_letter_data_mc_answer = {}

        # Load all .npy files in the folder
        for file_name in os.listdir(folder_path):
            # Extract the letter name from the file (e.g., 'A.npy' -> 'A')
            letter = os.path.splitext(file_name)[0] 
            if file_name.endswith("hira_question.npy"):
                # Load the .npy file and store the data
                self.jp_letter_data_question[letter] = np.load(os.path.join(folder_path, file_name))
            elif file_name.endswith("question.npy"):
                # Load the .npy file and store the data
                self.en_letter_data_question[letter] = np.load(os.path.join(folder_path, file_name))
            elif file_name.endswith("hira_tf_answer.npy"):
                # Load the .npy file and store the data
                self.jp_letter_data_tf_answer[letter] = np.load(os.path.join(folder_path, file_name))
            elif file_name.endswith("tf_answer.npy"):
                # Load the .npy file and store the data
                self.en_letter_data_tf_answer[letter] = np.load(os.path.join(folder_path, file_name))
            elif file_name.endswith("hira_mc_answer.npy"):
                # Load the .npy file and store the data
                self.jp_letter_data_mc_answer[letter] = np.load(os.path.join(folder_path, file_name))
            else:
                # Load the .npy file and store the data
                self.en_letter_data_mc_answer[letter] = np.load(os.path.join(folder_path, file_name))
                
    def process_letter(self,image,roi):
        threshold = 200
        image = image.crop(roi) # left, top, right, bottom
        image = (np.array(image) > threshold).astype(int)*255
        non_empty_rows = np.where(np.any(image != 255, axis=1))[0]
        non_empty_cols = np.where(np.any(image != 255, axis=0))[0]
        if non_empty_rows.size != 0:
            row_start, row_end = non_empty_rows[0], non_empty_rows[-1] + 1
            col_start, col_end = non_empty_cols[0], non_empty_cols[-1] + 1
            image = image[row_start:row_end, col_start:col_end]
        return image.astype(np.uint8)

    def find_letter(self, pixel_data,letter_type):
        size = pixel_data.shape
        if letter_type == "question":
            if np.mean(size) > 25:
                letter_database = self.jp_letter_data_question.items()
            else:
                letter_database = self.en_letter_data_question.items()
        elif letter_type == "tf_answer":
            if np.mean(size) > 25:
                letter_database = self.jp_letter_data_tf_answer.items()
            else:
                letter_database = self.en_letter_data_tf_answer.items()
        else: # letter_type == "mc_answer"
            if np.mean(size) > 25:
                letter_database = self.jp_letter_data_mc_answer.items()
            else:
                letter_database = self.en_letter_data_mc_answer.items()
        
        for letter, letter_pixels in letter_database:
            resized_pixel_data = Image.fromarray(pixel_data).resize(letter_pixels.shape[::-1], Image.LANCZOS)
            resized_pixel_data = (np.array(resized_pixel_data) > 200).astype(int)*255
            #print(sum(sum(resized_pixel_data != letter_pixels))/resized_pixel_data.size)
            if sum(sum(resized_pixel_data != letter_pixels))/resized_pixel_data.size < 0.15:
                #print(letter," found")
                return letter               
        return "Error: Letter not found"
    
    
    
    
    
    
    
    
    
    