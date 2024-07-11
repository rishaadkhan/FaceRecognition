import cv2
import face_recognition
import pickle
import os
import firebase_admin
import numpy as np
from firebase_admin import credentials
from firebase_admin import storage

# Initialize Firebase app
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognition-4ad4f-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognition-4ad4f.appspot.com"  # Remove 'gs://' prefix
})

# Initialize Firebase storage bucket
bucket = storage.bucket()

# Function to resize and convert image to PNG
def resize_and_convert(img_path, target_size=(216, 216)):
    img = cv2.imread(img_path)
    if img is not None:
        # Resize image
        resized_img = cv2.resize(img, target_size)
        # Convert to PNG format
        _, img_encoded = cv2.imencode('.png', resized_img)
        return img_encoded.tobytes()
    else:
        print(f"Failed to read image {img_path}")
        return None

# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []

# Read images, resize, convert to PNG, and upload to Firebase Storage
for path in pathList:
    img_path = os.path.join(folderPath, path)
    img_data = resize_and_convert(img_path)
    if img_data:
        student_id = os.path.splitext(path)[0]
        imgList.append(img_data)
        studentIds.append(student_id)

        # Construct the file name and upload to Firebase Storage
        fileName = f'{folderPath}/{student_id}.png'  # Ensure the file extension is .png
        blob = bucket.blob(fileName)
        try:
            blob.upload_from_string(img_data, content_type='image/png')
            print(f"Uploaded {fileName} successfully.")
        except Exception as e:
            print(f"Failed to upload {fileName}: {e}")

print(studentIds)

# Function to find encodings
def findEncodings(imagesList):
    encodeList = []
    for img_data in imagesList:
        # Decode image data
        img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encode = encodings[0]
            encodeList.append(encode)
        else:
            print("No face found in image.")
    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Save encodings to a file
with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print("File Saved")
