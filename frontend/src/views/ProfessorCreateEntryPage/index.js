import { Link } from 'react-router-dom';
import './ProfessorCreate.css';
import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ProfessorCreate = () => {
    // 1. Setting up the state:
    const [formData, setFormData] = useState({
        courseName: '',
        crn: '',
        email: '',
        password: ''
    });

    const [showPassword, setShowPassword] = useState(false); //State for toggling password visibility

    // 2. Handling user input:
    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevData => ({
            ...prevData,
            [name]: value
        }));
    };

    const handleSubmit = () => {
        console.log(formData);
        // Make an API call to the backend with formData
        fetch('http://127.0.0.1:8000/professor/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === "success") {
                // Handle the success scenario
                // For instance, you can display a success notification or redirect to another page
                toast.success('Class created and details saved successfully!');
            } else if(data.status === "error") {
                // Handle the error scenario
                // Display the error message to the user
                toast.error(data.message);
            }
        })
        .catch(error => {
            // Handle any other network or parsing errors here
            console.error("There was an error processing the request:", error);
        });
    };

    return (
        <div className="prof-create-container">
            <h1 className="prof-create-h1">Professor Create</h1>
            
            <h2 className="prof-create-h2">Enter Course Name</h2>
            <div className="prof-create-input-container">
                <input 
                    className="prof-create-input"
                    type="text"
                    placeholder="Enter Course Name..."
                    name="crn"
                    value={formData.crn}
                    onChange={handleChange}
                    autoComplete="off"
                
                />
            </div>
            
            <h2 className="prof-create-h2">CRN</h2>
            <div className="prof-create-input-container">
                <input 
                    className="prof-create-input" 
                    type="text" 
                    placeholder="Enter CRN..." 
                    name="crn" 
                    value={formData.crn} 
                    onChange={handleChange}
                    autoComplete="off"
                />
            </div>

            <h2 className="prof-create-h2">Email</h2>
            <div className="prof-create-input-container">
                <input 
                    className="prof-create-input" 
                    type="email" 
                    placeholder="Enter Email..." 
                    name="email" 
                    value={formData.email} 
                    onChange={handleChange}
                    autoComplete="email"
                />
            </div>
            
            <h2 className="prof-create-h2">Password</h2>
<           div className="prof-create-input-container">
                <input 
                    className="prof-create-input" 
                    type={showPassword ? "text" : "password"} 
                    placeholder="Enter Password..." 
                    name="password" 
                    value={formData.password} 
                    onChange={handleChange}
                    autoComplete="current-password"
                />

                <i 
                    className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'} toggle-password-icon`} 
                    onClick={() => setShowPassword(prevShowPassword => !prevShowPassword)}
                ></i>
            </div>

            <ToastContainer position={toast.POSITION.TOP_RIGHT}/>
            
            <button className="prof-create-btn" onClick={handleSubmit}>Create</button>
        </div>
    );
}

export default ProfessorCreate;