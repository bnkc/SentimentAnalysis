#programmer: Lev Ostatnigrosh 
#date started: 9/27/2021
#the point of this program is to find out how my friend sergey feels based on his texts over the course of the last year
#you should be able to do things such as filter what dates and times you are looking for to find out the polarity of Sergeys texts.
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer




sia = SentimentIntensityAnalyzer()
results_array = []


def executor(info):
    """
    Users input takes you to the appropriate function
    """

    response = input('Welcome to Sergeys Mood Calculator. Please Select From the Following List: \n{}'.format('How is sergey doing this month?[1]'))
    if response == '1':
        res = lastMonth(info)
        results_array.append(res)

    else:
        raise ValueError('mistakes were made')


def lastMonth(info):
    df = pd.DataFrame(info)
    new = df['Message_Date'].str.split(" ", n = 1, expand = True)
    df['date'] = new[0]
    df['time'] = new[1]
    df.drop(columns = ['Message_Date'], inplace = True)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    #Filter data between two dates
    df = df.query("date >= '2021-06-21' \
                       and date < '2021-09-30'")
    #filter out my messages and leave just sergeys messages
    df = df.loc[df['Type'] == 'Incoming']
    
    #filter out the null messages
    df = df[df['Text'].notnull()]

    #Data pre-processing for textual variables 
    #lowercasing
    df = df.apply(lambda x: x.astype(str).str.lower())

    #special characters
    df['Text'] = df['Text'].str.replace('[^\w\s]','', regex = True)

    #stemming
    st = PorterStemmer()
    words = df['Text'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))


    #loop through the column messages to rate each message with sentement
    #and then average the message sentament dependent on # of texts
    count_positive = 0
    count_negative = 0
    count_neutral = 0
    count = len(words)
    for word in words:
        val = sia.polarity_scores(word)
        for i in val:
            if i == 'neg':
                count_negative += val[i]
            elif i == 'neu':
                count_neutral += val[i]
            elif i == 'pos':
                count_positive += val[i]


    print('This is a breakdown of sergeys mood over the course of the last month: \
        \n {:.1%} of Sergeys texts have been negative from 9/1/2021 - 9/30/2021\
        \n {:.1%} of Sergeys texts have been neutral from 9/1/2021 - 9/30/2021\
        \n {:.1%} of Sergeys texts have been positive from 9/1/2021 - 9/30/2021'.format(count_negative / count, count_neutral / count, count_positive / count))
    

    









#here we read the csv file
debug = True 

if debug:
    information = pd.read_csv('Messages - Sergey Filimonov.csv', lineterminator='\n')

    results = executor(information)