# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 11:03:35 2019

"""

#IMPORTS
from imutils import face_utils
import imutils
import dlib
import cv2
import os
from sklearn.linear_model import LogisticRegression
import pickle
import shutil


param = [] 
result = []


#FONCTIONS
def face_detection(rects):
    """
    """
    for (i, rect) in enumerate(rects):
        #Recupere les points du visages et les stock dans une liste
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

        param.append(features)


# EYES
def dist_between_eyebrow(shape):
    den = abs(float(shape[17][0] - shape[1][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[23][0] - shape[22][0])) / den
    return dist

def dist_corner_eye_right(shape):
    den = abs(float(shape[16][1] - shape[23][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[43][1] - shape[23][1])) / den
    return dist


def dist_corner_eye_left(shape):
    den = abs(float(shape[2][1] - shape[22][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[40][1] - shape[22][1])) / den
    return dist


def dist_eyebrow_eye_right(shape):
    den = abs(float(shape[42][1] - shape[20][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[38][1] - shape[20][1])) / den
    return dist


def dist_eyebrow_eye_left(shape):
    den = abs(float(shape[47][1] - shape[25][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[45][1] - shape[25][1])) / den
    return dist


def dist_open_eye_right(shape):
    den = abs(float(shape[46][0] - shape[43][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[48][1] - shape[44][1])) / den
    return dist


def dist_open_eye_left(shape):
    den = abs(float(shape[40][0] - shape[37][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[41][1] - shape[39][1])) / den
    return dist


# NOSE
def dist_nose_width(shape):
    den = abs(float(shape[15][0] - shape[3][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[36][0] - shape[32][0])) / den
    return dist


def dist_nose_height(shape):
    den = abs(float(shape[7][1] - shape[28][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[32][1] - shape[28][1])) / den
    return dist


# MOUTH
def dist_mouth(shape):
    width = abs(shape[55][0] - shape[49][0])
    height = abs(shape[58][1] - shape[52][1])
    if height == 0:
        height = 0.1

    dist = float(width) / float(height)
    return dist


def dist_min_mouth(shape):
    width = abs(shape[55][0] - shape[49][0])
    height = abs(shape[67][1] - shape[63][1])
    if height == 0:
        height = 0.1

    dist = float(width) / float(height)
    return dist


def dist_mouth_width(shape):
    den = abs(float(shape[14][0] - shape[4][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[55][0] - shape[49][0])) / den
    return dist


def dist_mouth_cheeks_right(shape):
    den = abs(float(shape[14][0] - shape[4][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[14][0] - shape[55][0])) / den
    return dist


def dist_mouth_cheeks_left(shape):
    den = abs(float(shape[14][0] - shape[4][0]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[49][0] - shape[4][0])) / den
    return dist


def dist_mouth_corner(shape):
    den = abs(float(shape[9][1] - shape[52][1]))
    if den == 0:
        den = 0.1
    dist = abs(float(shape[55][1] - shape[52][1])) / den
    return dist


#MAIN
if __name__ == "__main__":

    # INIT DETECTOR DLIB : Visage et traits
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    
    
    #Parcours les images de différentes emotions
    for folder in os.listdir("learning_images"):
        for img in os.listdir("learning_images/" + folder):
            # Charge l'image, la redimensionne et la met en noir et blanc
            image = cv2.imread("learning_images/" + folder + "/" + img)
            image = imutils.resize(image, width=500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detection des visages
            rects = detector(gray, 1)
            face_detection(rects)
            result.append(folder)
    
    logreg = LogisticRegression(C=1e5, max_iter= 20000,solver='sag', multi_class='multinomial')
    logreg.fit(param, result)
    
    #Sauvegarder le model
    filename = "learning_save.sav"
    pickle.dump(logreg, open(filename, 'wb'))
    
    
    


