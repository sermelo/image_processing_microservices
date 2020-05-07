import cv2
import imutils

def preprocess_image(image):
    new_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(new_image, (21, 21), 0)

def diff(org_image1, org_image2):
    min_area = 500
    image1 = preprocess_image(org_image1)
    image2 = preprocess_image(org_image2)
    boxes_image = image2.copy()
    imageDelta = cv2.absdiff(image1, image2)
    thresh = cv2.threshold(imageDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    boxes = []
    for c in cnts:
          # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_area:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        boxes.append((x, y, w, h))
        cv2.rectangle(boxes_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    retval, buffer = cv2.imencode('.jpg', boxes_image)
    return buffer, boxes
    # draw the text and timestamp on the frame
#    cv2.putText(org_image2, "Room Status: {}".format(text), (10, 20),
#                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#    cv2.putText(org_image2, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
#                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

