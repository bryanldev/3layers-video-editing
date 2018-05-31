import numpy as np
import cv2

# Change 'input.avi' to your video input.
vin = cv2.VideoCapture('input.avi')

# Check if camera opened successfully
if vin.isOpened() is False:
    print("Error opening video stream or file")


# Get the width/height
width = int(vin.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vin.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
vout = cv2.VideoWriter('output.avi',
                       fourcc, 25, (width, height), True)


while(vin.isOpened()):

    ret, frame = vin.read()
    if ret is True:

        ###############################################################
        # Mask: gray color.                                           #
        # Copy the middle panel from the video and convert it to gray #
        ###############################################################

        mask = frame[0:0 + width, int(width / 3):int(width / 3) + int(width/3)]
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        locs = np.where(mask != 0)  # Get the non-zero mask locations
        frame[0:0 + width, int(width / 3):int(width / 3) +
              int(width / 3)] = mask[:, :, None]

        ###############################################################
        # Canny Edge Detector to the right panel                      #
        # Copy the right panel from the video and apply the detector  #
        ###############################################################

        edges = frame[0:0+width, int(width*(2 / 3)):int(width*(2 / 3)) +
                      int(width / 3)]
        edges = cv2.Canny(edges, 100, 300)

        locs = np.where(edges != 0)
        frame[0:0 + width, int(width * (2 / 3)):int(width *
              (2 / 3)) + int(width / 3)] = edges[:, :, None]

        vout.write(frame)
        cv2.imshow('Modified Video', frame)
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

vin.release()
vout.release()
cv2.destroyAllWindows()
