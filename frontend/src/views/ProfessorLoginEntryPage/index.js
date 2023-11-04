import './ProfessorLoginEntry.css';
import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom'; // Importing useNavigate

const ProfessorLogin = () => {
    const navigate = useNavigate(); // Initialize navigate function

    // Initializing formData state
    const [formData, setFormData] = useState({
        crn: '',
        email: '',
        password: '',
    });

    const [showPassword, setShowPassword] = useState(false); //State for toggling password visibility


    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevData => ({
            ...prevData,
            [name]: value
        }));
    };

    const handleSubmit = () => {
        // Use the formData directly as the JSON payload
        const formPayload = JSON.stringify(formData);

        console.log(formData);

        // Make an API call to the backend with formData
        fetch('http://127.0.0.1:8000/professor/login/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Assuming you're using CSRF checks with DRF (optional line)
                'X-CSRFToken': document.cookie.split('csrftoken=')[1]
            },
            body: formPayload
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === "success") {
                toast.success('Login successful!');
                setTimeout(() => {
                    navigate('/professor-generateLog'); // Redirecting after a delay
                }, 2500); // 2.5 seconds delay
            } else if(data.status === "error") {
                toast.error(data.message);
            }
        })
        .catch(error => {
            console.error("There was an error processing the request:", error);
        });
    };

    return (
        <div className="prof-login-container">
            <h1 className="prof-login-h1">Professor Login</h1>
            {/* ... (rest of the form elements remain unchanged) ... */}
            
            <h2 className="prof-login-h2">CRN</h2>
            <div className="prof-login-input-container">
                <input 
                    className="prof-login-input" 
                    type="text" 
                    placeholder="Enter CRN..." 
                    name="crn" 
                    value={formData.crn} 
                    onChange={handleChange}
                    autoComplete="off"
                />
            </div>

            <h2 className="prof-login-h2">Email</h2>
            <div className="prof-login-input-container">
                <input 
                    className="prof-login-input" 
                    type="email" 
                    placeholder="Enter Email..." 
                    name="email" 
                    value={formData.email} 
                    onChange={handleChange}
                    autoComplete="email"
                />
            </div>

            <h2 className="prof-login-h2">Password</h2>
<           div className="prof-login-input-container">
                <input 
                    className="prof-login-input" 
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
            
            <button className="loginEntry-btn" onClick={handleSubmit}>Login</button>
        </div>
    );
}

export default ProfessorLogin;