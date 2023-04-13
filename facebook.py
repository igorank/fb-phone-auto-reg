import pathlib
import time
import random
from config import Config


class Facebook:

    def __init__(self, device):
        self.__device = device
        self.__config = Config()
        self.__device.shell(f'input tap {self.__config.get_coords("facebook_app")}')
        time.sleep(6)
        self.__device.shell(f'input tap {self.__config.get_coords("create_acc")}')
        time.sleep(3)
        self.__device.shell(f'input tap {self.__config.get_coords("start")}')
        time.sleep(3)

    def __fill_names(self, name, surname):
        self.__device.shell(f'input tap {self.__config.get_coords("name_field")}')
        self.__device.shell(f'input text {name}')
        self.__device.shell(f'input tap {self.__config.get_coords("surname_field")}')
        self.__device.shell(f'input text {surname}')
        self.__device.shell(f'input tap {self.__config.get_coords("next")}')
        time.sleep(3)

    def __fill_date(self):
        self.__device.shell(f'input tap {self.__config.get_coords("date_field")}')
        time.sleep(1)
        self.__swipe_year()
        self.__swipe_month()
        self.__swipe_day()
        self.__device.shell(f'input tap {self.__config.get_coords("set_date")}')
        time.sleep(0.5)
        self.__device.shell(f'input tap {self.__config.get_coords("next2")}')
        time.sleep(2)

    def __select_gender(self, gender):
        if gender == 0:
            self.__device.shell(f'input tap {self.__config.get_coords("female_gender")}')
        else:
            self.__device.shell(f'input tap {self.__config.get_coords("male_gender")}')
        time.sleep(1)
        self.__device.shell(f'input tap {self.__config.get_coords("next3")}')
        time.sleep(1)

    def __enter_email(self, email):
        self.__device.shell(f'input tap {self.__config.get_coords("decline")}')
        time.sleep(1)
        self.__device.shell(f'input tap {self.__config.get_coords("use_email_butt")}')
        time.sleep(1)
        self.__device.shell(f'input text {email}')
        self.__device.shell(f'input tap {self.__config.get_coords("next4")}')
        time.sleep(1)

    def __set_password(self, password):
        self.__device.shell(f'input text {password}')
        self.__device.shell(f'input tap {self.__config.get_coords("next5")}')
        time.sleep(1)
        self.__device.shell(f'input tap {self.__config.get_coords("not_save_pass")}')
        time.sleep(1)

    def __swipe_year(self):
        for _ in range(random.randint(3, 5)):
            self.__device.shell(f'input swipe 720 1200 720 {str(random.randint(1712, 2012))} 500')
            time.sleep(0.5)

    def __swipe_month(self):
        for _ in range(random.randint(3, 6)):
            self.__device.shell(f'input swipe 530 1200 530 {str(random.randint(1712, 2012))} 500')
            time.sleep(0.5)

    def __swipe_day(self):
        for _ in range(random.randint(3, 6)):
            self.__device.shell(f'input swipe 330 1200 330 {str(random.randint(1712, 2012))} 500')
            time.sleep(0.5)

    def input_code(self, code):
        self.__device.shell(f'input text {code}')
        self.__device.shell(f'input tap {self.__config.get_coords("next6")}')

    def register(self, profile_data, email_data):
        self.__fill_names(profile_data['name'], profile_data['surname'])
        self.__fill_date()
        self.__select_gender(profile_data['gender'])
        self.__enter_email(email_data[0])
        self.__set_password(profile_data['password'])
        self.__device.shell(f'input tap {self.__config.get_coords("accept_rules")}')
        time.sleep(40)

    def take_screenshot(self):
        self.__device.shell('screencap -p /sdcard/screencap.png')
        self.__device.pull('/sdcard/screencap.png',
                           pathlib.Path().resolve().__str__() + '//screencap.png')

    def clear_cache(self):
        self.__device.shell('pm clear com.facebook.katana')

    def change_ip(self):
        self.__device.shell('am start -a android.settings.AIRPLANE_MODE_SETTINGS')
        time.sleep(2)
        self.__device.shell(f'input tap {self.__config.get_coords("airp_mode")}')
        time.sleep(3)
        self.__device.shell(f'input tap {self.__config.get_coords("airp_mode")}')
        time.sleep(1)
        self.__device.shell(f'input tap {self.__config.get_coords("mid_butt")}')
        time.sleep(2)
