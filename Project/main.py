#programmer: Lev Ostatnigrosh 
#date started: 9/27/2021

#the point of this program is to run a sentiment analysis on your friends texts,
#and create a highlight reel of the best and worst texts that have been sent to you
#as well as graph the average on any given time table 

import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer
import datetime
import matplotlib.pyplot as plt


class SentimentAnalysis:

    def __init__(self, sia): 
        self.sia =  SentimentIntensityAnalyzer()
        self.df = pd.DataFrame(information)
        self.st = PorterStemmer()


    def process(self):
        """
        This Function runs a sentiment analysis on any given persons texts for any timeframe
        """

        new = self.df['Message Date'].str.split(" ", n = 1, expand = True)
        self.df['date'], self.df['time'] = new[0], new[1]
        self.df.drop(columns = ['Message Date'], inplace = True)
        self.df['date'] = pd.to_datetime(self.df['date'], format='%Y-%m-%d')

        df = self.df.query(f"date >= '{self.start}' \
                          and date < '{self.end}' \
                            and Type == 'Incoming'")


        #make a copy of the df into df1 that can then be used to pull the orginal wording
        self.fresh_words = df['Text'].to_list()

        #Data pre-processing for textual variables 
        df = df.apply(lambda x: x.astype(str).str.lower())
        df['Text'] = df['Text'].str.replace('[^\w\s]','', regex = True)
        df['Text'] = df['Text'].apply(lambda x: " ".join([self.st.stem(word) for word in x.split()]))
        self.words = df['Text'].to_list()
        sa.polarity_loop()

        
    def polarity_loop(self):
        """loop through the column messages to rate each message with sentiment
        and then average the message sentiment dependent on # of text"""
        self.compound_negative = 0
        self.compound_positive = 0
        self.compound_neutral = 0
        count_n = -0.1
        count_p = 0.1
        new_array = []
        for n in range(10):
            for word in self.words:
                val = self.sia.polarity_scores(word)
                if val['compound'] < count_n:
                    self.compound_negative += 1
                elif val['compound'] > count_p:
                    self.compound_positive += 1
                else: 
                    self.compound_neutral += 1
        count_n -= 0.1
        count_p += 0.1
        sa.options()


    def options(self):
        print(f'Here is the breakdown of {self.name}s texts: \
            \n {self.compound_negative / 10} of {self.name}s texts have been negative from {self.start} - {self.end}\
            \n {self.compound_neutral / 10} of {self.name}s texts have been neutral from {self.start} - {self.end}\
            \n {self.compound_positive / 10} of {self.name}s texts have been positive from {self.start} - {self.end}')

        re = input('Would you like a further breakdown? [Y/N] ')
        if re == 'Y' or 'y':
            print('Please Select from the following list: ')
            answer = input('Plot This Data [1]: \nView the best and worst texts sent to you [2]:')
            if answer == '1':
                sa.plot()
            elif answer == '2':
                sa.good_and_bad()
        else:
            exit()


    def plot(self):

        plt.plot(self.compound_positive, self.compound_negative)
        plt.xlabel('Time(Days/Months)')
        plt.ylabel('positive/negative average')
        plt.show()


    def good_and_bad(self):
        """
        Find the best and worst texts in the dataframe
        """
        good_array = []
        bad_array = []

        for item in self.words:
            v = self.sia.polarity_scores(item)
            if v['compound'] < -0.4:
                index1 = self.words.index(item)
                bad_array.append(self.fresh_words[index1])
            elif v['compound'] > 0.4:
                index2 = self.words.index(item)
                good_array.append(self.fresh_words[index2])

        print('Here are the top positive and negative texts sent to you... \n########################################################### \n\
               TOP POSITIVE TEXTS: \n{}\n\
               TOP NEGATIVE TEXTS: \n{} \n'.format(good_array[:5], bad_array[:5]))
        
        ans = input('Would You like to plot this data? [Y/N]')
        if ans == 'Y' or 'y':
            sa.plot()
        else:
            print('Exiting program...')
            exit()


    def executor(self):
        """
        Users input takes you to the appropriate function
        """
        split_date = self.df['Message Date'].str.split(" ", n = 1, expand = True)
        self.df['date'] = split_date[0]
        self.name = input('Welcome to the Mood Calculator. Please enter your friends name: ')
        self.response = input(f'Lets jump right in! \nAnalyze {self.name}. Select [1] ')
        if self.response == '1':
            print('Please enter a date range (YYYY-MM-DD) from the range available: {} - {}'.format(self.df['date'].iloc[0], self.df['date'].iloc[-1]))
            self.start= input('Start Date: ')
            self.end= input('End Date: ')
            try:
                datetime.datetime.strptime(self.start, '%Y-%m-%d')
                datetime.datetime.strptime(self.end, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            sa.process()

        else:
            raise ValueError('mistakes were made')


if __name__ == "__main__":
    information = pd.read_csv('XXXXXXXXXXXXX', lineterminator='\n')

    sa = SentimentAnalysis(information)
    sa.executor()
 
