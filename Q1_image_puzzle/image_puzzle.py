import argparse
import numpy as np
import cv2 as cv
from copy import deepcopy
from glob import glob
import os

# Get the number of red dots in the image
def get_num_red_dots(img: np.ndarray) -> int:
    # Get the RG and B channels as separate numpy arrays
    b, g, r = cv.split(img)
    # generate a bit mask for the highlighting the red dots.
    # each red dot lie in the range RGB(200,0,0) -> RGB(255, 20, 20)
    r_mask = (r>=200) & (r<=255)
    g_mask = (g>=0) & (g<=20)
    b_mask = (b>=0) & (b<=20)
    red_dot_mask = b_mask & g_mask & r_mask
    # set pixels where bit mask is true to 255. Set every other pixel as 0
    # this ensures that the image gets transformed into a black and white image where
    # onlt the red dot is highlighted in white while every thing else is black
    img[red_dot_mask] = 255
    img[~red_dot_mask] = 0
    # use the findCountours function from opencv to detect the number of white dots
    contours = cv.findContours(img[:, :, 0], cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return len(contours[0])


# Get the number of red dots in the image
def get_num_blue_dots(img: np.ndarray) -> int:
    # Get the RG and B channels as separate numpy arrays
    b, g, r = cv.split(img)
    # generate a bit mask for the highlighting the blue dots.
    # each red dot lie in the range RGB(0,0,200) -> RGB(20, 20, 255)
    r_mask = (r>=0) & (r<=20)
    g_mask = (g>=0) & (g<=20)
    b_mask = (b>=200) & (b<=255)
    blue_dot_mask = b_mask & g_mask & r_mask
    # set pixels where bit mask is true to 255. Set every other pixel as 0.
    # This ensures that the image gets transformed into a black and white image where
    # only the blue dot is highlighted in white while every thing else is black
    img[blue_dot_mask] = 255
    img[~blue_dot_mask] = 0
    # Use the findCountours function from opencv to detect the number of white dots
    contours = cv.findContours(img[:, :, 0], cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return len(contours[0])



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('base_folder', type=str, help='Location of folder having the image puzzle pieces')
    args = parser.parse_args()
    
    # base_folder = 'Validation Test-20220415T052724Z/Validation Test/saturn/'
    base_folder = args.base_folder
    img_files = glob(os.path.join(base_folder, '*'))
    if len(img_files) == 0:
        print('No image foles found. Please check the base folder location')
        exit()

    pieces = dict()
    for fp in img_files:
        img = cv.imread(fp)
        n_reds = get_num_red_dots(deepcopy(img))
        n_blues = get_num_blue_dots(deepcopy(img))
        pieces[(n_blues, n_reds)] = img

    full_img = []
    num_rows = max(map(lambda x: x[0], pieces.keys()))
    num_cols = max(map(lambda x: x[1], pieces.keys()))
    for ridx in range(1, num_rows+1):
        row = [pieces[(ridx, cidx)]for cidx in range(1, num_cols+1)]
        row = np.hstack(row)
        full_img.append(row)

    full_img = np.vstack(full_img)
    cv.imshow('full_image', full_img)
    cv.waitKey(0)
    cv.destroyAllWindows()



