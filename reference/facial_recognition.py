import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import util
from datetime import datetime
import numpy as np
import pickle
from db_utils import connect


class FaceRecognitionApp:
    def __init__(self, root, crn):

        # Initialize the facial recognition app with its GUI and settings
        self.root = root
        self.crn = crn

        # Basic window settings and configurations
        self.root.title("Class Attendance System")
        self.root.geometry("1200x750")
        self.root.configure(bg='black')
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)

        # Initialization of required variables
        self.frame_buffer = []
        self.buffer_size = 10  # the number of frames to keep in the buffer for averaging

        self.frame_skip = 2  # process one frame for every 2 captured
        self.frame_count = 0

        # state variables for face recognition
        self.face_detected = False
        self.face_recognized = False
        self.attendance_marked = False

        # Initialize GUI elements
        # Initialize your buttons, labels, etc. here
        self.initialize_ui()
        self.start_webcam()

    # Setup the UI components like buttons, labels, etc.
    def initialize_ui(self):
        # Create and place your buttons, labels, etc. here
        # Use util.get_button, util.get_img_label, etc.
        self.webcam_label = util.get_img_label(self.root)
        self.webcam_label.config(width=640, height=400)
        self.webcam_label.pack(pady=10)

        self.login_button = util.get_button(self.root, 'Login', 'green', self.login)
        self.login_button.pack(pady=10)

        self.register_button = util.get_button(self.root, 'Register', 'gray', self.register)
        self.register_button.pack(pady=10)

        self.exit_button = util.get_button(self.root, 'Exit', 'red', self.destroy)
        self.exit_button.pack(pady=10)

    # Reset the state for the next recognition attempt
    def reset_for_next_recognition(self):
        self.frame_buffer = []
        self.face_detected = False
        self.face_recognized = False
        self.attendance_marked = False

    # Add the new frame to the buffer and remove the oldest frame if the buffer is full
    def update_buffer(self, new_frame):
        if len(self.frame_buffer) >= self.buffer_size:
            self.frame_buffer.pop(0)
        self.frame_buffer.append(new_frame)

    # Calculate the average face encoding over the buffered frames
    def get_average_face_encoding(self):
        if len(self.frame_buffer) == 0:
            return None

        average_encoding = None
        for frame in self.frame_buffer:
            face_encodings = face_recognition.face_encodings(frame)
            if len(face_encodings) > 0:
                if average_encoding is None:
                    average_encoding = face_encodings[0]
                else:
                    average_encoding = np.add(average_encoding, face_encodings[0])

        if average_encoding is not None:
            average_encoding = np.divide(average_encoding, len(self.frame_buffer))

        return average_encoding

    # Initialize and start the webcam capture
    def start_webcam(self):
        try:
            self.cap = cv2.VideoCapture(0)  # Starting the default webcam
            if not self.cap.isOpened():
                raise ValueError("Could not open video device")
            self.process_webcam()
        except Exception as e:
            util.msg_box('Error', f'An error occurred while starting the webcam: {e}')
            self.cap = None

    # Process the webcam feed and update the UI with the captured frames
    def process_webcam(self):
        ret, frame = self.cap.read()

        if not ret:
            util.msg_box('Error', 'Could not read frame from webcam.')
            return

        self.frame_count += 1

        if self.frame_count % self.frame_skip == 0:
            self.most_recent_capture = frame
            self.update_buffer(self.most_recent_capture)
            img_rgb = cv2.cvtColor(self.most_recent_capture, cv2.COLOR_BGR2RGB)
            img_rgb = cv2.resize(img_rgb, (640, 480))

            self.most_recent_capture_pil = Image.fromarray(img_rgb)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

            self.webcam_label.imgtk = imgtk
            self.webcam_label.configure(image=imgtk)

        self.webcam_label.after(10, self.process_webcam)

    # Stop and release the webcam
    def stop_webcam(self):
        # Stop webcam if running
        self.cap.release()

    # Attempt to recognize and login a user using the current frame
    def login(self):
        if self.cap is None or not self.cap.isOpened():
            util.msg_box('Error', 'Webcam not available.')
            return

        average_encoding = self.get_average_face_encoding()
        if average_encoding is not None:
            name = util.recognize_from_encoding(average_encoding, self.crn)
        else:
            name = 'no_persons_found'  # Fallback if average encoding couldn't be calculated

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Oops...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Welcome back!', f'Welcome, {name}.')
            self.log_event(name, 'Present')
            self.reset_for_next_recognition()

    # Recognize and log out the user using the current frame
    def logout(self):
        if self.cap is None or not self.cap.isOpened():
            util.msg_box('Error', 'Webcam not available.')
            return

        # Your logout logic here
        name = util.recognize(self.most_recent_capture)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('ops...', 'Unknown user. Please register new user or try again.')
        else:
            self.root.after(250, self.root.quit)  # Close the Tkinter window after 3000 milliseconds

        if name not in ['unknown_person', 'no_persons_found']:
            self.log_event(name, 'exited app')
            self.reset_for_next_recognition()

    # Log an event (e.g., login, logout) for a specific user
    def log_event(self, username, action):
        """Log an event (e.g., login, logout) for a specific user using the database."""

        conn = None
        try:
            # Establish a database connection using the 'connect' function from db_util.py
            conn = connect()
            cursor = conn.cursor()

            # Fetch the student_id using the given username
            student_query = "SELECT student_id, email, crn FROM Students WHERE student_name = %s"
            cursor.execute(student_query, (username,))
            result = cursor.fetchone()

            if not result:
                raise Exception("User not found in database")

            student_id, student_email, student_crn = result      #un pack the result tuple

            # Record attendance
            cursor.execute("""
                INSERT INTO Attendance_Log (student_email, class_crn, attendance_date, attendance_time, method) 
                VALUES (
                    %s, 
                    %s,
                    CURDATE(),
                    CURTIME(),
                    'Facial Recognition'
                )
            """, (student_email, self.crn))
            conn.commit()

        except Exception as e:
            print(f"error: {e}")
        finally:
            if conn and conn.is_connected():
                conn.close()

    # Open the registration window
    def register(self):
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Register")

        username_label = util.get_text_label(self.register_window, "Username:", font_size=16)
        username_label.pack()

        self.username_entry = util.get_entry_text(self.register_window, height=1, width=30, font_size=16)
        self.username_entry.pack()

        email_label = util.get_text_label(self.register_window, "Email:", font_size=16)
        email_label.pack()

        self.email_entry = util.get_entry_text(self.register_window, height=1, width=30, font_size=16)
        self.email_entry.pack()

        submit_button = util.get_button(self.register_window, 'Submit', 'green', self.submit_registration)
        submit_button.pack()

        self.register_window.grab_set()

    # Process and submit a new registration
    def submit_registration(self):
        # Your registration logic here
        username = self.username_entry.get("1.0", 'end-1c').strip()
        email = self.email_entry.get("1.0", 'end-1c').strip()

        if not email or not username:
            util.msg_box("Error", "Username and Email cannot be empty")
            return

        conn = None
        try:
            conn = connect()
            cursor = conn.cursor()

            # Check if a student with the given email already exists
            check_query = "SELECT facial_encoding_file FROM Students WHERE email = %s AND crn = %s"
            cursor.execute(check_query, (email, self.crn))
            face_result = cursor.fetchone()

            # check if a user with the given username and CRN already exists
            if face_result and face_result[0]:
                util.msg_box("Error", f"Username {username} already exists.")
                return

            embeddings = face_recognition.face_encodings(self.most_recent_capture)

            if len(embeddings) == 0:
                util.msg_box("Error", "No face found. Try again.")
                return

            closest_match = util.get_closest_match(embeddings[0], self.crn)

            if closest_match:
                util.msg_box("Error", f"You are already registered as {closest_match}. Please log in.")
                return
            serialized_embedding = pickle.dumps(embeddings[0])  # Serialize the embeddings

            # If user is already in the database, update their record to add the facial encoding
            if face_result:
                update_query = """
                UPDATE Students 
                SET facial_encoding_file = %s 
                WHERE email = %s
                """
                cursor.execute(update_query, (serialized_embedding, email))
            else:
                # If not, create a new record for the user with their facial encoding and other details
                insert_query = """
                INSERT INTO Students (student_name, email, crn, facial_encoding_file) 
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (username, email, self.crn, serialized_embedding))
            conn.commit()

            util.msg_box("Success", f"{username} was successfully registered for the facial recognition system.")

            self.register_window.destroy()
        except Exception as e:
            util.msg_box("Error", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()

    # Handle the window close event
    def destroy(self):
        self.stop_webcam()
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.root.quit()


# Start the facial recognition window
def run_facial_recognition_window(crn):
    root = tk.Tk()
    app = FaceRecognitionApp(root, crn)
    root.mainloop()