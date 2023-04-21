import cv2
import numpy as np


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

    error, _ = comp_mse(img1, img2)
    print("Image matching Error between the two images:", error)
    return error


def get_accept_rules_coords() -> str:
    screenshot = cv2.imread("screencap.png", 0)
    template = cv2.imread("template.png", 0)

    h, w = template.shape

    res = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF)

    # threshold  = 0.1
    # loc = np.where (res >= threshold)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    return str(int(min_loc[0] + (w / 2))) + " " + str(int(min_loc[1] + (h / 2)))
