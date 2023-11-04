import './StudentCRNentryPage.css';
import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you might use routing at some point

const StudentCRNEntry = () => {
    return (
        <div className="student-crn-entry-container">
            <h1 className="student-crn-entry-h1">Student Course Entry</h1>
            <h2 className="student-crn-entry-h2">Enter the CRN of the course you want to take attendance for</h2>
            <input className="student-crn-entry-input" type="text" placeholder="Enter CRN..." />
            <button className="student-crn-entry-submit-btn">Submit</button>
        </div>
    );
};

export default StudentCRNEntry;