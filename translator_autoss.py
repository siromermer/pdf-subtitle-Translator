import pyautogui
import keyboard
from PIL import Image
import pytesseract
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound
import time
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np 
import pandas as pd 

# datasets for antonyms and synonyms 
syn_df=pd.read_csv("synonyms_clear.csv")
ant_df=pd.read_csv("antonyms_clear.csv")

# important line for pytesseract , it must be your tesseract.exe file path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

"""
    WordNetLemmatizer for getting the root of the words , it is needed when user wants to see synonyms or antonyms 
    in csv files there are only root of functions therefore it is needed but in translate part there is no need to use that 
"""
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


"""
    in take_screenshot function program takes screenshot with respect mouse starting function and finishing function
"""

m = 0 # images path is increasing in every ss  , therefore you can see all the images after program finished
def take_screenshot(assignment):
    global m

    # mouse position
    x, y = pyautogui.position()
    
    # screen size 
    width, height = pyautogui.size()
    
    """ 
        !!!!!! SS COORDİNATES , USER NEEDS TO ADJUST THEM (for example i like reading pdf's with whole page , but user may want to see only paragraph or sentence )
        in this case user has to increase or decrease constants max(0, x - 120) 120 in this case    
        in my opinion best way to do it by trial and error , after 3 or 4 shot  you are gonna get results
    """

    # in programming coordinates work differently if you go downside y values are incerasing but x axis is same as classic math
    left = max(0, x - 120)  
    top = max(0, y - 23)    
    right = min(width, x + 120)    
    bottom = min(height, y + 23) 

    # take screenshot
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # increase size of image for better results
    new_width = screenshot.width * 2
    new_height = screenshot.height * 2
    resized_screenshot = screenshot.resize((new_width, new_height))

    # save screenshot with folder that you want 
    resized_screenshot.save(f"ssdemos31{m}.png")

    """
        Very İmportant : i tried all the Tesseract Page Segmentation Modes for extracting text from image and i decide to use 
                        psm 7 , for this project it worked best for me but you can try other modes
    """
    custom_config = r'--oem 3 --psm 7'   

    # extract sentence/text from image
    demo_string = pytesseract.image_to_string(Image.open(f'ssdemos31{m}.png'), config=custom_config)
    
    # increase m , because i want to see all the screenshots after program finished , otherwise images will override each other
    m+=1

    """
        find_word function takes two argument , demo_string is string that i extract above , and assignment comes from take_screenshot(assignment)
        assignment will decide what user want  : translated word , pronunciation , antonymous or synonym
    """
    find_word(demo_string,assignment)


def find_word(demo_string,assignment):
    word_list = demo_string.split(" ")
    for word in word_list:

        # remove \n 's from words 
        if "\n" in word:
            word=word.replace("\n","")
        
        # remove letters and conjunctions
        if len(word) <= 3: 
            continue

        # from below one of the function is gonna activate with parameter 'word'
        if assignment=="translate":
            translate(word)
        if assignment=="pronunciation":
            get_pronunciation(word)
        if assignment=="synonym":
            get_synonym(word)
        if assignment=="antonymous":
            get_antonymous(word)
         
"""
    translate function gives translated word :  dest="tr"  decides which language
"""

def translate(word):
    translator = Translator(service_urls=['translate.googleapis.com'])
    translated_word = translator.translate(word, src="en", dest="tr").text

    # gTTS is for voice 
    speech = gTTS(text=translated_word, lang="tr", slow=False)
    os.remove('text.mp3') 
    speech.save("text.mp3")
    playsound('text.mp3')

# for pronunciation of desired word
def get_pronunciation(word):
    speech = gTTS(text=word, lang="en", slow=False)
    os.remove('text.mp3') 
    speech.save("text.mp3")
    playsound('text.mp3')


def get_synonym(word):
    
    #  pure_word is root of the word --> played  convert to the  play
    pure_word = lemmatizer.lemmatize(word, pos='v')
    
    try:
        
        # it gives index of word in csv file
        word_index=np.where(syn_df["word"] == pure_word.lower())[0][0]

        # find synonym of word in csv file
        synonym_word=syn_df.iloc[word_index]["synonyms"]

        # sound part
        speech = gTTS(text=synonym_word, lang="en", slow=False)
        os.remove('text.mp3') 
        speech.save("text.mp3")
        playsound('text.mp3')
    
    except:
        print(f"no synonyms for {pure_word}")



# get_antonymous works like same with get_synonym you can check above for explanations 
def get_antonymous(word):

    #  pure_word is root of the word --> played  convert to the  play
    pure_word = lemmatizer.lemmatize(word, pos='v')

    try:
        word_index=np.where(ant_df["word"] == pure_word.lower())[0][0]
        antonyms_word=ant_df.iloc[word_index]["antonyms"]

        speech = gTTS(text=antonyms_word, lang="en", slow=False)
        os.remove('text.mp3') 
        speech.save("text.mp3")
        playsound('text.mp3')
    except:
        print(f"no antonyms for {pure_word}")


"""
    from on_key_event function i activate new function that is name is take_screenshot with one parameter
"""
def on_key_event(event):
    if event.name =='g':
        take_screenshot("translate")
    if event.name=="h":
        take_screenshot("pronunciation")
    if event.name=="j":
        take_screenshot("synonym")
    if event.name=="k":
        take_screenshot("antonymous")

"""
    When user pressed a key on_key_event function starts to work ,   there is one parameter and it is letter
    you can reach that letter with event.name 
"""     
keyboard.on_press(on_key_event)
keyboard.wait('+')


















