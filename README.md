# Volume-control-using-hand-gesture-using-python-and-openCv
The script can control volume of device with help of camera using the tips our thumb and index finger using Python , Mediapipe

### WORKING PRINCIPLE
The camera in our device is used for this project. It detects our hand with points in it so as it can see the distance between our thumb finger tip and index finger tip. The distance between the points 4 and 8 is directly proportional to the volume of device.

### APPROACH
Detect hand landmarks
Calculate the distance between thumb tip and index finger tip.
Map the distance of thumb tip and index finger tip with volume range. For my case, distance between thumb tip and index finger tip was within the range of 30 – 350 and the volume range was from -63.5 – 0.0.
In order to exit press ‘q'
