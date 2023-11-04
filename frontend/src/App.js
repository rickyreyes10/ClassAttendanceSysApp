import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './views/HomePage';
import AboutPage from './views/AboutPage';
import HowToUsePage from './views/HowToUsePage';
import TeamPage from './views/TeamPage';
import ProfessorOptionsPage from './views/ProfessorOptionsPage'
import StudentCRNentryPage from './views/StudentCRNentryPage';
import ProfessorLoginEntryPage from './views/ProfessorLoginEntryPage';
import ProfessorCreateEntryPage from './views/ProfessorCreateEntryPage';
import ProfessorDeleteEntryPage from './views/ProfessorDeleteEntryPage';
import ProfessorGenerateLogPage from './views/ProfessorGenerateLogPage';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/about" element={<AboutPage />} />
                <Route path="/how-to-use" element={<HowToUsePage />} />
                <Route path="/team" element={<TeamPage />} />
                <Route path="/professor-options" element={<ProfessorOptionsPage />} />
                <Route path="/student-crn-entry" element={<StudentCRNentryPage />} />
                <Route path="/professor-login" element={<ProfessorLoginEntryPage />} />
                <Route path="/professor-create" element={<ProfessorCreateEntryPage />} />
                <Route path="/professor-delete" element={<ProfessorDeleteEntryPage />} />
                <Route path="/professor-generateLog" element={<ProfessorGenerateLogPage />} />
            </Routes>
        </Router>
    );
}

export default App;