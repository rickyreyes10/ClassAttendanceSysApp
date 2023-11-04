import io
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
import qrcode
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import util
from datetime import datetime
import json
from db_utils import connect
from io import BytesIO
import PIL.Image


class QRCodeEntryApp:
    def __init__(self, root, crn):
        self.root = root
        self.crn = crn

        # Window settings
        self.root.title("QR Code Entry System")
        self.root.geometry("1200x750")
        self.root.configure(bg='black')
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)

        # Initialize UI elements and webcam
        self.initialize_ui()
        self.start_webcam()

    # Create and set up the webcam display label
    def initialize_ui(self):
        self.webcam_label = util.get_img_label(self.root)
        self.webcam_label.config(width=640, height=400)
        self.webcam_label.pack(pady=10)

        # Create and set up the 'Register' button
        self.register_button = util.get_button(self.root, 'Register', 'gray', self.register)
        self.register_button.pack(pady=10)

        # Create and set up the 'Retrieve QR' button
        self.retrieve_button = util.get_button(self.root, 'Retrieve QR', 'blue', self.retrieve_qr_code)
        self.retrieve_button.pack(pady=10)

        # Create and set up the 'Exit' button
        self.exit_button = util.get_button(self.root, "Exit", 'red', self.destroy)
        self.exit_button.pack(pady=10)

    # Initialize webcam
    def start_webcam(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showinfo('Error', 'Could not open video device')
            return
        self.process_webcam()

    # Capture and process frames from the webcam
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture = frame
        qr_info = decode(frame)

        detected = False  # initialize the detected flag

        if not ret:
            return

        conn = None
        try:
            conn = connect()
            cursor = conn.cursor()

            # Check if a QR code is detected in the frame
            for qr in qr_info:
                data = qr.data.decode('utf-8')

                try:
                    cleaned_data = data.replace("'", '"')
                    self.data = json.loads(cleaned_data)  # parse the cleaned JSON string into a dictionary
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    print(f"Received data: {data}")
                    return

                email = self.data.get('email', 'Unknown')
                student_name = self.data.get('username', 'Unknown')

                # Check if the student with this email is registered for the class with the specified CRN
                cursor.execute("SELECT email FROM Students WHERE email = %s AND crn = %s", (email, self.crn))
                result = cursor.fetchone()

                if not result:
                    messagebox.showwarning('Warning', 'Student not registered for this class or unrecognized QR code. Please register')
                    continue

                student_email = result[0]

                # Highlight the QR code area
                rect = qr.rect
                frame = cv2.rectangle(frame, (rect.left, rect.top),
                                      (rect.left + rect.width, rect.top + rect.height), (0, 255, 0), 2)

                # Record attendance
                cursor.execute("""
                    INSERT INTO Attendance_Log (student_email, class_crn, attendance_date, attendance_time, method) 
                    VALUES (
                        (%s), 
                        (%s),
                        CURDATE(),
                        CURTIME(),
                        'QR Code'
                    )
                """, (student_email, self.crn))
                conn.commit()

                messagebox.showinfo('QR Code Detected', f'Welcome {student_name}, attendance marked!')

                detected = True  # mark that a QR code was detected

                self.reset_for_next_login()  # reset for next login

        except Exception as e:
            print("Database error:", e)
        finally:
            if conn:
                conn.close()

        # Display the processed frame in the UI
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(img_rgb, (640, 480))
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)

        self.webcam_label.imgtk = imgtk
        self.webcam_label.configure(image=imgtk)

        # allows the webcam to continue running even after a QR code is detected and processed
        self.webcam_label.after(10, self.process_webcam)

    # Reset data for the next login attempt
    def reset_for_next_login(self):
        self.data = {}

    # Stop the webcam and release resources
    def stop_webcam(self):
        self.cap.release()

    # Display a given QR code image in a new window, once registered
    def show_qr_code(self, image_source):
        new_window = tk.Toplevel(self.root)
        new_window.title("Your QR Code")

        # Check if image_source is a string (file path) or an Image object
        if isinstance(image_source, str):
            img = Image.open(image_source)
        else:
            img = image_source

        img = img.resize((300, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        label = tk.Label(new_window, image=img)
        label.image = img
        label.pack()

    def register(self):
        # Open registration form window
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Register")

        # Username input
        username_label = util.get_text_label(self.register_window, "Username:", font_size=16)
        username_label.pack()

        self.username_entry = util.get_entry_text(self.register_window, height=1, width=30, font_size=16)
        self.username_entry.pack()

        # Email input
        email_label = util.get_text_label(self.register_window, "Email:", font_size=16)
        email_label.pack()

        self.email_entry = util.get_entry_text(self.register_window, height=1, width=30, font_size=16)
        self.email_entry.pack()

        # Submit registration button
        submit_button = util.get_button(self.register_window, 'Submit', 'green', self.submit_registration)
        submit_button.pack()

        self.register_window.grab_set()

    def submit_registration(self):
        # Process the registration form submission
        username = self.username_entry.get("1.0", 'end-1c').strip()
        email = self.email_entry.get("1.0", 'end-1c').strip()

        if not (username and email):
            messagebox.showwarning('Registration Failed', 'Both username and email are required.')
            return

        conn = None
        try:
            conn = connect()
            cursor = conn.cursor()

            # Check if this email is already registered in the database for the given CRN
            cursor.execute("SELECT qr_code_file FROM Students WHERE email = %s AND CRN = %s", (email, self.crn))
            qr_result = cursor.fetchone()

            if qr_result and qr_result[0]:
                messagebox.showwarning('Registration Failed', f'Email {email} is already registered.')
                return

            # Generate the QR code for the new registration
            qr_data = {
                "username": username,
                "email": email,
                "CRN": self.crn
            }
            json_str = json.dumps(qr_data)
            qr_image = self.generate_qr_code(json_str, email)  # This should return a PIL Image object

            # Convert the PIL Image object to binary
            buf = BytesIO()
            qr_image.save(buf, format="PNG")
            binary_data = buf.getvalue()

            # Save user details and QR code in the database
            if qr_result:
                update_query = """
                UPDATE Students 
                SET qr_code_file = %s 
                WHERE email = %s
                """
                cursor.execute(update_query, (binary_data, email))
            else:
                # If not, create a new record for the user with their QR code and other details
                insert_query = """
                INSERT INTO Students (student_name, email, crn, qr_code_file) 
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (username, email, self.crn, binary_data))
            conn.commit()

            util.msg_box("Success", f"{username} was successfully registered for the QR system.")

            # Show the QR code directly from the PIL Image object
            self.show_qr_code(qr_image)

            self.register_window.destroy()

        except Exception as e:
            messagebox.showerror('Registration Error', f'An error occurred: {e}')
        finally:
            if conn:
                conn.close()

    def generate_qr_code(self, json_str, email):
        # Generate a QR code image from a given JSON string
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json_str)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Convert image to bytes
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        img_bytes = buf.getvalue()

        # Store in database
        conn = None
        try:
            conn = connect()
            cursor = conn.cursor()

            # Update the QR code for the given email (assuming email is unique in the database)
            update_query = """
                UPDATE Students 
                SET qr_code_file = %s 
                WHERE email = %s
                """
            cursor.execute(update_query, (img_bytes, email))

            if cursor.rowcount == 0:
                # If no rows were updated, the email was not found in the database
                print(f"Warning: Email {email} not found in Students table. QR code not updated.")

            conn.commit()

        except Exception as e:
            print(f"Error saving QR code to database: {e}")
        finally:
            if conn:
                conn.close()

        return img

    # Retrieve a user's QR code using their email address
    def retrieve_qr_code(self):
        email = simpledialog.askstring("Retrieve QR", "Enter your email: ")
        if not email:
            return

        # Fetch QR code from database
        try:
            conn = connect()
            cursor = conn.cursor()
            select_query = "SELECT qr_code_file FROM Students WHERE email = %s"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()

            if result and result[0]:  # Check if result is not None and qr_code_file is not None
                qr_bytes = result[0]

                # Convert bytes back to an image
                img = Image.open(io.BytesIO(qr_bytes))
                self.show_qr_code(img)

            else:
                messagebox.showwarning('Retrieve QR', 'QR code not found or not created yet.')

        except Exception as e:
            print(f"Error fetching QR code from database: {e}")
            messagebox.showerror('Error', f'An error occurred while fetching the QR code: {e}')
        finally:
            if conn:
                conn.close()

    # Closes the application safely, ensuring the webcam is released and the Tkinter main loop is stopped.
    def destroy(self):
        self.stop_webcam()
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.root.quit()


# Initializes and runs the main window for the QR Code Entry application
def run_qr_code_entry_window(crn):
    root = tk.Tk()
    app = QRCodeEntryApp(root, crn)
    root.mainloop()