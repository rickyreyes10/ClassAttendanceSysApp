import React from 'react';
import './HowToUsePage.css'; // This should be in line with existing CSS files

const HowToUse = () => {
  return (
    <div className="how-to-use-container">
      <h1>How to Use</h1>
      {/* Professor Section */}
      <section className="how-to-use-section">
        <h2>For Professors:</h2>
        <p>Manage your classes effectively by selecting ‘Professor’. From there, choose to login to an existing class, create a new one, or delete a class as needed.</p>
      </section>
      {/* Student Section */}
      <section className="how-to-use-section">
        <h2>For Students:</h2>
        <p>Record your attendance by clicking ‘Student’. Enter your class CRN and follow the prompts to use the Facial Recognition or QR Code attendance systems.</p>
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