# Sign-Language-Recognition

Dự án phát triển một mạng nơ-ron thần kinh sử dụng các lớp LSTM để nhận dạng và chuyển ngôn ngữ ký hiệu tiếng Việt thành ngôn ngữ tự nhiên. Dự án cho phép nhận dạng trên thời gian thực cũng như sửa ngữ pháp cho các câu được nhận dạng. Ngoài ra, mô hình cung cấp khả năng cho người dùng có thể tự huấn luyện trên bộ dữ liệu của riêng họ.

### Tính năng chính:
* Quy trình tự thu thập dữ liệu để tạo bộ dữ liệu ngôn ngữ ký hiệu tùy chỉnh, đa dạng.
* Sử dụng các lớp LSTM để cấu tạo mô hình.
* Nhận dạng thời gian thực dựa trên các mốc điểm hành động của tay, mặt, dáng người.
* Tích hợp mô hình ngôn ngữ lớn LLAMA3-70B để thực hiện sửa lỗi ngữ pháp, hoàn thiện câu.
* Tích hợp pipeline MediaPipe Holistic để theo dõi hành động và trích xuất các đặc trưng mốc điểm.

## Mô tả:

Toàn bộ dự án chia thành ba phần chính:
1. Thu thập dữ liệu.
2. Huấn luyện mô hình.
3. Nhận dạng thời gian thực.

## Thu thập dữ liệu

In order for a user to collect data and create their own dataset, the [data_collection.py] is used. The script is organized in a way that it would be easy to configure your own preferences and options, such as the signs the user would like to add to their dataset, the number of sequences for each sign, the number of frames for each sequence, and the path where the user would like to store the dataset. Once these parameters were set and the script is running, the user can start recording the data. <ins>It is recommended that the user records a substantial number of sequences changing the position of their hands. This way the user can ensure data diversity which helps to obtain a generalized model.</ins>

[MediaPipe Holistic](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/holistic.md) pipeline was used to record the data from the user's actions. Using [MediaPipe Holistic](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/holistic.md) instead of [MediaPipe Hands](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/hands.md) opens doors to future extensions and possibilities of this script. The pipeline processes each frame sent through it and results in the pose, face, left hand, and right hand components neatly stored in a variable. Each of the components can be represented by landmarks (these components' coordinates). It resulting in overall 126 data entries (21 landmarks per hand with _x_, _y_, _z_ coordinates per landmark).

## Model Training

After the data has been collected and the dataset is complete, the user can proceed with the model training. In this step, the dataset is split into two subsets: 90% of the dataset is used for training and 10% for testing. The accuracy of testing using this 10% of the dataset will provide insight into the efficiency of the model.

For this particular project, the Neural Network is built using a Sequential model instance by passing three LSTM and two Densely-connected layers. The first four of these layers use the ReLU activation function with the last layer using the Softmax activation function. In the process of training, the Adam optimization algorithm is used to obtain optimal parameters for each layer.

Once the Neural Network is compiled, one can proceed with the model training and testing. During this step, the user can provide the model with the training subset, associated labels, and the number of epochs. Depending on the size of the provided subset and the number of epochs the training process can take up to a few minutes. Following the training, one can assess the model by performing predictions using the testing subset and evaluating the accuracy of these predictions.

## Real Time Predictions

In this step, the Neural Network is ready to apply everything it has learned to the real-world problem. [MediaPipe Holistic](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/holistic.md) pipeline processes every frame captured by a video camera and extracts hands' landmarks. Every new frame the script appends the landmarks to the previous ones until it reaches the length 30. Once 30 frames are processed and the corresponding landmarks are grouped together, the script converts the list with all the landmarks into an array and passes this array to the trained Neural Network so it can predict the sign of the user's hands. The prediction is then appended to the sentence list initialized earlier and the first word of the sentence is capitalized. Once the user has finished recording the sentence they can press "Enter" to perform a grammar check and correction using the llms. If the user is not satisfied with the result they can press the "Spacebar" to reset the lists and start over.

## Kết luận

Bằng cách kết hợp các kỹ thuật học máy, học sâu tiên tiến và theo dõi hành động thời gian thực, dự án giúp mọi người thu hẹp khoảng cách giao tiếp giữa ngôn ngữ ký hiệu và văn bản (ngôn ngữ tự nhiên), tạo điều kiện giao tiếp hiệu quả cho người khiếm thính.

## Yêu cầu:
* Python 3.6+
