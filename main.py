import cv2
import time
import random
import numpy as np
from ppadb.client import Client as AdbClient
from password_generator import PasswordGenerator
from facebook import Facebook
from imapreader import EmailReader
from outlook import Outlook
from config import Config


def check_connection(clnt):
    devices = clnt.devices()

    if len(devices) == 0:
        print('No devices')
        return None

    _device = devices[0]
    print(f'Connected to {_device}')
    return _device


def get_filesdata(filename, use_emails=False):
    if use_emails:
        with open(filename) as file:
            lines = file.read().splitlines()
    else:
        with open(filename, encoding='utf-8') as file:
            lines = file.read().splitlines()
    return lines


def load_data() -> dict:
    if random.uniform(0, 1) == 0:
        names = get_filesdata('names\\names_lat.txt')
        surnames = get_filesdata('names\\surnames_lat.txt')
        gender = 0
    else:
        names = get_filesdata('names\\names_m_lat.txt')
        surnames = get_filesdata('names\\surnames_m_lat.txt')
        gender = 1
    emails = get_filesdata('emails.txt', True)
    return {'names': names, 'surnames': surnames,
            'gender': gender, 'emails': emails}


# define the function to compute MSE between two images
def comp_mse(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff ** 2)
    mse = err / (float(h * w))
    return mse, diff


def compare_images(image1: str, image2: str) -> float:
    # load the input images
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    # convert the images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    error, diff = comp_mse(img1, img2)
    print("Image matching Error between the two images:", error)
    return error


def get_email_data(random_email: str) -> tuple:
    email = random_email.split(';')[0]
    email_domain = email.split('@')[1]
    if email_domain == "inbox.lv":
        return email, 'mail.inbox.lv', rand_email.split(';')[2]
    return email, 'outlook.office365.com', rand_email.split(';')[1]


def generate_password() -> str:
    pwo = PasswordGenerator()
    pwo.minlen = 8  # (Optional)
    pwo.maxlen = 20  # (Optional)
    pwo.minuchars = 2  # (Optional)
    pwo.minlchars = 3  # (Optional)
    pwo.minnumbers = 1  # (Optional)
    pwo.minschars = 0  # (Optional)
    pwo.excludeschars = "!$%^=<>&,()+-*?/"
    return pwo.generate()


def get_fb_code(delay: int) -> str:
    if email_data[1] == 'mail.inbox.lv':
        mail_reader = EmailReader(email_data[1], email_data[0], email_data[2])
        return mail_reader.get_facebook_code(delay)
    outlook_reader = Outlook()
    return outlook_reader.get_code(email_data[0], email_data[2], delay)


if __name__ == '__main__':
    config = Config()
    client = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037

    device = check_connection(client)
    if device is None:
        quit()

    for _ in range(2):
        file_data = load_data() # TEMP
        name = random.choice(file_data['names'])
        surname = random.choice(file_data['surnames'])
        rand_email = random.choice(file_data['emails'])
        password = generate_password()

        profile_data = {'name': name, 'surname': surname,
                        'password': password, 'gender': file_data['gender']}
        email_data = get_email_data(rand_email)

        fb = Facebook(device)
        fb.register(profile_data, email_data)

        fb.take_screenshot()
        img_match = compare_images('screencap.png', 'data\\succ_reg.png')
        if img_match < 5:
            print('Success')
            code = get_fb_code(300) # TEMP "Code did not come"
            print(code)
            fb.input_code(code)
            time.sleep(18)

            fb.take_screenshot()
            ver_match = compare_images('screencap.png', 'data\\succ_ver.png')
            if ver_match < 5:
                print('Profile verified')
                with open("accounts.txt", "a") as file:
                    file.write(str(email_data[0]) + ";" + str(password) + ";" + str(email_data[2]) + ";\n")
        fb.clear_cache()
        fb.change_ip()
