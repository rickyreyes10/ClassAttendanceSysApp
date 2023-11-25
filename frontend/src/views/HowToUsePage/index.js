import React from 'react';
import './HowToUsePage.css'; // This should be in line with existing CSS files

const HowToUse = () => {
  return (
    <div className="how-to-use-container">
      <h1>How to Use</h1>
      {/* Professor Section */}
      <section className="how-to-use-section">
        <h2>For Professors:</h2>
        <p>Manage your classes effectively with our Class Attendance System by selecting the ‘Professor’ option. Our intuitive interface provides you with the flexibility to handle all your class attendance needs seamlessly. Upon choosing to 'Login', you can access your existing classes with ease. Enter your unique credentials and gain insights into attendance patterns, download reports, and adjust settings specific to each class.

If you're starting a new semester or need to add a new class, the 'Create' option simplifies this process. With just a few clicks, you can enter course details, set up schedules, and establish your class within the system. Our platform ensures that setting up a new class is straightforward and hassle-free.

Occasionally, you may need to remove a class from the system. The 'Delete' function allows you to do this securely and efficiently. Whether a class has concluded or been canceled, you can ensure that all associated data is removed in compliance with data protection standards.

Beyond these core functions, our platform offers a range of tools designed to enhance your teaching experience. Customize attendance criteria, engage with student attendance trends, and leverage our analytics for informed decision-making. With our system, you have the power to manage every aspect of class attendance, giving you more time to focus on what you do best—teaching.

</p>
      </section>
      {/* Student Section */}
      <section className="how-to-use-section">
        <h2>For Students:</h2>
        <p>Recording your attendance is straightforward and secure with our 'Student' portal. Begin by clicking on the 'Student' button from the homepage. You will be prompted to enter the Course Reference Number (CRN) assigned to your class. Once entered, you will be directed to choose between two state-of-the-art attendance verification systems – Facial Recognition or QR Code scanning.

For the Facial Recognition option, ensure your device's camera is enabled. Position yourself in clear view of the camera and follow the on-screen instructions to capture your attendance. The system will compare your image against the class database in real-time, providing a quick and seamless verification process.

If you opt for the QR Code system, use your device's camera to scan the unique QR code provided by your instructor at the start of the class. The code will be scanned, and your attendance will be logged instantly. This method is especially useful if you're attending the class remotely or prefer a contactless check-in process.

Whichever system you choose, our platform guarantees a user-friendly experience. Should you encounter any difficulties, such as lighting issues for facial recognition or scanning errors with the QR code, simple troubleshooting steps are available within the platform. Our support team is also on hand to provide assistance, ensuring your attendance is recorded promptly and accurately, every time.</p>
      </section>
      {/* Navigation Section */}
      <section className="how-to-use-section">
        <h2>Navigation:</h2>
        <p>Use the navigation bar to explore all the functionalities offered. Simple and intuitive, it’s designed to help you find what you need quickly and easily.</p>
      </section>
      {/* Support Section */}
      <section className="how-to-use-section">
        <h2>Support:</h2>
        <p>If you encounter any issues or have questions, our dedicated support team is here to assist you every step of the way.</p>
      </section>
    </div>
  );
};

export default HowToUse;