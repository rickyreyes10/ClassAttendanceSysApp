import './HomePage.css';
import React, { useState } from 'react';
import { GiHamburgerMenu } from 'react-icons/gi';
import { Link } from 'react-router-dom';


const HomePage = () => {
    // State to track if the menu is open or closed
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    return (
        <div className="home-page-container">
            <div className="menu-icon">
                <GiHamburgerMenu 
                    size={35} 
                    color="black" 
                    onClick={() => setIsMenuOpen(!isMenuOpen)} // Toggle the menu state
                />
            </div>
            {isMenuOpen && (
                <div className="menu">
                    <ul>
                        <Link to="/about" onClick={() => setIsMenuOpen(false)}>
                            <li>About</li>
                        </Link>
                        <Link to="/how-to-use" onClick={() => setIsMenuOpen(false)}>
                            <li>How to use</li>
                        </Link>
                        <Link to="/team" onClick={() => setIsMenuOpen(false)}>
                            <li>Team</li>
                        </Link>
                    </ul>
                </div>
            )}
            <h1 className="home-page-h1">Class Attendance System</h1>
            <p className="home-page-intro">
          Welcome to the Class Attendance System! Our innovative platform utilizes 
          facial recognition and QR code technology to streamline attendance tracking. 
          Experience hassle-free, accurate, and secure class attendance management 
          suitable for both professors and students.
            </p>
            {/* You can add icons to these buttons */}
            <Link to="/professor-options" style={{ textDecoration: 'none', color: 'inherit'}}>
                <button className="professor-btn">Professor</button>
            </Link>

            <Link to="/student-crn-entry" style={{ textDecoration: 'none', color: 'inherit'}}>
                <button className="student-btn">Student</button>
            </Link>
        </div>
    );
};

export default HomePage;