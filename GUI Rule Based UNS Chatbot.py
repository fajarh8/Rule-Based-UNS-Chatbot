import tkinter as tk
from tkinter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet
import bs4 as bs
import warnings
import urllib.request
import nltk
import random
import string
import re
from nltk.corpus import stopwords
# nltk.download('stopwords')

# Uncomment these below if being run for the first time
# nltk.download('wordnet')
# nltk.download('punkt')

# to filter warnings
warnings.filterwarnings('ignore')

# getting the synonyms for the word 'hello'
synonyms = []
for syn in wordnet.synsets('hello'):
    for lem in syn.lemmas():
        lem_name = re.sub(r'\[[0-9]*\]', ' ', lem.name())
        lem_name = re.sub(r'\s+', ' ', lem.name())
        synonyms.append(lem_name)

# inputs for greeting
greeting_inputs = ['hey', 'whats up', 'good morning',
                   'good evening', 'morning', 'evening', 'hello there', 'hey there']
# concatenating the synonyms and the inputs for greeting
greeting_inputs = greeting_inputs + synonyms
# inputs for a normal conversation
covo_inputs = ['how are you', 'how are you doing', 'you good']
# greeting responses by the bot
greeting_responses = ['Hello! How can I help you?',
                      'Hey there! So what do you want to know?',
                      'Hi, you can ask me anything regarding Brac.',
                      'Hey! wanna know about Brac? Just ask away!']
# conversation responses by the bot
convo_responses = ['Great! what about you?',
                   'Getting bored at home :( wbu??', 'Not too shabby']
# conversation replies by the user
convo_replies = ['great', 'i am fine', 'fine',
                 'good', 'super', 'superb', 'super great', 'nice']
# few limited questions and answers given as dictionary
question_answers = {'what are you': 'I am bot, ro-bot :3',
                    'who are you': 'I am bot, ro-bot :3',
                    'what can you do': 'Answer questions About UNS!',
                    'what do you do': 'Answer questions About UNS!'}

# fetching raw html data about brac from wiki
raw_data = urllib.request.urlopen(
    #comment satu per satu
    #'https://uns.ac.id/id/tentang-uns/sejarah-uns'
    #'https://id.wikipedia.org/wiki/Universitas_Sebelas_Maret'
    'https://www.gramedia.com/pendidikan/universitas/universitas-sebelas-maret-uns')

raw_data = raw_data.read()
article = bs.BeautifulSoup(raw_data, 'lxml')
paragraphs = article.find_all('p')
article_text = ''
for p in paragraphs:
    article_text += p.text

article_text = article_text.lower()

def save_to_txt(data, filename):
    with open(filename, 'a', encoding="utf-8") as file:
        for item in data:
            file.write(item)

def read_from_txt(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        content = file.read()
    return content

article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)
save_to_txt(article_text, 'chatbot.txt')
article_text = read_from_txt('chatbot.txt')
sentences = nltk.sent_tokenize(article_text)

words = nltk.word_tokenize(article_text)

# lemmatizing words as a part of pre-processing
def perform_lemmatization(tokens):
    lemma = nltk.stem.WordNetLemmatizer()
    return [lemma.lemmatize(token) for token in tokens]

# removing punctuation
remove_punctuation = dict((ord(punc), None) for punc in string.punctuation)

# method to pre-process all the tokens utilizing the above functions
def processed_data(document):
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(remove_punctuation)))

