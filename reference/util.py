import tkinter as tk
from tkinter import messagebox, dialog
import pickle
import os
import face_recognition
from db_utils import connect


# Creates and returns a tkinter button with specified properties.
def get_button(window, text, color, command, fg='white', font_size=20, height=2, width=20):
    """
    Creates a button with specified properties.

    Parameters:
        window: tk.Tk or tk.Toplevel
            The tkinter window where the button will be placed.
        text: str
            Text to display on the button.
        color: str
            Background color of the button.
        command: function
            The function to be executed when the button is clicked.
        fg: str, optional
            Foreground color of the button. Default is 'white'.
        font_size: int, optional
            Font size of the text. Default is 20.
        height: int, optional
            Height of the button. Default is 2.
        width: int, optional
            Width of the button. Default is 20.

    Returns:
        tk.Button: A tkinter Button object.
    """
    button = tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=height,
        width=width,
        font=(f'Helvetica bold', font_size)
    )
    return button


# Display a custom modal dialog box with a specified title, message, and button text.
def custom_dialog(title, message, button_text):
    def on_button_click():
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title(title)
    tk.Label(dialog, text=message).pack(padx=20, pady=20)
    tk.Button(dialog, text=button_text, command=on_button_click).pack(pady=10)
    dialog.grab_set()  # make it modal


# Create and return a tkinter label for displaying images.
def get_img_label(root, bg=None):
    label = tk.Label(root)
    if bg:
        label.configure(bg=bg)
    return label


# Create and return a text label with specified properties.
def get_text_label(window, text, font_size=21, justify="left", fg_color='white', bg_color='black'):
    label = tk.Label(window, text=text, fg=fg_color, bg=bg_color)
    label.config(font=("sans-serif", font_size), justify=justify)
    return label


# Create and return a tkinter text entry widget with specified properties.
def get_entry_text(window, height=2, width=15, font_size=32):
    txt_input = tk.Text(window, height=height, width=width, font=("Arial", font_size))
    return txt_input


# Display an informational message box with a specified title and description.
def msg_box(title, description):
    messagebox.showinfo(title, description)


# Save the face encoding for a specific CRN (Course Registration Number) to disk.
def save_face_encoding(crn, student_name, encoding):
    # Save face encoding to database.
    # Connect to the database
    connection = connect()
    cursor = connection.cursor()

    # Convert encoding to binary format for storage
    binary_encoding = pickle.dumps(encoding)

    # Save the encoding to the Students table
    query = """INSERT INTO Students(student_name, facial_encoding_file, crn) 
               VALUES (%s, %s, (SELECT crn FROM Classes WHERE crn=%s))"""
    cursor.execute(query, (student_name, binary_encoding, crn))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()


def get_face_encoding_from_db(crn, student_name):
    """Retrieve face encoding from database."""
    # Connect to the database
    connection = connect()
    cursor = connection.cursor()

    # Get the encoding from the Students table based on CRN and student_name
    query = """SELECT facial_encoding_file 
               FROM Students 
               WHERE student_name=%s AND crn=(SELECT crn FROM Classes WHERE crn=%s)"""
    cursor.execute(query, (student_name, crn))

    # Fetch the result
    result = cursor.fetchone()

    # Close the connection
    cursor.close()
    connection.close()

    if result:
        # Unpickle the encoding
        encoding = pickle.loads(result[0])
        return encoding
    else:
        return None


# Attempt to recognize a face in an image based on known encodings for a given CRN.
def recognize(face_image, crn):
    """Attempt to recognize a face in an image based on known encodings for a given CRN."""
    face_locations = face_recognition.face_locations(face_image)
    if len(face_locations) == 0:
        return 'no_persons_found'

    face_encodings = face_recognition.face_encodings(face_image, face_locations)

    for face_encoding in face_encodings:
        # Instead of listing through files, iterate over database records
        connection = connect()
        cursor = connection.cursor()
        query = """SELECT student_name, facial_encoding_file 
                   FROM Students 
                   WHERE crn=(SELECT crn FROM Classes WHERE crn=%s)"""
        cursor.execute(query, (crn,))

        for student_name, known_face_encoding_binary in cursor.fetchall():
            known_face_encoding = pickle.loads(known_face_encoding_binary)
            matches = face_recognition.compare_faces([known_face_encoding], face_encoding)

            if True in matches:
                return student_name

    return 'unknown_person'


# Retrieve the closest matching filename for a given face encoding and CRN
def get_closest_match(face_encoding, crn):
    connection = connect()
    cursor = connection.cursor()
    query = """SELECT student_name, facial_encoding_file 
               FROM Students 
               WHERE crn=(SELECT crn FROM Classes WHERE crn=%s)"""
    cursor.execute(query, (crn,))

    closest_match = None
    closest_distance = float('inf')  # Initialize with infinity

    for student_name, known_face_encoding_binary in cursor.fetchall():
        known_face_encoding = pickle.loads(known_face_encoding_binary)
        distance = face_recognition.face_distance([known_face_encoding], face_encoding)[0]

        if distance < closest_distance:
            closest_distance = distance
            closest_match = student_name

    cursor.close()
    connection.close()
    return closest_match


# Attempt to recognize a face from its encoding based on known encodings for a given CRN.
def recognize_from_encoding(face_encoding, crn):
    connection = connect()
    cursor = connection.cursor()
    query = """SELECT student_name, facial_encoding_file 
               FROM Students 
               WHERE crn=(SELECT crn FROM Classes WHERE crn=%s)"""
    cursor.execute(query, (crn,))

    closest_match = None
    closest_distance = 0.6  # You can adjust the threshold

    for student_name, known_face_encoding_binary in cursor.fetchall():
        known_face_encoding = pickle.loads(known_face_encoding_binary)
        distance = face_recognition.face_distance([known_face_encoding], face_encoding)[0]

        if distance < closest_distance:
            closest_distance = distance
            closest_match = student_name

    cursor.close()
    connection.close()

    return closest_match or 'unknown_person'


