import os
import google.generativeai as genai
import PIL
import csv
import re
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

apikey = "enter your own apikey"
genai.configure(api_key=apikey, transport='rest')

model = genai.GenerativeModel('gemini-1.5-pro')

img_path = './yourown path for recognition (yingqiwenyuan or O2BR)/img'

for file in tqdm(os.listdir(img_path)):
    img = PIL.Image.open(img_path+file)
    w, h = img.size
    print(w, h)
    print(img_path+file)
    try:
        prompt = "How many oracle bone character in this image? Return a bounding box for each detected oracle bone character in [ymin, xmin, ymax, xmax] format."
        response = model.generate_content([img, prompt])


        coordinates = []
        lines = response.text.strip().split('\n')
        pattern = re.compile(r'-\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]')
        for line in lines:
            match = pattern.search(line)
            if match:
                ymin, xmin, ymax, xmax = map(int, match.groups())
                ture_ymin = int(ymin*h/1000)
                ture_xmin = int(xmin*w/1000)
                true_ymax = int(ymax*h/1000)
                true_xmax = int(xmax*w/1000)
                coordinates.append([ture_ymin, ture_xmin, true_ymax, true_xmax])

        print(coordinates)

        image = cv2.imread(img_path+file)
        filename = file[:-4]

        for (ymin, xmin, ymax, xmax) in coordinates:
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


        plt.figure()
        plt.imshow(image_rgb)
        plt.axis('off') 
        # plt.show()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.savefig("./gemini15pro/img/" + filename[:-4] + '.png')
        plt.close()
        
        file_path = './gemini15pro/annotation/' + filename[:-4] + '.csv'

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ymin', 'xmin', 'ymax', 'xmax']) 
            writer.writerows(coordinates)

        print(f"Save to {file_path}")
        time.sleep(3)
    
    except Exception as general_error:
    # Handle errors such as timeout
        print(f"Unexpected error with {file}: {str(general_error)}")
        continue  # Break the loop or raise the error