# function for punctuation removal
def punc_remove(str):
    punctuations = r'''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ''

    for char in str:
        if char not in punctuations:
            no_punct = no_punct + char

    return no_punct


# method to generate a response to greetings
def generate_greeting_response(hello):
    if punc_remove(hello.lower()) in greeting_inputs:
        return random.choice(greeting_responses)


# method to generate a response to conversations
def generate_convo_response(str):
    if punc_remove(str.lower()) in covo_inputs:
        return random.choice(convo_responses)


# method to generate a answers to questions
def generate_answers(str):
    if punc_remove(str.lower()) in question_answers:
        return question_answers[punc_remove(str.lower())]


stop_words = nltk.corpus.stopwords.words('indonesian')
# method to generate response to queries regarding brac


def generate_response(user):
    bracrobo_response = ''
    sentences.append(user)

    word_vectorizer = TfidfVectorizer(tokenizer=processed_data, stop_words=stop_words)

    all_word_vectors = word_vectorizer.fit_transform(sentences)
    similar_vector_values = cosine_similarity(
        all_word_vectors[-1], all_word_vectors)
    similar_sentence_number = similar_vector_values.argsort()[0][-2]

    matched_vector = similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]

    if vector_matched == 0:
        bracrobo_response = bracrobo_response + 'Sorry, my database doesn\'t have the response for that. Try something different and related. '
        return bracrobo_response
    else:
        bracrobo_response = bracrobo_response + \
            sentences[similar_sentence_number]
        return bracrobo_response


root = tk.Tk()
root.config(background="light blue")
root.title("UNS BOT")
# specify size of window.
root.geometry("500x800")


# Create text widget and specify size.
T = Text(root, height=5, width=20)

# Create label
l = Label(root, text="WELCOME ON CHATBOT UNS", background="light blue")
l.config(font=("Courier", 14))

# Create an Exit button.
b2 = Button(root, text="Exit",
            command=root.destroy, background="red", activebackground="yellow", font="Normal 10")

label4 = Label(
    root, text="Input your question here", font="Normal 10", background="light blue")
# label4.grid(row=1, column=0, columnspan=1)
entry1 = Text(root, bd=1, height=2,
              width=35,
              font="Normal 10",)
# entry1.grid(row=2, column=0, columnspan=1)
b11 = Button(root, text="Input", font="Normal 10",
             activebackground="blue", command=lambda: Take_input())
# b11.grid(row=2, column=1, columnspan=1)
label5 = Label(root, text="The answer are : ",
               font="Normal 10", background="light blue")
# label5.grid(row=2, column=2, columnspan=1)


def Take_input():
    user_input = entry1.get("1.0", "end-1c").lower()
    print(user_input)
    user_input = punc_remove(user_input)

    if user_input != 'bye':
        if user_input == 'thanks' or user_input == 'thank you very much' or user_input == 'thank you':
            print('Uns_Bot: Not a problem! (And WELCOME! :D)')
            Output.insert(
                END, '\n--------------------------------------------\nUns_Bot: Not a problem! (And WELCOME! :D)')
        elif user_input in convo_replies:
            print(
                '\n--------------------------------------------\nUns_Bot: That\'s nice! How may I be of assistance?')
            Output.insert(
                END, '\n--------------------------------------------\nUns_Bot: That\'s nice! How may I be of assistance?')
        else:
            if generate_greeting_response(user_input) is not None:

                print('Uns_Bot: ' + generate_greeting_response(user_input))
                Output.insert(END, '\n--------------------------------------------\nUns_Bot: ' +
                              generate_greeting_response(user_input))
            elif generate_convo_response(user_input) is not None:
                Output.insert(END, '\n--------------------------------------------\nUns_Bot: ' +
                              generate_convo_response(user_input))
                print('Uns_Bot: ' + generate_convo_response(user_input))
            elif generate_answers(user_input) is not None:
                print('Uns_Bot: ' + generate_answers(user_input))
                Output.insert(END, '\n--------------------------------------------\nUns_Bot: ' +
                              generate_answers(user_input))
            else:
                print('Uns_Bot: ', end='')
                # print(generate_response(user_input))
                Output.insert(END, '\n--------------------------------------------\nUns_Bot: ' +
                              generate_response(user_input))
                sentences.remove(user_input)
    else:
        print('\n--------------------------------------------\nUns_Bot: Bye, take care, stay home and stay safe!')
        Output.insert(
            END, '\n--------------------------------------------\nUns_Bot: Bye, take care, stay home and stay safe! ')


Output = Text(root, height=30,
              width=55,
              bg="light cyan")

l.pack()


label4.pack()
entry1.pack()
b11.pack()
label5.pack()
Output.pack()

b2.pack()
Output.insert(
    END, '\nHi! I am UNS BOT. You can ask me about UNS and I shall try my best to answer them: ')
tk.mainloop()
