import './ProfessorGenerateLogPage.css';
import React from 'react';

const ProfessorGenerateLog = () => {

    const handleGenerateClick = async () => {
        try {
            // backend endpoint for generating the attendance log
            const response = await fetch('http://127.0.0.1:8000/professor/generateLog/', 
            { 
                method: 'GET',
                credentials: 'include'

            });
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                // the filename you want
                a.download = 'attendance_report.xlsx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                // Handle more specific errors based on the backend's response
            const data = await response.json();
            console.error('Failed to generate attendance report. Reason:', data.message);
            }
        } catch (error) {
            console.error('There was an error generating the attendance report.', error);
        }
    }

    return (
        <div className="professor-generate-log-container">
            <h1 className="professor-generate-log-h1">Generate Attendance records</h1>
            <h2 className="professor-generate-log-h2">Click the button below to get the attendance records</h2>
            <button className="professor-generate-log-btn" onClick={handleGenerateClick}>Generate</button>
        </div>
    );
};

export default ProfessorGenerateLog;