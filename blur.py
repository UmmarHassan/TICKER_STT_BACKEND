

# import cv2
# import glob
# paths=glob.glob(r'D:\ticker_new\NinetyTwo_Ticker\*.jpg')
# for image_path in paths:

#     # image_path = r"D:\ticker_new\30.jpg"
#     imgColor = cv2.imread(image_path)
#     img = cv2.cvtColor(imgColor, cv2.COLOR_BGR2GRAY)

#     ret1, img1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#     ret2, img2 = cv2.threshold(img,192,255,cv2.THRESH_BINARY)

#     whitepixels1 = cv2.countNonZero(img1)
#     whitepixels2 = cv2.countNonZero(img2)
#     difference=whitepixels1-whitepixels2

#     print(difference)
#     if difference<3000 and difference>10: 
#         print('sharp')
#     else:
#         print('blurry')
   

#     print("img1 white pixels - %d" % whitepixels1)
#     print("img2 white pixels - %d" % whitepixels2)
#     cv2.imshow("Image", img)
#     key = cv2.waitKey(0)
import re

def compare_ocr_text_with_dictionary(ocr_text, dictionary_file, threshold):
    with open(dictionary_file, 'r', encoding='utf-8') as file:
        dictionary_words = {line.strip() for line in file}

    # ocr_words = set(ocr_text.split())
    # print('ocr_words',ocr_words)
    
    words_regex = re.findall(r'\b\w+\b', ocr_text, re.U)  # Add re.U flag for Unicode characters
    print('words_regex_list:', words_regex)

    words_set = set(words_regex)
    print('words_set:', words_set)

    total_words = len(words_regex)
    accurate_words = len(words_set.intersection(dictionary_words))
    print('word_regex',words_regex)

    accuracy_percentage = (accurate_words / total_words) * 100
    print('accuracy_percentage',accuracy_percentage)
    if accuracy_percentage < threshold:
        return False  # Discard the ticker
    else:
        return True  # Ticker is valid

# Example usage:
ocr_text="شہباز قمر اپنے ہونہار طلبا میں طریقے لیپ ٹاپ ؟"
dictionary_file = "words.txt"  # Path to the Urdu dictionary file
accuracy_threshold = 90  # Set the accuracy threshold percentage

if compare_ocr_text_with_dictionary(ocr_text, dictionary_file, accuracy_threshold):
    print("Ticker has accurate OCR text. Keep it.")
else:
    print("Ticker does not have accurate OCR text. Discard it.")
# import re

# urdu_text = "اسلام آباد : وفاقی وزیر خزانہ اسحاق ڈار کی گفتگویہ 9 ماہ کا پروگرام ہے اس میں 3 ارب ڈالر پاکستان کو ملیں گے، وزیر خزانہ"

# # Using split() method
# words = urdu_text.split()
# print(words)

# # Using regular expressions
# words_regex = re.findall(r'\b\w+\b', urdu_text)
# print(words_regex)

# import cv2
# import argparse
# import glob
# # ap = argparse.ArgumentParser()
# # ap.add_argument('-i', '--images', required=True,)
# # ap.add_argument('-t', '--threshold', type=float)
# # args = vars(ap.parse_args())
# # images = [cv2.imread(file) for file in glob.glob("{}/*.jpeg".format(args['images']))]
# # for image in images:
# image=cv2.imread(r"D:\ticker_new\30.jpg")
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# fm = cv2.Laplacian(gray, cv2.CV_64F).var()
# text = "Not Blurry"

# if fm < 100:
#     text = "Blurry"
# print(text)
# cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
#     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
# cv2.imshow("Image", image)
# cv2.waitKey(0)
# ***************
# import the necessary packages
# from imutils import paths
# import argparse
# import cv2
# def variance_of_laplacian(image):
# 	# compute the Laplacian of the image and then return the focus
# 	# measure, which is simply the variance of the Laplacian
# 	return cv2.Laplacian(image, cv2.CV_64F).var()
# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--images", required=True,
# 	help="path to input directory of images")
# ap.add_argument("-t", "--threshold", type=float, default=100.0,
# 	help="focus measures that fall below this value will be considered 'blurry'")
# args = vars(ap.parse_args())
# # loop over the input images
# for imagePath in paths.list_images(args["images"]):
# 	# load the image, convert it to grayscale, and compute the
# 	# focus measure of the image using the Variance of Laplacian
# 	# method
# 	image = cv2.imread(imagePath)
# 	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 	fm = variance_of_laplacian(gray)
# 	text = "Not Blurry"
# 	# if the focus measure is less than the supplied threshold,
# 	# then the image should be considered "blurry"
# 	if fm < args["threshold"]:
# 		text = "Blurry"
# 	# show the image
# 	cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
# 		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
# 	cv2.imshow("Image", image)
# 	key = cv2.waitKey(0)