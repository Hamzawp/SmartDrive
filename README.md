# SmartDrive

<br/>
<p align="center">
  <img src="./assets/logo.png" width="20%" alt="logo"/>
</p>

<p align="center">
  <a href="#table-of-contents"><b>Explore the docs »</b></a>
  <br />
  <br />
  <a href="#architecture-and-design">Architecture</a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#demonstration">Features</a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="#contributing">Local Setup</a>
  <br />
</p>

## Table Of Contents

- [About the Project](#about-the-project)
- [Architecture](#architecture)
- [Demonstration & Features](#demonstration)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [Authors](#authors)

## About The Project

**Problem Statement**

Despite automotive technology advancements, global concern persists regarding driver safety due to increasing vehicle numbers, heightening accident risks. Our project aims to tackle this by:

1. Calculating safe driving areas through analysis of roadway conditions.
2. Developing precise lane boundary detection to prevent lane departures.
3. Integrating safety features like Drowsiness, Seat Belt, and Smoking, Drinking and Occupancy Detection to monitor and mitigate driver risks.
4. Providing solution at a sustainable cost for all the drivers.

Through these initiatives, we aim to substantially reduce road accidents and enhance overall road safety.

<br />

**Features**

1. Prioritizing measures and practices aimed for reducing risks and ensuring the well-being of drivers on the road. Enhancing safety through real-time insights and alerts for specific vehicle types.
2. The project scope explicitly excludes integration of autonomous technology, emphasizing a focus solely on conventional driver-operated systems.
3. The algorithmic solutions for this project are specifically tailored to address safe area calculation, lane detection, and driver behavior monitoring. Safe area calculation algorithms are designed to identify and analyze potential hazards within the driving environment.
4. Aiming to promote responsible habits without involving hardware components in all vehicle types.

## Demonstration

**Back Cam**
<img src="./assets/Demo1.png" alt="demo">
<br />
**Front Cam**
<img src="./assets/Demo2.jpg" alt="demo">
<br />

## Architecture

The architecture:

<img src="./assets/block_diagram1.png" alt="architecture">
<br />
<img src="./assets/block_diagram2.png" alt="architecture">
<br />
<img src="./assets/block_diagram3.png" alt="architecture">
<br />

## Algorithm

1. Initialize and Load Models:

- Import required libraries and load pre-trained models for object detection, smoking, and drinking detection.
- Load face and eye cascades for drowsiness detection.

2. Video Capture and Frame Processing:

- Capture video frames from the input video.
- Resize frames and limit the region of interest.

3. Face and Seatbelt Detection:

- Detect faces and draw rectangles around them.
- Use a pre-trained model to detect seatbelt usage and log the results.

4. Smoking and Drinking Detection:

- Apply smoking and drinking detection models on the frames.
- Draw bounding boxes and labels for detected objects.

5. Drowsiness Detection:

- Detect eyes within the face regions.
- Log and label the frames if no eyes are detected (indicating drowsiness).

6. Display Results:

- Draw a dashboard on the frames to display the status of smoking, drinking, seatbelt usage, drowsiness, and face count.
- Show the video feed with the drawn information.

6. Log and Post-Processing:

- Log activities such as face count, smoking, drinking, seatbelt usage, and drowsiness.
- Read the log file and generate a report summarizing the detections and their counts.

7. Clean Up:

- Release video capture and close all OpenCV windows after processing.

<br />
<br />

### Technologies Used

- Computer Vision
- YOLO

<br />

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**

```sh
   git clone https://github.com/your_username/SmartDrive.git
   cd SmartDrive
```

2. **Install the required packages**

```sh
 pip install -r requirements.txt
```

3. **Install specific versions of the required libraries**

```sh
 pip install cv2==4.8.0
 pip install numpy
 pip install torch
 pip install opencv-python
 pip install opencv-contrib-python
 pip install ultralytics
 pip install cvzone
```

4. **Run the application**

```sh
 python App.py
```

## Contributing

**Local Setup || Project Structure**

NOTE: Individual instructions can be found in respective directories.

```
*
├───Module 1 - BackCam
├───Module 2.1 - FrontCam
├───Module 2.2 - FrontCam
├───Module 2.3 - FrontCam
├───Module 2.4 - FrontCam
├───Module 2.5 - FrontCam
├───Safe-lane-detection
└───App.py
```

- `Module 1 - BackCam`: Safe lane detection.
- `Module 2.1 - FrontCam`: Drinking detection.
- `Module 2.2 - FrontCam`: Drowsiness detection.
- `Module 2.3 - FrontCam`: Smoking detection.
- `Module 2.4 - FrontCam`: Seatbelt detection.
- `Module 2.5 - FrontCam`: Occupancy detection.

<br />
<br />



## Authors

- Hamza Sayyed
  - [LinkedIn](https://shorturl.at/hjAEI)
- Om Shete
  - [LinkedIn](https://www.linkedin.com/in/om-shete-25748522a/)
- Mohib Abbas Sayed
  - [LinkedIn](https://www.linkedin.com/in/mohib-abbas-sayed-83837422a/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

## License 📜

[GPU License](https://github.com/Hamzawp/SmartDrive/blob/master/LICENSE)