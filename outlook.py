import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected_condition


class Outlook(webdriver.Chrome):

    def __init__(self) -> None:
        # self.__options = webdriver.ChromeOptions()
        # self.__options.add_argument("--headless=new")
        # super().__init__(options=self.__options)
        super().__init__()

    def __wait_for_code(self, delay: int) -> str:
        for _ in range(delay):
            if "ваш код подтверждения для Facebook" in self.page_source:
                element = self.find_element(By.XPATH,
                                            "//*[contains(text(), 'ваш код подтверждения для Facebook')]")
                return element.text[:5]
            time.sleep(1)
        return "Code did not come"

    def get_code(self, email: str, password: str, delay: int):
        self.get("https://go.microsoft.com/fwlink/p/?linkid=2125442&clcid=0x419&culture=ru-ru&country=ru")
        self.find_element(By.ID, 'i0116').send_keys(email)
        WebDriverWait(self, 6).until(expected_condition.element_to_be_clickable(
            (By.ID, 'idSIButton9'))).click()
        WebDriverWait(self, 6).until(expected_condition.element_to_be_clickable(
            (By.ID, 'i0118'))).send_keys(password)
        # self.find_element(By.ID, 'i0118').send_keys(password)
        WebDriverWait(self, 6).until(expected_condition.element_to_be_clickable(
            (By.ID, 'idA_PWD_ForgotPassword')))
        self.find_element(By.ID, 'idSIButton9').click() # BUG

        try:
            WebDriverWait(self, 6).until(expected_condition.element_to_be_clickable(
                (By.ID, 'idBtn_Back'))).click()
        except TimeoutException:
            self.execute_script("arguments[0].click();", WebDriverWait(self, 8).until(
                expected_condition.element_to_be_clickable((By.ID, 'iShowSkip'))))
            # self.find_element(By.ID, 'iShowSkip').click()
            WebDriverWait(self, 6).until(expected_condition.element_to_be_clickable(
                (By.ID, 'idBtn_Back'))).click()
            WebDriverWait(self, 6).until(expected_condition.element_to_be_clickable(
                (By.ID, 'iCancel'))).click()
        WebDriverWait(self, 40).until(expected_condition.visibility_of_element_located(
            (By.ID, '1-panel')))
        code = self.__wait_for_code(delay)

        if not code:
            return code

        self.close()
        return code
