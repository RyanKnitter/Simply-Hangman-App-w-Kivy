import kivy
kivy.require('1.11.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import (StringProperty, NumericProperty, ObjectProperty)
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.graphics import Rectangle
from kivy.clock import Clock
import pandas as pd
import numpy as np

Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '550')

class HangmanPic(Widget):
    
    def update_pic(self, wrongGuesses):
        self.canvas.clear() 
        self.pos_hint = {'x': .05, 'y': .45}
        self.size_hint = (.90, .55)               
        with self.canvas:
            Rectangle(source="HangmanPic{}.jpg".format(wrongGuesses),
                      pos=self.pos, 
                      size=self.size)

class HangmanWord(Label):
    
    def __init__(self, **kwargs):
        super(HangmanWord, self).__init__(**kwargs)
        self.new_word()        

    def new_word(self):
        hangmanWords = pd.read_csv("C:/Users/rknit/Hangman/hangmanWords.csv",
                                   header=None)
        randomInt = np.random.randint(0,hangmanWords.shape[0])
        self.selectWord = hangmanWords.loc[randomInt][0].lower()
        #self.selectWord = "testtest"
        self.currentWord = "_ " * len(self.selectWord)
        del hangmanWords
        
    def update_word(self, letter):        
        if self.selectWord.find(letter) >= 0:
            self.updateWord = ""
            for i, l in enumerate(self.selectWord):
                if l == letter:
                    self.updateWord += l + " "
                else:
                    self.updateWord += self.currentWord[i*2] + " "
            self.currentWord = self.updateWord
            return 0
        else:
            return 1
            
    def actual_word(self):
        self.updateWord = ""
        for l in self.selectWord:
            self.updateWord += l + " "
        self.currentWord = self.updateWord

class HangmanMessage(Label):
    
    def __init__(self, msg = "Let's play! Enter a letter to start.", **kwargs):
        super(HangmanMessage, self).__init__(**kwargs)
        self.msg = msg
    
    def correct_answer(self):
        correctResponse = pd.read_csv("C:/Users/rknit/Hangman/correctResponses.csv",
                                      header=None)
        randomInt = np.random.randint(0,correctResponse.shape[0])
        self.msg = correctResponse.loc[randomInt][0]
        
    def wrong_answer(self):
        wrongResponse = pd.read_csv("C:/Users/rknit/Hangman/wrongResponses.csv",
                                    header=None)
        randomInt = np.random.randint(0,wrongResponse.shape[0])
        self.msg = wrongResponse.loc[randomInt][0]
        
    def losser(self):
        self.msg = "Better luck next time."
        
    def winner(self):
        self.msg = "Nice job!"
        
class HangmanInput(TextInput):
    
    def __init__(self, maxCharacters = 0, wrongGuesses = 0, **kwargs):
        super(HangmanInput, self).__init__(**kwargs)
        self.maxCharacters = maxCharacters
        self.wrongGuesses = wrongGuesses

    
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.maxCharacters:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)
        
    def refocusOnCommandTextInput(self):
        Clock.schedule_once(self._refocusTextInput, 0.1)  
        
    def _refocusTextInput(self, *args):
        self.focus = True

    # When the user types enter, the input text is passed to the hWrd.update_Word() 
        # only if guesses are less than 6
    # self.wrongGuesses is compared to the hWrd.wrongGuesses
    # If equal hMsg.correct_answer()
    # Check if the word was solved and end the game if it was
    # Else self.wrongGuesses = hWrd.wrongGuesses; hPic.update_pic()
        # If self.wrongGuesses < 6 then hMsg.wrong_answer() 
        # else hMsg.game_over() hWrd.actual_Word

class HangmanGame(Widget):
    hPic = ObjectProperty(None)
    hMsg = ObjectProperty(None)
    hWrd = ObjectProperty(None)
    hInpt = ObjectProperty(None)
    
    def __init__(self, wrongGuesses=0, **kwargs):
        super(HangmanGame, self).__init__(**kwargs)
        self.wrongGuesses = wrongGuesses
    
    def check_letter(self):
        if self.hInpt.text != "":
            self.i = self.hWrd.update_word(letter=self.hInpt.text)
            self.hInpt.text = ''
            if self.i == 1:
                self.wrongGuesses += 1
                self.hPic.update_pic(wrongGuesses=self.wrongGuesses)
                if self.wrongGuesses == 6:
                    self.hMsg.losser()
                    self.hInpt.maxCharacters = -1
                    self.hWrd.actual_word()
                else:
                    self.hMsg.wrong_answer()
            else:
                if self.hWrd.currentWord.find("_") == -1:
                    self.hMsg.winner()
                    self.hInpt.maxCharacters = -1
                else:
                    self.hMsg.correct_answer()
            
            self.hMsg.text = self.hMsg.msg
            self.hWrd.text = self.hWrd.currentWord
        
        self.hInpt.refocusOnCommandTextInput()
    

class HangmanApp(App):

    def build(self):
        self.title = 'Hangman'
        game = HangmanGame()
        return game

if __name__ == '__main__':
    HangmanApp().run()