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

def gen_img_art(frame, width):
    img_height, img_width = frame.shape[:2]
    ratio = img_height / img_width
    height = int(ratio * width * 0.5)
    img = cv2.resize(frame, (width, height))
    
    # convert to grayscale
    img = bgr2gray(img)
    
    # normalize values to our ascii_characters
    img = min_max_normalize(img)
    
    output = []
    for y in range(height):
        row = []
        for x in range(width):
            index = int(img[y, x])  # scale to ASCII index range
            row.append(ASCII_CHARS[index])
        output.append("".join(row))  # oin row into a single string
    
    return output
            
def gen_art(video_path, width = 100):
    cap = cv2.VideoCapture(video_path)
    
    ascii_frames = []

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # get video frame width, height, and FPS for output video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    
    frame_count = 0

    while True:
        # read frame from video
        ret, frame = cap.read()
        
        # exit if no more frames
        if not ret:
            break  
        
        frame_count += 1  
        # only process every 5th frame for now
        if frame_count % 5 == 0:
            art = gen_img_art(frame, width)
            
            # then write art to output
            ascii_frames.append(art)

    # release video capture object
    cap.release()
        
    return ascii_frames

def process_video(video_path, width=100):
    return gen_art(video_path, width)

# entry point
if __name__ == "__main__":
    ascii_frames = process_video("videoplayback.mp4", 150)

    import time
    for i, frame in enumerate(ascii_frames):
        print(f"Frame {i}:")
        print("\n".join(frame))
        print("\n" + "-"*150 + "\n")
        time.sleep(0.2)
   