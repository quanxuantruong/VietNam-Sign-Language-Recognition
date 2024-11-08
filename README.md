# Sign-Language-Recognition

This project is aimed at developing a Neural Network using LSTM and Dense layers to translate VietNamese sign language into text (natural language). It enables real-time recognition as well as grammar correction of recognited sentences. 

### Key Features:
* User-friendly data collection process for creating custom sign language datasets.
* Real-time recognition base on action landmarks, include: face, two-hand, pose.
* Integration of LLAMA3 to perform grammar correction.

<p align="center"> <img src="img/1_1.gif" alt="drawing" width="450"/> </p>

## Description

The whole project can be split into three main parts:
1. Data collection.
2. Model training.
3. Real time predictions.

## Data Collection

[MediaPipe Holistic](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/holistic.md) pipeline was used to record the data from the user's actions. Using [MediaPipe Holistic](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/holistic.md) instead of [MediaPipe Hands](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/hands.md) has improved the accuracy and diversity of the data, it processes each frame sent through it and results in the pose, face, left hand, and right hand components neatly stored in a variable. Each of the components can be represented by landmarks (these components' coordinates). In this case, only the hands' components' landmarks are being extracted resulting in overall 1626 data entries.

## Model Training

After the data has been collected and the dataset is complete, the user can proceed with the model training. In this step, the dataset is split into two subsets: 90% of the dataset is used for training and 10% for testing. The accuracy of testing using this 10% of the dataset will provide insight into the efficiency of the model.

For this particular project, the Neural Network is built using a Sequential model instance by passing three LSTM and three Densely-connected layers. The first five of these layers use the ReLU activation function with the last layer using the Softmax activation function. In the process of training, the Adam optimization algorithm is used to obtain optimal parameters for each layer.

Once the Neural Network is compiled, one can proceed with the model training and testing. During this step, the user can provide the model with the training subset, associated labels, and the number of epochs. Depending on the size of the provided subset and the number of epochs the training process can take up to a few minutes. Following the training, one can assess the model by performing predictions using the testing subset and evaluating the accuracy of these predictions.

## Real Time Predictions

In this step, the Neural Network is ready to apply everything it has learned to the real-world problem. [MediaPipe Holistic](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/holistic.md) pipeline processes every frame captured by a video camera and extracts hands' landmarks. Every new frame the script appends the landmarks to the previous ones until it reaches the length 30. Once 30 frames are processed and the corresponding landmarks are grouped together, the script converts the list with all the landmarks into an array and passes this array to the trained Neural Network so it can predict the sign of the user's hands. The prediction is then appended to the sentence list initialized earlier and the first word of the sentence is capitalized. Once the user has finished recording the sentence they can press "Enter" to perform a grammar check and correction using LLAMA3. If the user is not satisfied with the result they can press the "Spacebar" to reset the lists and start over.

## Conclusion

By combining advanced machine learning techniques and real-time action tracking, Sign-Language-Recognition empowers individuals to bridge the communication gap between sign language gestures and text, facilitating effective communication for the deaf and hearing-impaired.

## Prerequisites
* Python 3.6+

## Installation
1. Install requirement
   ```sh
   pip install -r requirements.txt
   ```
2. Update parameter:
   - Enter your API key in `grammar_correction.py` to acess to LLMs
   - Define and update your webcam index to cv2
   - Define list of action that want to train and recognite
4. Data collection:
   - Run `data_setup` to create data store folder
   - Run `data_collect.py` to start collect data from your webcam.
5. Training model:
   - Run `model.py` to start training model or load model using`.h5` file 
6. Recognition realtime
   - Run 'main.py` to start app.
     + Pess `space` to reset sentence
     + Press `enter` to grammar correction

