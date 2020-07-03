from selenium import webdriver
from bs4 import BeautifulSoup
from googletrans import Translator
import time
import random
import requests

class RiceBot:
    def __init__(self, category):
        '''
        Parameters
        ----------
        category : str
            The cateogry from freerice.com that the bot will answer questions of
        '''
        self.category = category

        self.driver = webdriver.Firefox(executable_path=r'./geckodriver')
        self.driver.get('https://freerice.com/categories/' + self.category)

        # giving the website enough time to load in
        time.sleep(5)

    def run(self, num_questions):
        '''
        Runs the bot on the appropriate category for the given number
        of questions. If the category isn't supported by the bot then
        this method does nothing.

        Parameters
        ----------
        num_questions : int
            The number of questions for the bot to answer
        '''

        if num_questions <= 0:
            return
            
        if self.category == "english-vocabulary":
            self.run_english_vocab(num_questions)
        elif self.category == "multiplication-table":
            self.run_mult_table(num_questions)
        elif self.category == "spanish":
            self.run_language(num_questions, "spanish")
        elif self.category == "french":
            self.run_language(num_questions, "french")
        elif self.category == "italian":
            self.run_language(num_questions, "italian")
        elif self.category == "german":
            self.run_language(num_questions, "german")
        elif self.category == "czech":
            self.run_language(num_questions, "czech")
        elif self.category == "famous-quotations":
            self.run_quotations(num_questions)
        else:
            return

    def run_english_vocab(self, num_words):
        '''
        Attempts to correctly answer the given number of vocabulary questions. 
        It has about an 80% accuracy rate by searching the given word on thesaurus.com and
        scraping the synonyms to figure out the best possible answer.

        Parameters
        ----------
        num_words : int
            The number of vocabulary questions for the bot to answer
        '''

        for i in range(num_words):
            time.sleep(random.random() * 4 + 2) # enough time to simulate reading the question

            found_syn = False

            # initializing the question word and its synonyms from thesaurus.com
            question_word = self.init_question().text.split()[0]
            synonyms = self.find_synonyms(question_word)

            # intializing the four options
            options = self.init_options()
            
            # checking if any of the options are listed as synonyms on thesaurus.com
            for option in options:
                if option.text in synonyms:
                    option.click()
                    found_syn = True
                    break

            # if no synonyms are found, randomly choose an option
            if not found_syn:
                options[random.randint(0,3)].click()

            print("Finished with word", str(i+1))
            time.sleep(5) # enough time for the next question to pop up

        print("Done!")

    def run_mult_table(self, num_questions):
        '''
        Attempts to correctly answer the given number of multiplication questions. 
        It has a 100% accuracy rate by conducting the multiplication and then clicking the option
        with the correct answer.

        Parameters
        ----------
        num_questions : int
            The number of multiplication questions for this bot to answer
        '''

        for i in range(num_questions):
            time.sleep(random.random() * 4 + 2) # enough time to simulate reading the question

            # initializing the two numbers being multiplied
            equation = self.init_question()
            num1 = int(equation.text.split(" x ")[0])
            num2 = int(equation.text.split(" x ")[1])

            # initializing the four options
            options = self.init_options()

            # choosing the option that contains the right answer to the multiplication
            for option in options:
                if num1 * num2 == int(option.text):
                    option.click()
                    break

            print("Finished with question", str(i+1))
            time.sleep(5) # enough time for the next question to pop up

        print("Done!")

    def run_language(self, num_questions, language):
        '''
        Attempts to correctly answer the given number of language translation questions. 
        It has about a 90% accuracy rate by using an unofficial google translate api to translate the
        question and find the best option.

        Parameters
        ----------
        num_questions : int
            The number of questions for the bot to answer

        language : str
            The language of the question for the bot to answer
        '''

        for i in range(num_questions):
            time.sleep(random.random() * 4 + 2) # enough time to simulate reading the question

            # initializing the question and its translation in the given language
            question = self.init_question().text.split(" means")[0]
            translation = Translator().translate(question, src = language).text

            # initializing the four options
            options = self.init_options()
            found_trans = False

            # clicks on the option that is similar to the translation
            for option in options:
                if self.semi_equals(option.text, translation):
                    option.click()
                    found_trans = True
                    break
            
            # if none of the options are similar to the translation, choose a random one
            if not found_trans:
                options[random.randint(0,3)].click()

            print("Finished with question", str(i+1))
            time.sleep(5) # enough time for the next question to pop up

        print("Done!")

    def run_quotations(self, num_questions):
        '''
        Attempts to correctly answer the given number of famous quotation questions. 
        It has about a 90% accuracy rate by searching the given quotation on google and scraping
        the results to see whose name appears the most in them.

        Parameters
        ----------
        num_questions : int
            The number of quotation questions for this bot to answer
        '''

        for i in range(num_questions):
            time.sleep(random.random() * 4 + 2) # enough time to simulate reading the question

            # initializing the quote
            question = self.init_question().text

            # initializing the four options
            options = self.init_options()

            # clicking the option whose name pops up when the quote is searched on google
            self.find_quote_source(question, options).click()

            print("Finished with question", str(i+1))
            time.sleep(5) # enough time for the next question to load in

        print("Done!")

    def init_options(self):
        '''
        Finds the four options by their XPath and returns an array of all the options.

        Returns
        -------
        list
            a list representing the four possible answers to the current question

        '''

        options = []

        for j in range(2,6):
            options.append(self.driver.find_element_by_xpath('//*[@id="root"]/section/div/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div[' + str(j) + ']'))

        return options

    def init_question(self):
        '''
        Finds the question by its XPath and returns it.

        Returns
        -------
        element
            the element representing the current question
        '''

        return self.driver.find_element_by_xpath("//*[@id=\"root\"]/section/div/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div[1]")


    def find_synonyms(self, word):
        '''
        Takes in a word and then searches that word up on thesaurus.com
        and uses BeautifulSoup to return a list of synonyms of the given word and any related words.

        Parameters
        ----------
        word : str
            The word being looked up on thesaurus.com

        Returns
        -------
        list
            a list of the synonyms of the given word and any related words
        '''

        html = requests.get("https://www.thesaurus.com/browse/" + word + "?s=t").text
        soup = BeautifulSoup(html, "lxml")
        
        # creating a list of the synonyms of the original word
        # and the synonyms of any related words
        synonym_tags = soup.find_all("div", class_ = "css-43mn45-ContentCard e1qo4u831")
        synonym_tags.append(soup.find("div", class_ = "css-191l5o0-ClassicContentCard e1qo4u830"))
        synonyms = []
        
        # check if there are any synonym tags and, if not, return an empty list of synonyms
        if synonym_tags != None:
            for tag in synonym_tags:
                if tag != None:
                    synonyms.extend(tag.find_all("span", class_ = "css-1y6i96q-WordGridItemBox etbu2a32"))
        else:
            return []
        
        # add the text of each synonym tag to the final list of synonyms
        list_of_syns = []
        
        for syn in synonyms:
            if syn.find("a") != None:
                list_of_syns.append(syn.find("a").get_text())

        # since the definition sometimes contains synonyms that aren't included in the actual
        # synonym list, we split the definition by commas and add every item in that list to 
        # the list of synonyms
        definition = soup.find("strong")
        if definition != None:
            list_of_syns.extend(definition.get_text().split(", "))
                
        return list_of_syns # final list of synonyms

    def semi_equals(self, word1, word2):
        '''
        Returns whether or not either of the given strings is a substring of the other.

        Parameters
        ----------
        word1 : str
            The first string
        
        word2 : str
            The second string

        Returns
        -------
        boolean
            a boolean determining if the either of the two strings is a substring of the other
        '''

        s1 = word1.upper()
        s2 = word2.upper()

        return s1 in s2 or s2 in s1

    def find_quote_source(self, quote, options):
        '''
        Given a list of the options, returns the option whose name appears the most when
        the given quote is searched on Google.

        Parameters
        ----------
        quote : str
            The quote being searched on google

        options : list
            A list of the possible answers of who said the given quote

        Returns
        -------
        element
            An element representing the answer to who said the given quote
        '''

        html = requests.get("https://www.google.com/search?q=" + quote).text
        soup = BeautifulSoup(html, "lxml")
        search_results = soup.get_text() # the text of the google search results

        # a dictionary to see which name has the highest frequency
        freq_dict = {}
    
        for option in options:
            freq_dict[option] = search_results.count(option.text)

        # returning the option with the highest frequency
        max_option = max(freq_dict.items(), key = lambda option : option[1])
        return max_option[0]