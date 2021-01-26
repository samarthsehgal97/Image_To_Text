try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import csv
import os
from pytesseract import Output
UPLOAD_FOLDER = 'static/uploads/'


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    image = cv2.imread(os.path.join(UPLOAD_FOLDER,filename.filename))
    # im1 = Image.open(filename)
    #converting image into gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # converting it to binary image by Thresholding
    # this step is require if you have colored image because if you skip this part
    # then tesseract won't able to detect text correctly and this will give incorrect result
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


    #configuring parameters for tesseract
    custom_config = r'--oem 3 --psm 6'
    # now feeding image to tesseract
    details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')


    total_boxes = len(details['text'])
    for sequence_number in range(total_boxes):
 	      if int(details['conf'][sequence_number]) >30:
 		           (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
 		           threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)


    parse_text = []
    word_list = []
    last_word = ''
    for word in details['text']:
        if word!='':
            word_list.append(word)
            last_word = word
        if (last_word!='' and word == '') or (word==details['text'][-1]):
            parse_text.append(word_list)
            word_list = []
    # UPLOAD_FOLDER = 'static/uploads/'
    # text = pytesseract.image_to_string(im1)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    # im1=im1.save(os.path.join(UPLOAD_FOLDER,filename.filename))
    with open('Output.txt',  'w', newline="") as file:
        csv.writer(file, delimiter=" ").writerows(parse_text)
    return parse_text
