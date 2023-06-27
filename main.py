import sys
import time
import random
import vision
from ppadb.client import Client as AdbClient
from selenium.common.exceptions import TimeoutException
from imap_tools.errors import MailboxLoginError
from password_generator import PasswordGenerator
from facebook import Facebook
from imapreader import EmailReader
from outlook import Outlook
from config import Config
from helper import remove_line_by_text


def check_connection(clnt):
    devices = clnt.devices()

    if len(devices) == 0:
        print('No devices')
        return None

    _device = devices[0]
    print(f'Connected to {_device}')
    return _device


def get_filesdata(filename):
    with open(filename, encoding='utf-8') as o_file:
        lines = o_file.read().splitlines()
    return lines


def load_data() -> dict:
    if random.randint(0, 1) == 0:
        names = get_filesdata('names\\names_lat.txt')
        surnames = get_filesdata('names\\surnames_lat.txt')
        gender = 0
    else:
        names = get_filesdata('names\\names_m_lat.txt')
        surnames = get_filesdata('names\\surnames_m_lat.txt')
        gender = 1
    emails = get_filesdata('emails.txt')
    return {'names': names, 'surnames': surnames,
            'gender': gender, 'emails': emails}


def get_email_data(random_email: str) -> tuple:
    email = random_email.split(';')[0]
    email_domain = email.split('@')[1]
    match email_domain:
        case "inbox.lv":
            return email, 'mail.inbox.lv', \
                rand_email.split(';')[2], rand_email.split(';')[1]
        case "outlook.com":
            return email, 'outlook.office365.com', \
                rand_email.split(';')[1], rand_email.split(';')[1]
        case "rambler.ru":
            return email, 'imap.rambler.ru', \
                rand_email.split(';')[1], rand_email.split(';')[1]


def generate_password() -> str:
    pwo = PasswordGenerator()
    pwo.minlen = 8  # (Optional)
    pwo.maxlen = 20  # (Optional)
    pwo.minuchars = 2  # (Optional)
    pwo.minlchars = 3  # (Optional)
    pwo.minnumbers = 1  # (Optional)
    pwo.minschars = 0  # (Optional)
    pwo.excludeschars = "!#$%^=<>&,()+-*?/;"
    return pwo.generate()


def get_fb_code(mail_obj, delay: int) -> (str or bool):
    try:
        code = mail_obj.get_facebook_code(delay)
        if code in {"Code did not come", "Timeout"}:
            fb.resend_code()
            return False
        return code
    except TimeoutException:
        print("BINGO")
        time.sleep(99999)  # TEMP
        return "Timeout"


def check_registration(comp_result: bool) -> (bool or str):
    if comp_result:  # default = 5
        print('Success')

        if email_data[1] == 'mail.inbox.lv' or email_data[1] == 'imap.rambler.ru':
            try:
                mail_obj = EmailReader(email_data[1], email_data[0], email_data[2])
            except MailboxLoginError:   # Invalid login or password
                print('Invalid login or password')
                remove_line_by_text('emails.txt',
                                    str(email_data[0]))  # удаляем почту из txt файла
                return False
        else:
            mail_obj = Outlook()
            mail_obj.login(email_data[0], email_data[2])
            # if not mail_obj.login(email_data[0], email_data[2]):
            #     remove_line_by_text('emails.txt',
            #                         str(email_data[0]))  # удаляем почту из txt файла
            #     print(email_data[0] + " has been banned")
            #     return False

        for _ in range(10):
            code = get_fb_code(mail_obj, 30)
            if code:
                return code


def compare(dest: list, source='screencap.png') -> bool:
    for i in dest:
        if vision.compare_images(source, i) < 5:
            return True
    return False


def check_verification(timeout: int = 22) -> bool:
    start = time.time()
    elapsed_time = 0

    succ_ver_list = ['data\\succ_ver.png', 'data\\succ_ver2.png',
                     'data\\succ_ver3.png', 'data\\succ_ver4.png',
                     'data\\succ_ver5.png', 'data\\succ_ver6.png']

    while elapsed_time <= timeout:
        fb.take_screenshot()

        if compare(succ_ver_list):
            print('Profile verified')
            with open("accounts.txt", "a") as file:
                file.write(str(email_data[0]) + ";" + str(password) + ";" + str(email_data[3]) + ";\n")
            remove_line_by_text('emails.txt',
                                str(email_data[0]))  # удаляем почту из txt файла
            return True
        elif vision.compare_images('screencap.png', 'data\\not_verified.png') < 5:
            print('Profile not verified')
            remove_line_by_text('emails.txt',
                                str(email_data[0]))  # удаляем почту из txt файла
            return False

        end = time.time()
        elapsed_time = end - start
        # print(elapsed_time)  # TEMP

    return False


def get_answer():
    try:
        value = int(input('How many iterations to make?\n'))
    except ValueError:
        print("Sorry, I didn't understand that.")
        return None
    if value <= 0:
        print("Sorry, your response must not be negative or equal to 0.")
        return None
    return value


if __name__ == '__main__':
    config = Config()
    client = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037

    device = check_connection(client)
    if device is None:
        sys.exit()

    number_of_profiles = get_answer()

    for _ in range(number_of_profiles):
        file_data = load_data()  # TEMP
        name = random.choice(file_data['names'])
        surname = random.choice(file_data['surnames'])
        try:
            rand_email = random.choice(file_data['emails'])
        except IndexError:  # пустой emails.txt
            sys.exit()
        password = generate_password()

        profile_data = {'name': name, 'surname': surname,
                        'password': password, 'gender': file_data['gender']}
        email_data = get_email_data(rand_email)

        fb = Facebook(device)
        if fb.check_init():
            if fb.register(profile_data, email_data):
                res = fb.check_checkpoint(email_data)
                ver_code = check_registration(res)
                if ver_code:
                    print(ver_code)
                    fb.input_code(ver_code)
                    check_verification()

        fb.clear_cache()
        fb.change_ip()
