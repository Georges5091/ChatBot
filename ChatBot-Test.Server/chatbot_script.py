import sys
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
try:
  nltk.data.find('tokenizers/punkt')
  nltk.data.find('corpora/wordnet')
except LookupError:
  nltk.download('punkt')
  nltk.download('wordnet')

def tokenize():
  file = open('data.txt', 'r', errors='ignore')
  corpus = file.read()
  sentences_tokens = nltk.sent_tokenize(corpus)
  word_tokens = nltk.word_tokenize(corpus)
  return sentences_tokens, word_tokens

lemmatizer = WordNetLemmatizer()

def lemmatize_tokens(tokens):
  return [lemmatizer.lemmatize(token) for token in tokens]

def preprocess_text(text):
  punctuation_map = dict((ord(punct), None) for punct in string.punctuation)
  tokens = nltk.word_tokenize(text.lower().translate(punctuation_map))
  tokens = lemmatize_tokens(tokens)
  return tokens

greeting_inputs = ['hello', 'hi', 'hey', 'greetings']
greeting_responses = ['I am a chatbot', 'hello', 'hi', 'hi there']

def greeting(text):
  for token in text.split():
    if token.lower() in greeting_inputs:
      return random.choice(greeting_responses)

def respond(user_query):
  bot_response = ''

  #Tokenize
  sent_tokens, word_tokens = tokenize()
  sent_tokens.append(user_query)

  #Vectorizing
  tfidf_obj = TfidfVectorizer(tokenizer=preprocess_text, stop_words='english')
  tfidf = tfidf_obj.fit_transform(sent_tokens)

  #Cosine Similarity
  similarity = cosine_similarity(tfidf[-1], tfidf)

  #selecting the response or token with max similarity
  index = similarity.argsort()[0][-2]

  flattened_sim = similarity.flatten()
  flattened_sim.sort()

  required_tfidf = flattened_sim[-2]

  if required_tfidf == 0:
    bot_response = bot_response + 'I am sorry, I do not understand'
    return bot_response
  else:
    bot_response = bot_response + sent_tokens[index]
    return bot_response

def split_input(user_query):
  delimiters = ['?', '.']
  questions = []
  temp = ""
  for char in user_query:
    if char in delimiters:
      if temp.strip():
        questions.append(temp.strip())
      temp = ""
    else:
      temp += char
  if temp.strip():
    questions.append(temp.strip())

  return questions

def chatbot(user_query):
  if user_query == 'exit':
    return "Bye, see you!"
  
  if greeting(user_query):
    return greeting(user_query)
  
  questions = split_input(user_query)
  responses = [respond(question) for question in questions]
  combined_response = " ".join(responses)
  return combined_response

if __name__ == '__main__':
  user_query = sys.argv[1]
  print(chatbot(user_query))