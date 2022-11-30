## Q1 Computer Vision
---

### Enviorment Setup
1. Install python 3
2. Install packages in requirements.txt using pip

---

### Execution
Use the following command to run the program
> python image_puzzle.py {path_to_image_fuzzle_folder}

For example, if the image pieces are present in the folder `fumo` run:
> python image_puzzle.py fumo

The program will display a window showing the solved image puzzle

---

### Architecture
The program uses OpenCV to process a image into a numpy array. Separate bit masks for detecting red and blue dots are used in the image to highlight red and blue dots in the image. The contour finding algorithm in opencv is then used to detect the number of red and blue dots. 

After processing all the image pieces, they are then arranged and concatenated in the right order to create the final assembled image. Opencv is then used to display this image
