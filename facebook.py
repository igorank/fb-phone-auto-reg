import pathlib
import time
import random
import vision
from config import Config
from helper import remove_line_by_text


class Facebook:

    def __init__(self, device):
        self.__device = device
        self.__config = Config()
        self.__device.shell(f'input tap {self.__config.get_coords("facebook_app")}')

    def check_init(self, timeout: int = 12) -> bool:
        start = time.time()
        elapsed_time = 0
        iterator = 0

        succ_init = 'data\\init.png'

        while elapsed_time <= timeout or iterator < 2:
            self.take_screenshot()
            if vision.compare_images('screencap.png', succ_init) < 5:
                return True

            end = time.time()
            elapsed_time = end - start
            iterator += 1
            # print(elapsed_time) # TEMP

        return False

    def check_checkpoint(self, email_data: tuple, timeout: int = 40) -> bool:
        start = time.time()
        elapsed_time = 0

        succ_reg_list = ['data\\succ_reg.png', 'data\\succ_reg2.png', 'data\\succ_reg3.png'
                         , 'data\\succ_reg4.png', 'data\\succ_reg5.png', 'data\\succ_reg6.png']
        fail_reg_list = ['data\\checkpoint.png']

        while elapsed_time <= timeout:
            self.take_screenshot()

            for i in succ_reg_list:
                if vision.compare_images('screencap.png', i) < 5:
                    return True

            for i in fail_reg_list:
                if vision.compare_images('screencap.png', i) < 5:
                    remove_line_by_text('emails.txt',
                                        str(email_data[0]))  # удаляем почту из txt файла
                    print("Checkpoint")
                    return False

            end = time.time()
            elapsed_time = end - start
        return False

    def __fill_names(self, name, surname, version: str = '1'):
        self.__device.shell(f'input tap {self.__config.get_coords("name_field_" + version)}')
        self.__device.shell(f'input text {name}')
        time.sleep(0.5)
        self.__device.shell(f'input tap {self.__config.get_coords("surname_field_" + version)}')
        self.__device.shell(f'input text {surname}')
        time.sleep(1)
        next_butt_coords = vision.get_coords("next_button.png")
        self.__device.shell(f'input tap {next_butt_coords}')
        time.sleep(3)

    def __tap_birth_date_coords(self) -> bool:
        self.take_screenshot()
        images = ["birth_date.png", "birth_date2.png", "birth_date3.png", "birth_date4.png"]
        for image in images:
            if vision.is_template_in_image('screencap.png', image):
                if image == "birth_date3.png":
                    return True
                birth_date_coords = vision.get_coords(image)
                # print("Birth date coordinates: " + birth_date_coords)  # TEMP
                self.__device.shell(f'input tap {birth_date_coords}')
                return True
        print("Can not find birth date coordinates")
        return False

    def __fill_date(self) -> bool:
        if self.__tap_birth_date_coords():
            time.sleep(1)
            self.__swipe_year()
            self.__swipe_month()
            self.__swipe_day()
            self.__device.shell(f'input tap {self.__config.get_coords("set_date")}')
            time.sleep(0.5)
            # self.take_screenshot()
            # next_butt_coords = vision.get_coords("next_button.png") # заменить на корд.
            self.__device.shell(f'input tap {self.__config.get_coords("next_date_window")}')
            time.sleep(2)
            return True
        return False

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
        self.take_screenshot()
        email_reg_butt = vision.get_coords("email_reg.png")
        self.__device.shell(f'input tap {email_reg_butt}')
        time.sleep(1)
        self.__device.shell(f'input text {email}')
        self.take_screenshot()
        next_butt = vision.get_coords("next_button.png")
        self.__device.shell(f'input tap {next_butt}')
        # self.__device.shell(f'input tap {self.__config.get_coords("next4")}')
        time.sleep(2)

    def __set_password(self, password):
        self.__device.shell(f'input text {password}')
        self.__device.shell(f'input tap {self.__config.get_coords("next5")}')
        time.sleep(2)
        self.take_screenshot()
        if vision.compare_images('screencap.png', 'data\\save_pass.png') < 5:
            self.__device.shell(f'input tap {self.__config.get_coords("not_save_pass")}')  # не всегда всплывает
        time.sleep(2)  # default = 2

    def __swipe_year(self):
        for _ in range(random.randint(4, 6)):
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

    def resend_code(self):
        codenotcome_butt = vision.get_coords("codedidntcome.png")  # заменить на корд.
        self.__device.shell(f'input tap {codenotcome_butt}')
        self.__device.shell(f'input tap {self.__config.get_coords("resend_code")}')

    def input_code(self, code):
        self.__device.shell(f'input text {code}')
        next_butt_coords = vision.get_coords("next_button.png")
        self.__device.shell(f'input tap {next_butt_coords}')

    def register(self, profile_data, email_data) -> bool:
        self.__device.shell(f'input tap {self.__config.get_coords("create_acc")}')
        time.sleep(3)
        self.__device.shell(f'input tap {self.__config.get_coords("start")}')
        time.sleep(3)

        self.__device.shell(f'input tap 300 675')  # TEMP
        time.sleep(0.5)
        self.take_screenshot()
        if vision.compare_images('screencap.png', 'data\\whatsurname.png') < 5:
            self.__fill_names(profile_data['name'], profile_data['surname'], '2')
        else:
            self.__fill_names(profile_data['name'], profile_data['surname'])

        if self.__fill_date():
            self.__select_gender(profile_data['gender'])
            self.__enter_email(email_data[0])
            self.__set_password(profile_data['password'])
            self.take_screenshot()
            accept_rules_coords = vision.get_coords()
            self.__device.shell(f'input tap {accept_rules_coords}')  # TEMP
            # time.sleep(40)
            return True
        return False

    def take_screenshot(self):
        self.__device.shell('screencap -p /sdcard/screencap.png')
        self.__device.pull('/sdcard/screencap.png',
                           str(pathlib.Path().resolve()) + '//screencap.png')

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
