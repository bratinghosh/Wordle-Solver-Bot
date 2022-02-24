from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from wordle_solver import WordleSolver 
import time

class WordleSolverBot:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\Bratin Ghosh\OneDrive\Desktop\Drivers\chromedriver.exe")
        self.wordle_solver = None
        self.url = "https://wordlegame.org/"
        self.driver.get(self.url)

    def get_guess_word_mapping_by_row(self, row):
        time.sleep(1)
        mapping = ""

        for column in range(1, 6):
            xpath = '//*[@id="root"]/div/div/div[4]/div['+str(row)+']/div['+str(column)+']'
            element = self.driver.find_element(By.XPATH, xpath)
            classname = element.get_attribute("class")
            if "elsewhere" in classname:
                mapping += "p"
            if "absent" in classname:
                mapping += "a"
            if "correct" in classname:
                mapping += "c"

        return mapping
    
    def enter_guess_word(self, word):
        # enter the letters
        for letter in word:
            time.sleep(2)
            actions = ActionChains(self.driver)
            actions.send_keys(letter)
            actions.perform()

        self.press_enter()
    
    def press_enter(self):
        # Press enter
        time.sleep(2)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def main(self):
        WINS = 0
        TOTAL_GAMES = 2

        for i in range(TOTAL_GAMES):
            time.sleep(1)

            FLAG = True
            TURN = 1
            TOTAL_TURNS = 6

            self.wordle_solver = WordleSolver()

            words = self.wordle_solver.default_words
            rule = self.wordle_solver.default_rule
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
                print("The word was", guess_word)
                WINS += 1

            self.press_enter()

        print("Games Played:", TOTAL_GAMES)
        print("Wins:", WINS)
        print("Win Percentage:", float(WINS / TOTAL_GAMES))

        # All windows related to driver instance will quit
        self.driver.quit()

wordle_solver_bot = WordleSolverBot()
wordle_solver_bot.main()
