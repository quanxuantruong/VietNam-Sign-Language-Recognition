import cv2
import numpy as np
from model import *
from function import *
import os
from tensorflow.keras.models import load_model

# 1. New detection variables
sequence = []
sentence = []
predictions = []
threshold = 0.5

actions = np.array(['hello', 'thanks', 'iloveyou'])

# Load the trained model
model = load_model('my_model')


cap = cv2.VideoCapture(1400)
# Set mediapipe model 
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
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
        sequence = sequence[-30:]
        
        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            print(actions[np.argmax(res)])
            predictions.append(np.argmax(res))
            
            
        #3. Viz logic
        if np.unique(predictions[-10:])[0]==np.argmax(res): 
            if res[np.argmax(res)] > threshold: 
                
                if len(sentence) > 0: 
                    if actions[np.argmax(res)] != sentence[-1]:
                        sentence.append(actions[np.argmax(res)])
                else:
                    sentence.append(actions[np.argmax(res)])

        if len(sentence) > 5: 
            sentence = sentence[-5:]

        # cv2.putText(image, ' '.join(sentence), (3,30), 
        #                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Calculate the size of the text to be displayed and the X coordinate for centering the text on the image
        textsize = cv2.getTextSize(grammar_result, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_X_coord = (image.shape[1] - textsize[0]) // 2

        # Draw the sentence on the image
        cv2.putText(image, grammar_result, (text_X_coord, 470),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Show to screen
        cv2.imshow('OpenCV Feed', image)

        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()