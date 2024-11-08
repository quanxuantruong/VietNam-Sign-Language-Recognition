import cv2
import numpy as np
from model import *
from function import *
import os
from grammar_correction import *
import keyboard

# 1. New detection variables
sequence = []
sentence = []
grammar_result=[]
threshold = 0.9
count = 0
last_prediction = ''

cap = cv2.VideoCapture(1400)
# Set mediapipe model 
with mp_holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75) as holistic:
    while cap.isOpened():

        # Read feed
        ret, frame = cap.read()

        # Make detections
        image, results = mediapipe_detection(frame, holistic)

        # Draw landmarks
        draw_styled_landmarks(image, results)
        
        # 2. Prediction logic
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        # Clear the keypoints list for the next set of frames
        sequence = sequence[-30:]
        
        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            print(actions[np.argmax(res)])
            print(count)
            
            if res[np.argmax(res)] > threshold and actions[np.argmax(res)]!='none': 
                if len(sentence) > 0: 
                    if actions[np.argmax(res)] == last_prediction and actions[np.argmax(res)] != sentence[-1]:
                        count+=1
                else:
                    if actions[np.argmax(res)] == last_prediction:
                        count+=1 

                if count > 15:
                    count = 0
                    
                if len(sentence) > 0: 
                    if count > 10:
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                            count = 0
                else:
                    if count > 10:
                        sentence.append(actions[np.argmax(res)])
                        count = 0

                last_prediction = actions[np.argmax(res)]

        # Limit the sentence length to 7 elements to make sure it fits on the screen
        if len(sentence) > 3:
            sentence = sentence[-3:]

        # # Reset if the "Spacebar" is pressed
        if keyboard.is_pressed(' '):
            sentence, sequence , grammar_result = [], [], []
            
        # # Check if the list is not empty
        # if sentence:
        #     # Capitalize the first word of the sentence
        #     sentence[0] = sentence[0].capitalize()

        #  # Check if the sentence has at least two elements
        # if len(sentence) >= 2:
        #     # Check if the last element of the sentence belongs to the alphabet (lower or upper cases)
        #     if sentence[-1] in string.ascii_lowercase or sentence[-1] in string.ascii_uppercase:
        #         # Check if the second last element of sentence belongs to the alphabet or is a new word
        #         if sentence[-2] in string.ascii_lowercase or sentence[-2] in string.ascii_uppercase or (sentence[-2] not in actions and sentence[-2] not in list(x.capitalize() for x in actions)):
        #             # Combine last two elements
        #             sentence[-1] = sentence[-2] + sentence[-1]
        #             sentence.pop(len(sentence) - 2)
        #             sentence[-1] = sentence[-1].capitalize()

        # Perform grammar check if "Enter" is pressed
        if keyboard.is_pressed('enter'):
            # Record the words in the sentence list into a single string
            text = ' '.join(sentence)
            # Apply grammar correction tool and extract the corrected result
            grammar_result = grammar_correction(text)

        if grammar_result:
            # Calculate the size of the text to be displayed and the X coordinate for centering the text on the image
            textsize = cv2.getTextSize(grammar_result, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_X_coord = (image.shape[1] - textsize[0]) // 2

            # Draw the sentence on the image
            cv2.putText(image, grammar_result, (150, 470),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (144, 238, 144), 2, cv2.LINE_AA)
        else:
            # Calculate the size of the text to be displayed and the X coordinate for centering the text on the image
            # textsize = cv2.getTextSize(' '.join(sentence), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            # text_X_coord = (image.shape[1] - textsize[0]) // 2

            # print(text_X_coord)

            # Draw the sentence on the image
            cv2.putText(image, ' '.join(sentence), (150, 470),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)


        # Show to screen
        cv2.imshow('OpenCV Feed', image)

        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()