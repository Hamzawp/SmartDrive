import cv2
import numpy as np
import imutils

# Slope of line
def Slope(a, b, c, d):
    return (d - b) / (c - a)

# Video file path
video_path = 'C:\\Users\\mohib\\Desktop\\MPR-VI\\Finding-seatbelt\\testvideo.mp4'

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video file is opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Loop to process each frame in the video
while True:
    # Read a frame from the video
    ret, beltframe = cap.read()

    # Break the loop if the video ends
    if not ret:
        break

    # Resizing The Image
    beltframe = imutils.resize(beltframe, height=800)

    # Converting To GrayScale
    beltgray = cv2.cvtColor(beltframe, cv2.COLOR_BGR2GRAY)

    # No Belt Detected Yet
    belt = False

    # Blurring The Image For Smoothness
    blur = cv2.blur(beltgray, (1, 1))

    # Converting Image To Edges
    edges = cv2.Canny(blur, 50, 400)

    # Previous Line Slope
    ps = 0

    # Previous Line Coordinates
    px1, py1, px2, py2 = 0, 0, 0, 0

    # Extracting Lines
    lines = cv2.HoughLinesP(edges, 1, np.pi / 270, 30, maxLineGap=20, minLineLength=170)

    # If "lines" Is Not Empty
    if lines is not None:

        # Loop line by line
        for line in lines:

            # Coordinates Of Current Line
            x1, y1, x2, y2 = line[0]

            # Slope Of Current Line
            s = Slope(x1, y1, x2, y2)

            # If Current Line's Slope Is Greater Than 0.7 And Less Than 2
            if (0.7 < abs(s) < 2):

                # And Previous Line's Slope Is Within 0.7 To 2
                if 0.7 < abs(ps) < 2:

                    # And Both The Lines Are Not Too Far From Each Other
                    if ((abs(x1 - px1) > 5) and (abs(x2 - px2) > 5)) or ((abs(y1 - py1) > 5) and (abs(y2 - py2) > 5)):

                        # Plot The Lines On "beltframe"
                        cv2.line(beltframe, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        cv2.line(beltframe, (px1, py1), (px2, py2), (0, 0, 255), 3)

                        # Belt Is Detected
                        print("Belt Detected")
                        belt = True

            # Otherwise, Current Slope Becomes Previous Slope (ps),
            # And Current Line Becomes Previous Line (px1, py1, px2, py2)
            ps = s
            px1, py1, px2, py2 = line[0]

    if not belt:
        print("No Seatbelt detected")

    # Show The "beltframe"
    cv2.imshow("Seat Belt", beltframe)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
