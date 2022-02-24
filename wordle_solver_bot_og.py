from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from wordle_solver import WordleSolver 
import time

class WordleSolverBotOG:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\Bratin Ghosh\OneDrive\Desktop\Drivers\chromedriver.exe")
        self.wordle_solver = None
        self.url = "https://www.powerlanguage.co.uk/wordle/"
        self.driver.get(self.url)

    def get_guess_word_mapping_by_row(self, row):
        time.sleep(3)
        mapping = ""

        for column in range(1, 6):
            element = self.driver.execute_script('return document.querySelector("game-app").shadowRoot.querySelector("game-theme-manager").querySelector("#game").querySelector("#board-container").querySelector("#board").querySelector("game-row:nth-child('+str(row)+')").shadowRoot.querySelector("div game-tile:nth-child('+str(column)+')")')
            evaluation = element.get_attribute("evaluation")
            mapping += evaluation[0]
        return mapping
    
    def enter_guess_word(self, word):
        # enter the letters
        for letter in word:
            time.sleep(1)
            actions = ActionChains(self.driver)
            actions.send_keys(letter)
            actions.perform()

        self.press_enter()
    
    def press_enter(self):
        # Press enter
        time.sleep(1)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def main(self):
        time.sleep(2)

        FLAG = True
        TURN = 1
        TOTAL_TURNS = 6

        self.wordle_solver = WordleSolver()

        words = self.wordle_solver.default_words
        rule = self.wordle_solver.default_rule
        guess_word = ""
        guess_word_mapping = "aaaaa"

        while (guess_word_mapping != "ccccc" and TURN <= TOTAL_TURNS):
            guess_word = self.wordle_solver.suggest_next_word(words, FLAG)
            self.enter_guess_word(guess_word)
            guess_word_mapping = self.get_guess_word_mapping_by_row(TURN)
            rule = self.wordle_solver.get_updated_rule(rule, guess_word, guess_word_mapping)
            words = self.wordle_solver.filter_words_by_rule(words, rule)
            
            # turn off the flag when the word list length is below a threshold
            if (len(words) < 5):
                FLAG = False

            TURN += 1
        
        if guess_word_mapping == "ccccc":
            print("Today's word is " + guess_word + ".")
        else:
            print("Sorry, the bot failed to find today's word.")

        time.sleep(2)

        # All windows related to driver instance will quit
        self.driver.quit()

wordle_solver_bot = WordleSolverBotOG()
wordle_solver_bot.main()
