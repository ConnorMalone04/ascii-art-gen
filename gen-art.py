import cv2
import numpy as np

ASCII_CHARS = ["@", "#", "8", "&", "%", "$", "?", "*", "+", ";", ":", ",", ".", " "]

# convert to grayscale with luminance formula
def bgr2gray(bgr):
    return np.dot(bgr[...,:3], [0.1140, 0.5870, 0.2989])

# min/max normalization for the ascii characters
def min_max_normalize(data):
        min_vals = np.min(data)
        max_vals = np.max(data)
    
        return ((data - min_vals) / (max_vals - min_vals)) * (len(ASCII_CHARS) - 1)

def gen_art(img_path, width = 100):
    img = cv2.imread(img_path)
    if img is None:
        print("Error: Image could not be opened.")
    else:
        # resize img to specified width
        img_height, img_width = img.shape[:2]
        ratio = img_height / img_width
        height = int(ratio * width * 0.5)
        img = cv2.resize(img,(width, height))
        
        # convert to grayscale
        img = bgr2gray(img)
        
        # normalize values to our ascii_characters
        img = min_max_normalize(img)
        
        #output = [[ASCII_CHARS[img[x][y]] for x in range(width)] for y in range(height)]
        output = []
        for y in range(height):
            row = []
            for x in range(width):
                index = int(img[y, x])  # scale to ASCII index range
                row.append(ASCII_CHARS[index])
            output.append("".join(row))  # oin row into a single string
        
        # print the ASCII art
        for row in output:
            print(row)
                
gen_art("cat.png",50)
        
        
        
        
        
        
        
    
    
    
