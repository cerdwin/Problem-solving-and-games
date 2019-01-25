import os
import re
import sys
from utils import read_classification_from_file as read_from_file
from neutralwords import words as neutral_words
 
# -------------- SUBSEQUENT METHODS WERE REMOVED DUE TO RESTRICTIONS ON IMPORTED LIBRARIES ----------------------#
# import nltk
# nltk.download('all')
# from nltk.stem import PorterStemmer
# porter = PorterStemmer()
# from dojo import Evaluate as evaluate -- parsing and finding optimal encoding currently not in use
# ---------------------------------------------------------------------------------------------------------------#
 
class MyFilter:
    """
    Naive Bayes filtering, (originally with Laplace normalisation, stemming) and tokenisation
    """
 
    def __init__(self):
        self.spam_count = 0 # I take a record of the number of spam emails
        self.spam_word_count = 0    # I record number of spam words
        self.ham_count = 0  # I record count of non-spam emails
        self.ham_word_count = 0     # I calculate all words which are non-spam
        self.total_emails = 0   # total emails, hopefully self-explanatory :)
        self.spam_probability = 0   # probablility of an email being a spam
        self.spam_words = {}    # dictionary of spam words
        self.ham_words = {}  # dictionary of ham words
        self.spamliness = 1.00  # initialising the likelihood of an email being spam and ham to 1.00
        self.hamliness = 1.00
        self.predictions = {}   # dictionary of emails tested and my predictions- only for my testing purposes
        self.numfiles = 0   # I record how many files I am being tested on
        self.my_dictionary = {}     # dictionary derived from !truth file, training set
        self.spam = 0       # I calculate how many emails I deem to be spam/non-spam
        self.ham = 0
        self.spam_limit = 0     # an arbitraty value which is low enough to capture words which are not significant
        self.ham_limit = 0
         
    # ------------------------------------------ TRAINING -------------------------------------#
    def train(self, directory):
        """
        Training method, recording and learning from test data
        :param directory: Absolute path to the !truth file
        :return: alters instances, records data
        """
        # 1. First I open the !truth file and read files classifications between Spam or Ham and place in a dictionary
        dictionary = read_from_file(os.path.join(directory, "!truth.txt"))
        self.my_dictionary = dictionary
        # 2. Second, I compute basic statistics - ratio of hams to spams and total counts
        self.statistics(dictionary)
        # 3. Third, I cast preprocessed spam and ham words into their respective dictionaries
        self.word_casting(dictionary, directory)
 
    @staticmethod
    def remove_html_tags(string):
        """
        A static method removing html tags from strings
        :param string: string is usually a single line in an email
        :return: function returns the line without html tags
        """
        remover = re.compile(r'<.*?>')   # First we compile the expression for html tags
        text_without_html = re.sub(remover, '', string)    # in the line we substitute the tags for an empty string
        return text_without_html    # we subsequently return the designated altered string
 
    @staticmethod
    def normalisation(line):
        """
        Instead of removing web addresses, phone numbers, money symbols or emails,
        this method replaces their occurrence with special words and accounts for stopwords
        :param line: Usually a line of an email
        :return: the same line, with words deemed irrelevant to classify removed and words specified above substituted
        """
 
        remover = re.compile(r'\b[\w\-.]+?@\w+?\.\w{2,4}\b')    # First compiles the expression for an email address
        line = re.sub(remover, 'xemailaddr', line) # Substitutes instances of email addresses for 'xemailaddr'
 
        remover = re.compile(r'(http[s]?\S+)|(\w+\.[A-Za-z]{2,4}\S*)')  # Second, compiles expression for website
        line = re.sub(remover, 'xwebaddr', line)   # Substitutes instances of web addresses for 'xwebaddr'
 
        remover = re.compile(r'ÂŁ|\$')   # Third, compiles expressions for money signs
        line = re.sub(remover, 'xmoney', line)  # substitutes instances of money signs for 'xmoney'
 
        # Fourth, compiles expressions for phone numbers
        remover = re.compile(r'\b(\+\d{1,2}\s)?\d?[\-(.]?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b')
        line = re.sub(remover, 'xphonenum', line)  # substitutes instances of phone numbers for 'xphonenum'
        return line     # returns the preprocessed line of email
 
    @staticmethod
    def tokenisation(string):
        """
        method removing regex characters from line (tokens)
        :param string:  Usually a line of an email
        :return:    the same line, without regular expression characters
        """
        remover = re.compile(r'[^\w\s]')    # First, compiles expressions for regular expressions
        text_without_tokens = re.sub(remover, '', string)  # removes instances of regular expressions
        return text_without_tokens  # returns the same line only without regular expressions
 
    @staticmethod
    def stemming(string):
        """
        - Not in use due to forbidden libraries -
        A simple NLP method unifying different tenses of one word - instead of seeing for example similar words like:
        we capture their meaning under an unifying umbrella term represented by their shared syntactical stem
        :param string: Usually a line of an email
        :return: the same line, with respective words reduced to their stems
        source: https://pythonprogramming.net/stemming-nltk-tutorial/
        """
        module_name = 'nltk'
        if module_name not in sys.modules:
            pass    # If download of nltk library was unsuccessful, we skip stemming
        else:
            return ' '.join(
                porter.stem(term)
                for term in string.split()
                if term not in set(neutral_words)      # We search neutral words as items in a set to improve speed
            )
 
    def word_casting(self, dictionary, path):
        """
        method preprocessing spam and ham words and casting them into respective dictionaries
        :param dictionary: a dictionary with file names as keys and "SPAM" or "OK" as respective values
        :return:
        """
 
        for document in dictionary.keys():      # Following steps are repeated for each file contained in dictionary
            with open(os.path.join(path, document), 'r', encoding='utf-8') as f:
                for line in f:  # For every line in respective email
                    # Preprocessing ------------------------------------------
                    if line is None:    # Avoiding processing blank lines
                        continue
                    line = line.rstrip()    # First, we remove redundant spaces and set the line to lower cases
                    line = line.lower()
                    line = self.remove_html_tags(line)  # Second, we remove html tags
                    line = self.normalisation(line) # Third, we join representation for money, web and email addresses
                    line = self.tokenisation(line)  # - Fourth, we remove tokens from strings
                    # line = self.stemming(line)   # Fifth, we reduce words to their common stems
                    if line is None:
                        continue
                    words = line.split()    # Sixth, we separate words
                    # ---------------------------------------------------
                    for word in words:  # For each word we find on a line of each file
                        # If the word is one we do not want to account for, as specified by neutral words, we skip it
                        if word in neutral_words:
                            continue
                        if (word.startswith("<" or ">")):   # checking remainds of regex parsing
                            continue
                        if (word.endswith(">" or "<")):
                            continue
                        if dictionary[document] == 'SPAM':  # if the email containing it is SPAM
                            self.spam_word_count += 1            # we increment the count of total spam words
                            if word in self.spam_words:     # if the word is already in dictionary of spam words
                                self.spam_words[word] += 1  # we merely increment its value - occurrence
                            else:
                                self.spam_words[word] = 1   # if the word is not in dictionary of spam words, we add it
                        else:                               # We repeat the process analogously with non-spam emails
                            self.ham_word_count += 1
                            if word in self.ham_words:
                                self.ham_words[word] += 1
                            else:
                                self.ham_words[word] = 1
            # document.close()
 
    def statistics(self, dictionary):
        """
        method receives a dictionary derived from !truth file and calculates
        ratio of SPAMs to HAMs
 
        :param dictionary: dictionary with file names as keys and "SPAM" and "OK" as values depending on the file type
        :return: works out the total count of emails and its share of spams
 
        """
        for i in dictionary.keys():  # repeating following steps for every dictionary entry
            if dictionary[i] == 'SPAM':     # if a certain file is classified as spam
                self.spam_count += 1        # the method increments the total value of spams
            else:                           # it proceeds analogously with non-spam emails
                self.ham_count += 1
        self.total_emails = self.ham_count + self.spam_count        # method takes the sum of spams and hams
        self.spam_probability = self.spam_count/(float)(self.total_emails)   # the probability of a spam is calculated
 
    # ----------------------------------TESTING------------------------------------------------------------ #
    def laplace(self, word, spamham):
        """
        method originally Laplace normalising values for Naive Bayes classification, now merely calculating
        mid-values for the Naive Bayes method.
        :param word: a single word found in body of an email
        :param spamham: either spam or ham category
        :return: a component of the Bayes (laplace normalisation) formula
        """
        if spamham == 'spam':
            x = self.spam_words[word]/(self.spam_count)
            if x > 0.000091:    # we try to eliminate very small numbers, the constant was chosen arbitrarily
                return (self.spam_words[word]/(self.spam_count))    # we return the share of the word in terms of spams
            else: return 1  # in case of an insignificant word, we do not account for it
 
        else:   # analogously
            if self.ham_words[word]/(self.ham_count) > 0.001:
                return (self.ham_words[word]/(self.ham_count))
            else:
                return 1
 
    def classify(self, path, prediction_dict):
        """
        Method writing into the !predictions file names of files and their status: SPAM or OK- currently not in use
        """
        with open(os.path.join(path, '!prediction.txt'), 'w', encoding='utf-8') as f:
            for key in prediction_dict:
                f.write(key + ' ' + prediction_dict[key])
                f.write('\n')
 
    def testing(self):
        """
        A method used merely for personal testing purposes.
        :return: A classification of a filters accuracy
        """
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        counter = 0
        for file in self.predictions.keys(): # for every file we added into training dictionary
            counter = counter + 1
            if file in self.my_dictionary.keys():   # method gathers true/false positives/negatives
                if self.predictions[file] == 'SPAM' and self.my_dictionary[file] == 'SPAM':
                    tp = tp + 1
                elif self.predictions[file] == 'SPAM' and self.my_dictionary[file] == 'OK':
                    fp = fp + 1
 
                elif self.predictions[file] == 'OK' and self.my_dictionary[file] == 'OK':
                    tn = tn + 1
                elif self.predictions[file] == 'OK' and self.my_dictionary[file] == 'SPAM':
                    fn = fn + 1
                else:
                    print("Something went wrong, are you sure you are using correct dictionaries?")
 
                # print("tp, fp, tn, fn") - method prints statistics
                # print(tp, fp, tn, fn)
                # print(counter)
 
    def test(self, directory):
        """
        Method assigning each email in directory into SPAM or OK category, writing it into !prediction file
        :param directory: directory of all documents employed
        :return: a file !prediction.txt with email names and "SPAM" or "OK" next to them
        """
        prediction_path = directory + '/!prediction.txt'    # I create an absolute path to !prediction file I made
        with open(prediction_path, 'w', encoding='utf-8') as f: # I open the file I am going to write into
            for filename in os.listdir(directory):  # for every single email in our directory
                if filename[0] == '!':  # if the email name starts with !, I skip it
                    continue
                else:
                    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as onefile:  # I open each email
                        self.numfiles += 1
                        for line in onefile:    # For each line in the email I preprocess its text
                            # Preprocessing ------------------------------------------
                            if line is None:
                                continue
                            line = line.rstrip() # preprocessing steps analogous to those used previously
                            line = line.lower()
                            line = self.remove_html_tags(line)
                            line = self.normalisation(line)
                            line = self.tokenisation(line)
                            # line = self.stemming(line)
                            if line is None:
                                continue
 
                            words = line.split()
                            # ---------------------------------------------------
                            for word in words:  # I subsequently calculate spamliness and hamliness of each word
                                if word in neutral_words :
                                    # print("skipping")
                                    continue
                                if (word.startswith("<" or ">")):
                                    continue
                                if (word.endswith(">" or "<")):
                                    continue
                                if word not in self.ham_words.keys():
                                    continue
                                if word not in self.spam_words.keys():
                                    continue
                                # Calculations ------------------------------------------
                                # method checking if the word is not representative enough
                                self.spam_limit = (self.spam_count / self.total_emails) * 100
                                self.ham_limit = (self.ham_count / self.total_emails) * 33
                                if self.spam_words[word] == self.spam_limit and self.ham_words[word] == self.ham_limit:
                                    continue
                                if self.spam_words[word] == 0:
                                    continue
                                self.spamliness = self.spamliness * self.laplace(word, 'spam') # Naive Bayesian calcs.
                                self.hamliness = self.hamliness * self.laplace(word, 'ham')
                                # --------------------------------------------------------
                                 
                        # Recording decision ----------------------------------------------
                        # if the file is more spam than ham, we record this into the !predictions file
                        if (self.spam_probability * self.spamliness) > ((1 - self.spam_probability) * self.hamliness):
                            self.predictions[filename] = 'SPAM' # If the email is more spamly, I decide it is a spam
                            f.write(filename + ' ' + 'SPAM' + '\n')
                            self.spam = self.spam + 1
                        # Otherwise, we record it being more likely a non-spam email
                        else:
                            self.predictions[filename] = 'OK'   # otherwise, I decide it is not a spam email
                            f.write(filename + ' ' + 'OK' + '\n')
                            self.ham = self.ham + 1
                        # ----------------------------------------------------------------
                    self.spamliness = 1.00     # I subsequently reset spamliness and hamliness coefficients used
                    self.hamliness = 1.00
        # f.close
 
if __name__ == '__main__':
    print("processing...")
    filter = MyFilter()
    train_path = r"C:\Users\notebook\Downloads\spamming.zip\1"
    test_path = r"C:\Users\notebook\Downloads\spamming.zip\1"
    filter.train("C:/Users/notebook/PycharmProjects/1")
    filter.test("C:/Users/notebook/PycharmProjects/2")
    filter.testing()
    print("spamy:", len(filter.spam_words.items()))
    print("hamy:", len(filter.ham_words.items()))
    print(filter.spam)
    print(filter.ham)
