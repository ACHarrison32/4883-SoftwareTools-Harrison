# :computer: A06 - Sphinx
## :name_badge: Andrew Harrison
## :school: 4883 Software Tools
## :date: 06/25/2023

### :memo: Description
#### [Sphinx](https://www.sphinx-doc.org/en/master/) is a widely used open-source documentation generation tool. It is commonly used to create documentation for software projects, libraries, and APIs. Sphinx supports various programming languages, but it is particularly popular in the Python community.


## :computer: How To Install Sphinx:
#### Video link on how to install [Sphinx](https://www.youtube.com/watch?v=WcUhGT4rs5o)
#### Directions for installing [Sphinx](https://www.sphinx-doc.org/en/master/usage/installation.html)
#### Start by making sure you have [Python](https://www.python.org/downloads/release/python-3114/) downloaded. You can check this in the Command Terminal using: python --version
#### Create a folder to keep all your sphinx stuff in
#### Install sphinx: pip install sphinx

## :desktop_computer: Starting Sphinx:
#### Quickstart sphinx in command terminal: sphinx-quickstart
#### Fill out the next few questions:
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_Quickstart.PNG" >

#### This creates you Sphinx project now you create your HTML documents and document you python code.

## :electric_plug: Adding Extensions and Python Module Search Path
#### First add your Python code documents in the folder that you quickstarted Sphinx in.
#### Open up your conf.py file: code conf.py
#### Add the following 3 lines to the file:
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_Python_Path.PNG">

#### Adding these 3 lines allows Sphinx to locate and import your project’s modules during the documentation generation process
#### Now we need to add the following Extensions:
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_Extensions.PNG" >

#### sphinx.ext.autodoc: This extension is used to automatically generate API documentation from your Python code.
#### sphinx.ext.viewcode: This extension adds links to the source code of documented Python objects, allowing users to easily view the source code.
#### sphinx.ext.napoleon: This extension allows you to use Google-style or NumPy-style docstrings, providing support for more expressive and readable docstrings.
#### Once you have added these extensions and the python path install the following command: pip install sphinx-autodoc-typehints
#### You have now installed everything you need to document your python code

## :file_folder: Creating Your rst Files and Including Modules
#### Now you want to make your rst files from your python code files.
#### To do this run the following command: sphinx-apidoc -o <output_directory> <source_directory>
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_apidoc.PNG" >

#### Once you have created the rst files, open your modules.rst file and make sure the follwing python file is called.
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_Modules.PNG" >

## :bookmark_tabs: Making Your index.rst and Toctree’s
#### Toctree’s are your Table of Contents Tree’s
#### This is where you will add your modules.rst file that calls your specified modules
#### You can add many toctree’s and have them link to different files
#### Create you index.rst using restructured text. This will be how your HTML cite looks.

