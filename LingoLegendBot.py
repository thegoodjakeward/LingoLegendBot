"""
-------------------------------------------------------------------------------
                              FILE INFORMATION
-------------------------------------------------------------------------------
FILE:         LingoLegendBot.py
AUTHOR:       Jacob Ward (thegoodjakeward)
DATE:         5/1/2025
DESCRIPTION:  Automatically answers questions in Lingo Legend's training mode.
VERSION:      1.0
INSTRUCTIONS: First change the start and stop star count and the region of
              interest (ROI) variables in the USER INPUTS section. The ROI
              values are currently set to the correct values for a OnePlus 7T 
              being displayed on a 1920x1080 monitor, however your device and 
              monitor will likely require different coordinates. Next, mirror 
              your phone to your computer using Vysor or similar software. 
              Open the mobile app Lingo Legend and from the home screen enter 
              "Training Mode". Then run this script to begin answering 
              questions. The script will stop upon reaching the desired star 
              count or when the user holds down the ESC key.
-------------------------------------------------------------------------------
                                USER INPUTS
-------------------------------------------------------------------------------
folder_path: Path to the numpy files that make up the letter database

startStar: Number of stars you currently have before running the program
stopStar:  Number of stars you want the program to end on after obtaining

questionROI:    Left, Top, Right, and Bottom values defining the box 
                surrounding the question letter (ROI = Region of Interest)
trueTestROI:    Region of interest values defining the box surrounding the word
                True to test if the question is a True/False question
trueTestPixels: This value is the sum of the pixel data inside the trueTestROI
                for a typical True/False question
tfROI:          Region of interest values defining the box surrounding the 
                True/False answer letter
mcEnglishROI:   Region of interest values defining the boxes surrounding the
                4 multiple choice answers when the answers are English
mcHiraganaROI:  Region of interest values defining the boxes surrounding the
                4 multiple choice answers when the answers are Hiragana
-------------------------------------------------------------------------------
"""

from PIL import ImageGrab
import pyautogui
import os
import keyboard
import QuestionAnswerer

# START OF USER INPUTS---------------------------------------------------------

folder_path = os.path.join(os.getcwd(), "Japanese Data")

startStar = 50
stopStar = 70

questionROI = (937,614,987,677)

trueTestROI = (1045,895,1100,915)
trueTestPixels = 192829
tfROI = (937,780,987,830)

mcEnglishROI = [
    (845,790,880,825),
    (1045,790,1080,825),
    (845,855,880,890),
    (1045,855,1080,890)
    ]
mcHiraganaROI = [
    (835,765,890,825),
    (1030,765,1090,825),
    (835,860,890,920),
    (1030,860,1090,920)
    ]

# END OF USER INPUTS-----------------------------------------------------------

questions = startStar*4

answerer = QuestionAnswerer.QuestionAnswerer(folder_path, questionROI, trueTestROI, trueTestPixels, tfROI, mcEnglishROI, mcHiraganaROI)

# The current qeuestion is compared to the previous question to prevent the
# program from answering a single question multiple times while waiting for the
# screen to transition to the next question. Unfortunately it is possible to
# get the same question twice in a row so the stuck_counter forces the program
# to continue if it has been waiting for a new question for too long.
previous_question = "" 
stuck_counter = 0

running = True
while running:
    # Holding the escape key will stop the program
    if keyboard.is_pressed('esc'): 
        running = False 
        print('Escape key pressed. Exiting loop.')
        
    # Take screenshot of screen and convert to grayscale
    image = ImageGrab.grab()
    image = image.convert('L')
    
    # Gets the question text and if it is True/False or Multiple Choice
    question_text, question_type = answerer.getQuestion(image)
    
    # If question text is error, do nothing as next question hasn't loaded yet
    if question_text != "Error: Letter not found":
        if question_text != previous_question:
            stuck_counter = 0
            if question_type == "tf": # True/False Question
                answer = answerer.answerTF(question_text, image)
            else: # Multiple Choice Question
                answer = answerer.answerMC(question_text, image)
                
            if answer == "Success: Answer Found":
                questions += 1
                previous_question = question_text
                print("Questions:",questions,"    Stars:",questions/4)
        else:
            stuck_counter += 1
            if stuck_counter > 10: 
                # It is a new question so set previous_question to empty so the
                # program continues
                previous_question = ""
            
    else: # Round of questions is over so click to start next round
        pyautogui.click(972,681)
        
    if questions/4 >= stopStar: # Stop when desired star count is reached
        running = False
        
    
    