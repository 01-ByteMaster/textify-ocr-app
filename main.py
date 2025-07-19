
##FOR 3 or multiple Images

import cv2
import os
import easyocr

# Input/output images folder paths
input_folder = 'images'
output_folder = 'outputs'
os.makedirs(output_folder, exist_ok=True)
threshold =0.25 

# Listing  all image files in the input folder
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]


reader = easyocr.Reader(['en'], gpu=False)

# Process each image
for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    img = cv2.imread(image_path)

    # Detect text
    text_details = reader.readtext(img)

    # Draw bounding boxes and text
    for bbox, text, score in text_details:
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        if score > threshold : 
            cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 2)
            cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Save processed image to output folder
    output_path = os.path.join(output_folder, f"processed_{image_file}")
    cv2.imwrite(output_path, img)

    print(f'Processed and saved: {output_path}')


    
