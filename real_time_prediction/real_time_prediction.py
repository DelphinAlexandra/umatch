from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time
import dlib
import cv2
import pickle

# EYES
def dist_between_eyebrow(shape):
    den = abs(float(shape[16][0] - shape[0][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[22][0] - shape[21][0])) / den
    return dist

def dist_corner_eye_right(shape):
    den = abs(float(shape[15][1] - shape[22][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[42][1] - shape[22][1])) / den
    return dist


def dist_corner_eye_left(shape):
    den = abs(float(shape[1][1] - shape[21][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[39][1] - shape[21][1])) / den
    return dist


def dist_eyebrow_eye_right(shape):
    den = abs(float(shape[41][1] - shape[19][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[37][1] - shape[19][1])) / den
    return dist


def dist_eyebrow_eye_left(shape):
    den = abs(float(shape[46][1] - shape[24][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[44][1] - shape[24][1])) / den
    return dist


def dist_open_eye_right(shape):
    den = abs(float(shape[45][0] - shape[42][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[47][1] - shape[43][1])) / den
    return dist


def dist_open_eye_left(shape):
    den = abs(float(shape[39][0] - shape[36][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[40][1] - shape[38][1])) / den
    return dist


# NOSE
def dist_nose_width(shape):
    den = abs(float(shape[14][0] - shape[2][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[35][0] - shape[31][0])) / den
    return dist


def dist_nose_height(shape):
    den = abs(float(shape[6][1] - shape[27][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[31][1] - shape[27][1])) / den
    return dist


# MOUTH
def dist_mouth(shape):
    width = abs(shape[54][0] - shape[48][0])
    height = abs(shape[57][1] - shape[51][1])
    if height == 0:
        height = 0.1

    dist = float(width) / float(height)
    return dist


def dist_min_mouth(shape):
    width = abs(shape[54][0] - shape[48][0])
    height = abs(shape[66][1] - shape[62][1])
    if height == 0:
        height = 0.1

    dist = float(width) / float(height)
    return dist


def dist_mouth_width(shape):
    den = abs(float(shape[13][0] - shape[3][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[54][0] - shape[48][0])) / den
    return dist


def dist_mouth_cheeks_right(shape):
    den = abs(float(shape[13][0] - shape[3][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[13][0] - shape[54][0])) / den
    return dist


def dist_mouth_cheeks_left(shape):
    den = abs(float(shape[13][0] - shape[3][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[48][0] - shape[3][0])) / den
    return dist


def dist_mouth_corner(shape):
    den = abs(float(shape[8][1] - shape[51][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[54][1] - shape[51][1])) / den
    return dist


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
loadmod = pickle.load(open("learning_save.sav", 'rb'))

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(0).start()
time.sleep(2.0)

start = time.time()
# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream, resize it to
    # have a maximum width of 400 pixels, and convert it to
    # grayscale
    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    end = time.time()

    if(end - start > 2) :
        start = time.time()
        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            features = []
            features.append(dist_between_eyebrow(shape))
            features.append(dist_corner_eye_right(shape))
            features.append(dist_corner_eye_left(shape))
            features.append(dist_eyebrow_eye_right(shape))
            features.append(dist_eyebrow_eye_left(shape))
            features.append(dist_open_eye_right(shape))
            features.append(dist_open_eye_left(shape))
            features.append(dist_nose_width(shape))
            features.append(dist_nose_height(shape))
            features.append(dist_mouth(shape))
            features.append(dist_min_mouth(shape))
            features.append(dist_mouth_width(shape))
            features.append(dist_mouth_cheeks_right(shape))
            features.append(dist_mouth_cheeks_left(shape))
            features.append(dist_mouth_corner(shape))

            # Prediction
            emotion = loadmod.predict([features])
            print(emotion)

    # show the frame
    end = time.time()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()