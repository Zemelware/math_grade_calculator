from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import login_info
import os


class MathGradeCalculator:
    def __init__(self):
        os.environ["WDM_LOG_LEVEL"] = "0"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        # Edsby won't work if we don't do this
        options.add_argument(f'user-agent={user_agent}')
        options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        # Always wait max 15 seconds for elements to load
        self.driver.implicitly_wait(15)
        # TODO: Change this to accept the link as input in the future
        self.driver.get(
            "https://tchat.edsby.com/p/MyWorkStudent/132691411?student=87530786&label=My%20Work")
        grades = self.__load_grades()
        self.__calculate_overall(grades)

    def __load_grades(self):
        grades = {'Knowledge': [], 'Thinking': [],
                  'Communication': [], 'Application': []}

        username_field = self.driver.find_element(
            By.ID, '3loginform-login-userid__f__')
        username_field.send_keys(
            login_info.username, Keys.TAB, login_info.password, Keys.ENTER)

        # Wait for the page to load
        wait = WebDriverWait(self.driver, 15)
        # If a div with a grade is located, that means the page should be loaded
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'MyWorkAssessmentComponent-details-body-content-gradebox-grades-bucket')))

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        self.driver.quit()

        for grade in soup.find_all('div', class_='MyWorkAssessmentComponent-details-body-content-gradebox-grades-bucket'):
            # Inside this div will be the category and the grade (e.g., Knowledge 10/10)
            children = grade.find_all('div')

            # Save the grade to the appropriate category in the dictionary
            grades[children[0].text].append(children[1].text)

        return grades

    def __calculate_overall(self, grades_dict):
        weightings = {'Knowledge': 0.4, 'Thinking': 0.15,
                      'Communication': 0.1, 'Application': 0.35}
        overall = 0
        for category, grades in grades_dict.items():
            cat_marks_earned = 0
            cat_total = 0
            for grade in grades:
                cat_marks_earned += float(grade.split('/')[0])
                cat_total += float(grade.split('/')[1])
            overall += (cat_marks_earned / cat_total) * weightings[category]

        print(f"Overall Math Grade: {round(overall * 100, 2)}%")


if __name__ == "__main__":
    MathGradeCalculator()
