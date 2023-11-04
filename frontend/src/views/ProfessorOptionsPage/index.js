import './ProfessorOptionsPage.css';
import React from 'react';
import { Link } from 'react-router-dom';

const ProfessorOptions = () => {
    return (
        <div className="prof-options-container">
            <h1 className="prof-options-h1">Professor Options</h1>
            <h2 className="prof-options-h2">Select an option:</h2>
            <Link to="/professor-login" style={{ textDecoration: 'none', color: 'inherit'}}>
                <button className="loginOption-btn">Login</button>
            </Link>
            <Link to="/professor-create" style={{ textDecoration: 'none', color: 'inherit'}}>
                <button className="createOption-btn">Create</button>
            </Link>
            <Link to="/professor-delete" style={{ textDecoration: 'none', color: 'inherit'}}>
                <button className="deleteOption-btn">Delete</button>
            </Link>
        </div>
    );
};

export default ProfessorOptions;