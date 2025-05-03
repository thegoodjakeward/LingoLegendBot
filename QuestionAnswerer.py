import LetterRecognizer
import numpy as np
from answerClicker import AnswerClicker

class QuestionAnswerer:
    
    def __init__(self, folder_path, questionROI, trueTestROI, trueTestPixels, tfROI, mcEnglishROI, mcHiraganaROI):
        """
        Constructor to create the LetterRecognizer and all ROI variables to ansewr questions.
        
        Args:
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
        Returns:
            None
        """
        self.recognizer = LetterRecognizer.LetterRecognizer(folder_path)
        self.questionROI = questionROI
        self.trueTestROI = trueTestROI
        self.trueTestPixels = trueTestPixels
        self.tfROI = tfROI
        self.mcEnglishROI = mcEnglishROI
        self.mcHiraganaROI = mcHiraganaROI
        
    def getQuestion(self, image):
        """
        Analyzes image to get information on the question.
        
        Args: 
            image (Image): Grayscale image of the current app screen
        
        Returns:
            tuple:
                question_text: The letter that constitutes the question
                question_type: Either "tf" or "mc" to indicate True/False or Multilple Choice question type
        """
        question_image = self.recognizer.process_letter(image, self.questionROI)
        question_text = self.recognizer.find_letter(question_image,"question")
        if question_text == "Error: Letter not found":
            return ("Error: Letter not found", "Error: Letter not found")
        
        true_test_image = image.crop(self.trueTestROI)
        if abs(np.int64(np.array(true_test_image).sum()) - self.trueTestPixels)/self.trueTestPixels < 0.1:
            question_type = "tf"
        else:
            question_type = "mc"
            
        return (question_text, question_type)
    
    def answerTF(self, question, image):
        """
        Answers a True/False type question.
        
        Args: 
            question (string): The letter that constitutes the question
            image (Image):     Grayscale image of the current app screen
        
        Returns:
            string: "Success: Answer Found" if question is answered successfully or "Error: Letter not found" if not
        """
        answer_image = self.recognizer.process_letter(image, self.tfROI)
        answer = self.recognizer.find_letter(answer_image,"tf_answer")
        if answer == "Error: Letter not found":
            return "Error: Letter not found"
        else:
            if question.split("_")[0] == answer.split("_")[0]:
                AnswerClicker.answerTrueFalse(True)
            else:
                AnswerClicker.answerTrueFalse(False)
            return "Success: Answer Found"
        
    def answerMC(self, question, image):
        """
        Answers a Multiple Choice type question.
        
        Args: 
            question (string): The letter that constitutes the question
            image (Image):     Grayscale image of the current app screen
        
        Returns:
            string: "Success: Answer Found" if question is answered successfully or "Error: Letter not found" if not
        """
        if question.endswith("hira_question"):
            for n in range(4):
                answer_image = self.recognizer.process_letter(image,self.mcEnglishROI[n])
                answer = self.recognizer.find_letter(answer_image,"mc_answer")
                if answer != "Error: Letter not found":
                    if question.split("_")[0] == answer.split("_")[0]:
                        AnswerClicker.answerMultipleChoice(n)
                        return "Success: Answer Found"
        else:
            for n in range(4):
                answer_image = self.recognizer.process_letter(image,self.mcHiraganaROI[n])
                answer = self.recognizer.find_letter(answer_image,"mc_answer")
                if answer != "Error: Letter not found":
                    if question.split("_")[0] == answer.split("_")[0]:
                        AnswerClicker.answerMultipleChoice(n)
                        return "Success: Answer Found"
        return "Error: Letter not found"
                        
                        
                        
                        