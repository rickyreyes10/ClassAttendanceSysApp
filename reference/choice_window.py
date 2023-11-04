import tkinter as tk
import util
from facial_recognition import FaceRecognitionApp
from qr_code_entry import QRCodeEntryApp

#Display a window for the user to select between Facial Recognition and QR Code attendance methods
def run_choice_window(root, frame, crn=None):
    root.geometry("1200x750")  # Set the geometry for the choice window

    # Destroy the previous frame if it exists
    if frame:
        frame.destroy()

    # Initialize and configure the main frame for choice window
    frame = tk.Frame(root, bg='black')  # Setting background color
    frame.pack(expand=True, fill="both")  # Expand and fill the available space

    ## Display the main label prompting user to select a choice
    label = util.get_text_label(frame, "Select which Class Attendance System you want to use", font_size=32,
                                justify="center", fg_color='white',
                                bg_color='black')
    label.pack(pady=20)

    #Start the facial recognition attendance system.
    def run_facial_recognition():
        frame.destroy()
        FaceRecognitionApp(root, crn)

    #Start the QR code based attendance system.
    def run_qr_code_entry():
        frame.destroy()
        QRCodeEntryApp(root, crn)

    # Create and pack the facial recognition choice button
    facial_recognition_button = util.get_button(frame, "Facial Recognition", color="#0066cc", command=run_facial_recognition, font_size=30, height=4, width=40)
    facial_recognition_button.pack(pady=10)

    # Create and pack the QR code choice button
    qr_code_button = util.get_button(frame, "QR Code", color="#009966", command=run_qr_code_entry, font_size=30, height=4, width=40)
    qr_code_button.pack(pady=10)
