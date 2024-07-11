import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognition-4ad4f-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "PAT004":
        {
            "name": "rishaad",
            "major": "khan",
            "last_attendance_time": "2022-12-11 00:54:34"

        },
    "PAT005":
        {
            "name": "abqari",
            "major": "abbas",
            "last_attendance_time": "2022-12-11 00:54:34"

        },
    "PAT004":
        {
            "name": "rishaad",
            "major": "khan",
            "last_attendance_time": "2022-12-11 00:54:34"

        },
    "PAT006":
        {
            "name": "suraj",
            "major": "kumar",
            "last_attendance_time": "2022-12-11 00:54:34"

        },
    "PAT007":
        {
            "name": "prashant",
            "major": "pal",

            "last_attendance_time": "2022-12-11 00:54:34"

        },
    "PAT008":
        {
            "name": "ashish",
            "major": "kumar",

            "last_attendance_time": "2022-12-11 00:54:34"

        },

}

for key, value in data.items():
    ref.child(key).set(value)