import pandas as pd
import re
class Clean:
    def __init__(self, filename):
        self.filename = filename
    #for column in list(data.columns):
    def clean_text(self, text):
        text = str(text)
        text = text.lower()
        text = re.sub(r"i'm", "i am", text)
        text = re.sub(r"he's", "he is", text)
        text = re.sub(r"she's", "she is", text)
        text = re.sub(r"that's", "that is", text)
        text = re.sub(r"there's", "there is", text)
        text = re.sub(r"what's", "what is", text)
        text = re.sub(r"\'ll", " will", text)
        text = re.sub(r"\'ve", " have", text)
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"won't'", "will not", text)
        text = re.sub(r"can't", "cannot", text)
        text = re.sub(r"we'd", "we would", text)
        text = re.sub(r"'d", " would", text)
        text = re.sub(r"didn't", "did not", text)
        text = re.sub(r"let's", "let us", text)
        text = re.sub(r"dont't", "do not", text)
        text = re.sub(r"it's", "it is", text)
        text = re.sub(' +',' ',text)
        #text = re.sub(r"[-()\"!@#$%^&*()*-+~?,|.]", "", text)
        text = re.sub(r"\r", " ", text)
        text = re.sub(r"\n", " ", text)
        text = re.sub(r"                 ", " ", text)
        text = re.sub(r"\s+"," ",text)
        #text = re.sub(r")"," ",text)
        text = re.sub(r"[()]"," ",text)
        text = re.sub(r"-"," ",text)
        text = re.sub(r"=="," ",text)
        #text = re.sub(r".."," ",text)
        text = re.sub(r":",",",text)
        return text
    def cleaning(self,filename):
        data = pd.read_csv(filename, encoding='utf-8', index_col='Unnamed: 0')
        lists_symptopms = []
        lists_subject = []
        data['subject'] = data['subject'].apply(lambda x:self.clean_text(x))
        data['Symptoms'] = data['Symptoms'].apply(lambda x:self.clean_text(x))
        #data['Solutions'] = data['Solutions'].apply(lambda x:x.lower())
        data = data[['subject','Symptoms', 'Solutions']]
        data.rename(columns= {"subject": "Subject"}, inplace = True)

        for i in data['Symptoms']:
            lists_symptopms.append(i)
        for i in data['Subject']:
            lists_subject.append(i)
        return lists_subject

    def dataframe(self,filename):
        data = pd.read_csv(filename, encoding='utf-8', index_col='Unnamed: 0')
        lists_symptopms = []
        lists_subject = []

        data['subject'] = data['subject'].apply(lambda x:self.clean_text(x))
        data['Symptoms'] = data['Symptoms'].apply(lambda x:self.clean_text(x))
        #data['Solutions'] = data['Solutions'].apply(lambda x:self.clean_text.lower())
        data = data[['subject','Symptoms', 'Solutions']]
        data.rename(columns= {"subject": "Subject"}, inplace = True)

        for i in data['Symptoms']:
            lists_symptopms.append(i)
        for i in data['Subject']:
            lists_subject.append(i)
        return data