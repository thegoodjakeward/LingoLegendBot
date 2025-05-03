# LingoLegendBot
## Overview
This project was for a YouTube video I did on creating a bot to get to the top of the monthly leaderboard in a language learning app called Lingo Legend. Check out the video here for more context: INSERT LINK HERE

## How It Works
The mobile app Lingo Legend has a "Training Mode" where you answer True/False and Multiple Choice language questions one after the other. This program looks at the app screen, matches the questions and answers to a database of letters, and then clicks on the correct answers, allowing speeds of almost 30 questions answered correctly per minute.

## How To Use
First, you will need to download Vysor or a similar software that allows you to mirror your phone screen to your computer and emulate taps from mouse clicks. From there, you will need to edit the region of interest (or ROI) variables in LingoLegendBot.py. These ROI variables define where the program will look when looking for the question and answers. They are currently set up to look at the correct places for a OnePlus 7T phone mirrored to a 1920x1080 monitor, but you will likely need to adjust for your phone type and monitor setup. Once these variables are set, and you have also defined your current star count and desired star count to stop on, you are ready to run the program. Mirror your phone screen, open up the Lingo Legend app, navigate to "Training Mode", and run LingoLegendBot.py. Checkout the program in action below:

![LingoLegendBotExample](https://github.com/user-attachments/assets/82e8f0d6-86f7-46db-92c9-3cb9bc383f65)

## Limitations
My goal for this project was to maximize stars earned per minute, which meant I chose a very easy language unit that only had True/False and Multiple Choice questions. This unit was unit 1.1 in the Japanese curriculum, "Hiragana Vowels: a, i, e, o & u". To expand this program to do other units, you would need to add the questions and answers from those units to the letter (or word) database. You would also need to add functionality for handling the "word builder" question type as this program can only handle True/False and Multiple Choice questions.
