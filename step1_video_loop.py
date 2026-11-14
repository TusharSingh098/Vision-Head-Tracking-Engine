import cv2

# Step 2: Video -> while (frame)

# 0 is usually the default webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    # If the frame was not grabbed successfully, break the loop
    if not ret:
        print("Failed to grab frame")
        break

    mirrored_frame = cv2.flip(frame, 3)
        
    # Show the video frame
    cv2.imshow('Video', mirrored_frame)
    
    # Exit if the 'q' key is pressed
    # waitKey(1) waits for 1 millisecond for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resource and close windows
cap.release()
cv2.destroyAllWindows()
