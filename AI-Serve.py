import os

#tkinter
import tkinter as tk
from PIL import ImageTk,Image
import threading

#emotion model
import pickle
import nltk
import re, string
with open(r'finalemotiondetector.pickle', 'rb') as f:
    classifier = pickle.load(f)

#chatbot
from transformers import pipeline, set_seed
generator = pipeline('text-generation', model='./chatbot-xl', device_map="auto")

def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []
    for token, tag in nltk.tag.pos_tag(tweet_tokens):
        token = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def lemmatize_sentence(tokens):
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in nltk.tag.pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

class App():
    def __init__(self, master):
        self.button3 = tk.Button(window,text='Enter', command=self.press_enter).grid(row=4,columnspan=2,sticky='NESW')
           
    def press_enter(self):
        text=entry.get()
        if (text == 'quit'):
            window.destroy()
            return
        else: restext = self.respond(str(text))

        print("You say: "+text)

        emotion = self.analyse(restext)
        print("Bot's emotion: "+emotion)
        img = ImageTk.PhotoImage(Image.open(prefix[0]+emotion+".png"))
        image.configure(image=img)
        image.image = img
        print('AI-Serve says: '+restext)
        response.configure(text=restext)

    def analyse(self, custom_tweet):  #emotion analyse
        custom_tokens = remove_noise(nltk.tokenize.word_tokenize(custom_tweet))
        return classifier.classify(dict([token, True] for token in custom_tokens))

    def respond(self, text):
        conv[0] += "\nFriend: "+text+"\n"+charac[0]+": "
        resp = generator(conv[0], max_new_tokens=30, num_return_sequences=1)[0]['generated_text'].split(conv[-1])[1].split('\nFriend:')[0]
        conv[0] += resp
        return resp

print("initialising...")

ix=None
while ix==None:
    emotion_path=["Kyoko Kirigiri","Chiaki Nanami","Junko Enoshima","Celestia Ludenberg"]
    print("Available characters: "+", ".join(emotion_path))
    try:
        ix = int(input("Input 0~3: "))
        if ix>3 or ix<0:
            print("please specify a valid integer within range!")
            ix=None
    except:print("please choose a valid integer!")

prefix = ["emotions/"+emotion_path[ix]+"/"]
charac = [emotion_path[ix].split()[0]]
#conv = ["System: Eve is a cute female minor bot named Eve, created by CyberCraze. Eve is now chatting with one of her creator's friend."]
setup = [["System: Kyoko is a stoic, mysterious and intelligent female bot, created by CyberCraze. Kyoko tends to hide her feelings, usually considered distant and cold. Kyoko is now chatting with one of her creator's friend."],
         ["System: Chiaki is a cute and lively female minor bot, created by CyberCraze. Chiaki loves to chat about games. Chiaki is now chatting with one of her creator's friend."],
         ["System: Junko is a antagonist female bot, created by CyberCraze. Junko's manner is extremely erratic and apathetic, easily bored to an unhealthy and abnormal degree. Junko is now chatting with one of her creator's friend."],
         ["System: Celestia is a gothic, cold and cunning female bot, created by CyberCraze. Celestia is also prideful and ambitious, willing to selfish the lives of others to achieve victory. Celestia is now chatting with one of her creator's friend."]]
conv = setup[ix]
#start tkinter window
window=tk.Tk()
window.title("AI_Serve the Companion Bot")

img = ImageTk.PhotoImage(Image.open(prefix[0]+"normal.png"))
image = tk.Label(window, image=img)
image.grid(row=1,columnspan=2,sticky='NESW')

response = tk.Label(window, text="Type Something to Chat")
response.grid(row=2,columnspan=2,sticky='NESW')

entry = tk.Entry(window)
entry.grid(row=3,columnspan=2,sticky='NESW')

App(window)
window.mainloop()
