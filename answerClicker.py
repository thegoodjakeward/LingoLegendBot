import pyautogui
import time

class AnswerClicker:
    
    @staticmethod
    def answerTrueFalse(itIsTrue):
        """
        Clicks the appropriate part of the screen to answer True or False
        
        Args:
            itIsTrue (bool): Lets this function know if it should answer True of False
        Returns:
            None
        """
        if itIsTrue:
            pyautogui.click(980,925)
            return
        else:
            pyautogui.click(940,925)
            time.sleep(0.5) # Half second delay to wait for the continue prompt to be clickable
            pyautogui.click(940,920)
            return
        
    @staticmethod
    def answerMultipleChoice(answer_number):
        """
        Clicks the appropriate part of the screen to answer a multiple choice question
        
        Args:
            answer_number (int): Lets this function know which multilpe choice answer it should select
        Returns:
            None
        """
        match answer_number:
            case 0: # Top left answer
                pyautogui.click(860,812)
            case 1: # Top right answer
                pyautogui.click(1060,812)
            case 2: # Bottom left answer
                pyautogui.click(860,870)
            case 3: # Bottom right answer
                pyautogui.click(1060,870)
            case _:
                print("Error: Multiple Choice Answer Not Found")
        return