## :clipboard: Sample Python Documents
### Addition 
``` py
def add(a, b):
    """
    This function returns the sum of two input numbers.

    :param a: First input number.
    :type a: float
    :param b: Second input number.
    :type b: float
    :return: The sum of two numbers.
    :rtype: float
    """
    s = a + b
    return s
```
### Subtraction
``` py
def sub(a1, b1):
    """
    This function returns the result of subtracting b1 from a1.

    :param a1: First input number.
    :type a1: int
    :param b1: Second input number.
    :type b1: int
    :return: The result of subtracting b1 from a1.
    :rtype: int
    """
    s1 = a1 - b1
    return s1
```
### Multiplication
``` py
def multiply(q, p):
    """
    This function returns the product of two input numbers.

    :param q: First input number.
    :type q: int
    :param p: Second input number.
    :type p: int
    :return: The product of the two input numbers.
    :rtype: int
    """
    result = q * p
    return result 
```
### Division
``` py
def divide(x, y):
    """
    This function returns the division result of two input numbers.

    :param x: Numerator.
    :type x: float
    :param y: Denominator.
    :type y: float
    :return: The division result of the two numbers.
    :rtype: float
    """
    result = x / y
    return result 
```
### Test File
``` py
import math
import os
import re
from collections import Counter


class Spamfilter:
    """A naive Bayesian spam filter"""

    def __init__(self, training_dir):
        """ inits Spamfilter with training data
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        print("Training filter with known ham ...")
        self.ham_table = dict(Counter(dir_tokens(training_dir + "ham/")))
        print("Training filter with known spam...")
        self.spam_table = dict(Counter(dir_tokens(training_dir + "spam/")))
        self.uniq_h_toks = len(self.ham_table)
        self.uniq_s_toks = len(self.spam_table)
        self.total_h_toks = sum(self.ham_table.values())
        self.total_s_toks = sum(self.spam_table.values())
        self.tok_arr = sorted(
            list(self.ham_table.keys()) + list(self.spam_table.keys())
        )
        self.freq_tab = self.create_frequency_table()
        self.file_count = 0
        self.count_spam = 0
        self.count_ham = 0
        self.spam_list = []
        self.ham_list = []

    def create_frequency_table(self):
        """ Generates token frequency table from training emails
        :return:  dict{k,v}:  spam/ham frequencies
        k = (str)token, v = {spam_freq: , ham_freq:, prob_spam:, prob_ham:}
        """
        freq_table = {}
        for tok in self.tok_arr:
            entry = {}
            s_freq = self.spam_table.get(tok, 0)
            entry["spam_freq"] = s_freq
            h_freq = self.ham_table.get(tok, 0)
            entry["ham_freq"] = h_freq
            s_prob = (s_freq + 1 / float(self.uniq_s_toks)) / (self.total_s_toks + 1)
            entry["prob_spam"] = s_prob
            h_prob = (h_freq + 1 / float(self.uniq_h_toks)) / (self.total_h_toks + 1)
            entry["prob_ham"] = h_prob
            freq_table[tok] = entry
        return freq_table

    def prob_spam(self, token):
        """calculates the probability that 'token' is found in spam emails

        :param token: (str)
        :return: (float) probability 'token' is spam based on training emails
        """
        val = self.freq_tab.get(token)
        if val is not None:
            return val["prob_spam"]
       
        return (1.0 / self.uniq_s_toks) / (self.total_s_toks + 1)

    def prob_ham(self, token):
        """calculates the probability that 'token' is found in ham emails

        :param token: (str)
        :return: (float) probability 'token' is ham based on training emails
        """
        val = self.freq_tab.get(token)
        if val is not None:
            return val["prob_ham"]
    
        return (1.0 / self.uniq_h_toks) / (self.total_h_toks + 1)

    def prob_msg_spam(self, filepath):
        """Calculates the probability that a message is spam

        :param filepath: (str) path of email
        :return: (float) probability message is spam
        """
        toks = file_tokens(filepath)
        sm = 0
        for tok in toks:
            sm += math.log10(self.prob_spam(tok))
        return sm

    def prob_msg_ham(self, filepath):
        """Calculates the probability that a message is ham

        :param filepath: (str) path of email
        :return: (float) probability message is ham
        """
        toks = file_tokens(filepath)
        sm = 0
        for tok in toks:
            sm += math.log10(self.prob_ham(tok))
        return sm

    def classify(self, filepath):
        """classifies a file as spam or ham based on training data

        :param filepath:
        :return: (boolean) True->spam, False->ham
        """
        self.file_count += 1
        if self.prob_msg_spam(filepath) > self.prob_msg_ham(filepath):
            self.count_spam += 1
            self.spam_list.append(filepath)
            return True
        else:
            self.count_ham += 1
            self.ham_list.append(filepath)
            return False

    def classify_all(self, dir_path, known_type="spam"):
        """Classifies all emails in a testing directory and maintains count of errors

        :param dir_path: path of testing directory
        :param known_type: str: the known type of testing directory
        """
        self.ham_list = []
        self.spam_list = []
        self.file_count = 0
        self.count_spam = 0
        self.count_ham = 0
        print("\nClassifying all emails found in directory: ./" + dir_path)

        try:
            for f in os.listdir(dir_path):
                self.classify(dir_path + f)
                if known_type == "spam":
                    correct = self.count_spam / float(self.file_count)
                else:
                    correct = self.count_ham / float(self.file_count)

            print("Total spam:{:8d}".format(self.count_spam))
            print("Total ham: {:8d}".format(self.count_ham))
            print("Correctly classified: {:6.2f}%".format(correct * 100))
        except FileNotFoundError as e:
            print("ERROR: classify_all() failed " + str(e))

    def clean_table(self, min_freq):
        """Removes entries from frequency table if they are deemed poor indicators.
        or if combined spam/ham frequency is below 'min_freq'

        :param min_freq: if total token count below threshold, delete from table
        """
        rm_keys = []
        for k, v in self.freq_tab.items():
            if (
                v["spam_freq"] + v["ham_freq"] < min_freq
                or 0.45 < (v["prob_spam"] / (v["prob_spam"] + v["prob_ham"])) < 0.55
            ):
                rm_keys.append(k)
        for k in rm_keys:
            print("deleting " + str(k) + " from freq table in clean()")
            del self.freq_tab[k]

    def print_table_info(self):
        """ Print training info:
            - unique tokens in ham and spam, number of emails in training set"""
        print("\n=======================================")
        print("TRAINING AND FREQUENCY TABLE INFO")
        print("=======================================")
        print("Unique tokens in spam messages:{:8d}".format(len(self.spam_table)))
        print("Unique tokens in ham messages: {:8d}".format(len(self.ham_table)))
        print("Unique tokens in ALL messages: {:8d}".format(len(self.freq_tab)))
        print("Num spam e-mails:{:22d}".format(len(os.listdir("emails/testing/spam/"))))
        print("Num ham e-mails: {:22d}".format(len(os.listdir("emails/testing/ham/"))))


def tokens(text, tok_size=3):
    """ Returns a list of all substrings contained in 'text' of size 'tok_size'

    :param text: (string) text to tokenize
    :param tok_size: length of substrings
    :return: (list) tokens of 'text'
    """
    return [text[i : i + tok_size] for i in range(len(text) - tok_size + 1)]


def clean_split(in_str):
    """ Removes all non-alphanum chars and splits string at whitespace, downcase

    :param in_str: (str) target string
    :return: (list) cleaned strings
    """
    return re.sub(r"[^\s\w]|_", "", in_str).lower().split()


def file_tokens(filepath):
    """ tokenizes all strings contained in 'filepath' after removing \
     all non-alphanum chars and splitting strings at whitespace

    :param filepath: path of target file
    :return: list of tokens
    """
    toks = []
    try:
        with open(filepath, encoding="utf8", errors="ignore") as fp:
            for line in fp:
                words = clean_split(line)
                toks.extend(words)
    except FileNotFoundError as e:
        print("Error:" + str(e))
    return [x for x in toks if len(x) < 10]


def dir_tokens(dir_path):
    """ tokenizes all files contained in 'dir_path'

    :param dir_path: directory containing files to be tokenized
    :return: list of tokens
    """
    dir_toks = []
    try:
        filenames = os.listdir(dir_path)
        for f in filenames:
            dir_toks.extend(file_tokens(dir_path + f))
    except FileNotFoundError as e:
        print("Error:" + str(e))
    return dir_toks


if __name__ == "__main__":
    spamfilter = Spamfilter("emails/training/")
    spamfilter.print_table_info()
    spamfilter.classify_all("emails/testing/spam/", "spam")
    spamfilter.classify_all("emails/testing/ham/", "ham") 
```
