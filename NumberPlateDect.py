import numpy as np
import cv2
import pytesseract
import pywhatkit
from openpyxl import load_workbook

# Set path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Load the Excel database
wb3 = load_workbook('C:\\Users\\Lenovo\\OneDrive\\Desktop\\BBB\\NO-PARKING-ZONE-MONITORING-MODLE-main\\vehicle_details.xlsx')
ws3 = wb3.active

# Select the correct camera index (update this with the index of your external camera)
camera_index = 1  # Change this to the index of your external camera

# Initialize the camera capture
cap = cv2.VideoCapture(camera_index)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform edge detection
    edged = cv2.Canny(gray, 170, 200)

    # Find contours in the edged image
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCnt = None

    # Loop over the contours
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            NumberPlateCnt = approx

            # Mask the number plate region
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
            new_image = cv2.bitwise_and(frame, frame, mask=mask)

            # Perform OCR on the masked region
            config = ('-l eng --oem 1 --psm 7')
            text = pytesseract.image_to_string(new_image, config=config)

            # Check if the detected number plate exists in the database
            for row in range(2, 12):
                plate_number = str(ws3['A' + str(row)].value).strip()
                if plate_number and plate_number in text:
                    contact_number = '+91' + str(ws3['C' + str(row)].value)

                    # Send WhatsApp message
                    pywhatkit.sendwhatmsg_instantly(contact_number, 'Your car is parked in a No-Parking Zone. INR 500 has been debited from your account.')
                    print("Message sent to", contact_number)

                    # Break out of the loop to avoid sending multiple messages for the same plate
                    break

    # Display the frame
    cv2.imshow('Frame', frame)

    # Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
