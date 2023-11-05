import React from 'react';
import './AboutPage.css'; // This should match the CSS filename

const About = () => {
  return (
    <div className="about-container">
      <h1>About Us</h1>
      <p>Class Attendance Using Facial Recognition is the premier platform for managing academic classes and tracking attendance with ease. Designed for both professors and students, our application ensures a seamless educational experience.</p>
      <section>
        <h2>Our Mission</h2>
        <p>We aim to empower educators and students with technology that simplifies academic administration and enhances the learning experience.</p>
      </section>
      <section>
        <h2>Features for Professors</h2>
        <p>Professors have access to powerful tools for class management and attendance reporting, all within a user-friendly interface.</p>
      </section>
      <section>
        <h2>Features for Students</h2>
        <p>Students can conveniently mark attendance with cutting-edge facial recognition and QR code technology.</p>
      </section>
      <section>
        <h2>Innovative Technology</h2>
        <p>Our commitment to innovation means we continually improve our platform with the latest technological advancements.</p>
      </section>
      <section>
        <h2>Security and Privacy</h2>
        <p>User security and privacy are at the forefront of our design, ensuring that all data is handled with the utmost care.</p>
      </section>
      <section>
        <h2>Future Outlook</h2>
        <p>As our Class Attendance System grows, we will continue to introduce new features and expand our capabilities to meet the needs of our users.</p>
      </section>
    </div>
  );
};

export default About;