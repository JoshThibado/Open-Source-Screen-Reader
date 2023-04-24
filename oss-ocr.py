from PIL import Image
import pytesseract

import cv2
font = cv2.FONT_HERSHEY_PLAIN

import pyttsx3

from TTS.api import TTS


def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports

def convert(frame):
    y=350
    x=137
    y2=460
    x2=500
    h=460
    w=500

    # Load from png
    #img_cv = cv2.imread(r'./test.png')
    
    # Load from frame
    #img_cv = frame[y:y2, x:x2]
    img_cv = frame
    
    #img_to_conv = cv2.resize(img_cv, (0,0), fx=4, fy=4) 
    #cv2.imshow('frame', img_cv)
    
    # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
    # we need to convert from BGR to RGB format/mode:
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    
    #cv2.imshow('Input', img_rgb)
    
    # OCR
    text = pytesseract.image_to_string(img_rgb, lang='eng')
    print(text)

    return text

def get_ocr_text():
    # Load from png
    img_cv = cv2.imread(r'/home/josh/projects/oss-ocr/test.png')
    
    # Load from frame
    #img_cv = frame[y:y2, x:x2]
    
    #img_to_conv = cv2.resize(img_cv, (0,0), fx=4, fy=4) 
    #cv2.imshow('frame', img_cv)
    
    # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
    # we need to convert from BGR to RGB format/mode:
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    
    #cv2.imshow('Input', img_rgb)
    
    # OCR
    text = pytesseract.image_to_string(img_rgb, lang='eng')
    print(text)
    return text

def ml_tts(input_text):
    # List available 🐸TTS models and choose the first one
    model_name = TTS.list_models()[0]
    print(model_name)
    # Init TTS
    tts = TTS(model_name)
    # Run TTS
    # ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
    # Text to speech with a numpy output
    wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])
    # Text to speech to a file
    tts.tts_to_file(text="Hello world!", speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")

def simple_tts(input_text):
    print("Input text is: " + input_text)
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    print (rate)                        #printing current voice rate
    engine.setProperty('rate', 150)     # setting up new voice rate
    engine.say(input_text)
    engine.runAndWait()


def main():
    sentence =  "Hello there, welcome to the world"
    #sentence = get_ocr_text()
    #ml_tts()
    #simple_tts(sentence)
    
    
    # Get input
    print(list_ports)
    videoCaptureObject = cv2.VideoCapture(0)
    
    while(True):
        ret,frame = videoCaptureObject.read()
        converted = convert(frame)
        cv2.imshow('Input', frame)
        if(cv2.waitKey(1) & 0xFF == ord('r')):
            simple_tts(converted)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            videoCaptureObject.release()
            cv2.destroyAllWindows()
    
    print("Program Ran")

if __name__ == "__main__":
    main()
