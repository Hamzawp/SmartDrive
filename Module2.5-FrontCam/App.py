import cv2

INPUT_VIDEO = "testvideo1.mp4"
cascPath = "./File.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(INPUT_VIDEO)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if not ret:
        break  # Break the loop if there is no frame

    # Resize the frame to a smaller size
    frame = cv2.resize(frame, (1000, 600))

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    # Count the number of faces
    face_count = len(faces)

    # Draw a rectangle around the faces and display the count on the video
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the face count on the video frame
    cv2.putText(
        frame,
        f"Faces: {face_count}",
        (10, 30),  # Position for the text
        cv2.FONT_HERSHEY_SIMPLEX,
        1,  # Font scale
        (255, 255, 255),  # White color for the text
        2,  # Thickness of the text
    )

    # Display the resulting frame
    cv2.imshow("Video", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# When everything is done, release the video capture and destroy all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
