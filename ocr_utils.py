
#For a Single Image 
import cv2
import easyocr

#read image 
image_path='test2.png'
img=cv2.imread(image_path)

#instance text detector -creating an instance 
reader= easyocr.Reader(['en'],gpu=False)
threshold=0.25



def extract_text_annotate_Image(image) :
    #detect text on image 
    text_details=reader.readtext(image)
    print(type(text_details))
    extracted_text = []
    
    #drawBBox and text
    for t in text_details : 
        print(t)
        bbox,text,score=t #unwrapping all the parameters 

        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        print(f"Drawing box from {top_left} to {bottom_right} with text: {text}")
        
        if score > threshold :
            cv2.rectangle(image,top_left,bottom_right,(0,255,0),5)
            cv2.putText(image,text,top_left,cv2.FONT_HERSHEY_COMPLEX,0.65,(255,255,255),2)
            extracted_text.append(text)

    return image,extracted_text

