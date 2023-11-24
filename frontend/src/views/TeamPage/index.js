import React from 'react';
import './TeamPage.css'; // Ensure you have this CSS file

const teamMembers = [
  {
    name: 'Rickey Reyes-Pena',
    role: 'Computer Science Student - GSU',
    skills: 'Java, Python',
    description: `Rickey is a dedicated student with a keen interest in software development and a strong grasp of Java and Python. His problem-solving abilities and technical knowledge are crucial to the technical aspects of our projects. Rickey is committed to leveraging his skills to contribute significantly to the development of our Class Attendance System. His proactive approach and willingness to learn make him an invaluable member of the team.`,
    
  },
  {
    name: 'Heeba Merchant',
    role: 'Fourth-year Computer Science Student - GSU',
    skills: 'Java, HTML',
    description: `Heeba's passion for technology is matched by her proficiency in Java and HTML, which she has applied to various projects, including revamping websites to enhance user experiences. Her recent internship allowed her to refine her skills further and take on challenges in software engineering. Heeba's enthusiasm for continuous learning and her ability to apply technical knowledge creatively are great assets to our team.`,
   
  },
  {
    name: 'Julian Vanderpool',
    role: 'Computer Science Student - GSU',
    skills: 'Java, Python, Scala, SQL',
    description: `Julian has demonstrated expertise in software engineering, particularly in backend development. His contributions to projects utilizing Kafka and Elasticsearch showcase his ability to work with complex data systems. Julian's skills are complemented by his active participation in collegiate programming communities and his commitment to discussing and addressing social issues through technology.`,
    
  },
  {
    name: 'Titobi Labisi',
    role: 'Computer Science Major - GSU',
    skills: 'Swift, Xcode, Firebase, Python, Java',
    description: `Titobi Labisi brings a dynamic blend of skills to our team, combining her knowledge of mobile application development with her proficiency in Swift, Xcode, and Firebase. Her recent project contributions have showcased her ability to adapt and apply her skills in practical settings. Titobi's enthusiasm for technology is evident in her technical writing, and her commitment to expanding her expertise in Python and Java is commendable.`,
    
  },
  {
    name: 'Stanley Delva',
    role: 'Computer Science Student - GSU',
    skills: 'Java, Python, JavaScript, SQL, React, Git',
    description: `Stanley Delva's breadth of expertise in programming languages and web development frameworks is a cornerstone of our project. His experience as a Software Engineer Intern at American Express has endowed him with valuable industry insights into data processing and agile methodologies. Stanley's contributions to open-source projects and his dedication to mastering new technologies make him an invaluable asset.`,
    
  }
];

const TeamPage = () => {
  return (
    <div className="team-page-container">
      <h1>Our Team</h1>
      <div className="team-members">
        {teamMembers.map(member => (
          <div className="team-member" key={member.name}>
            <h2>{member.name}</h2>
            <p className="team-member-role">{member.role}</p>
            <p className="team-member-skills">Skills: {member.skills}</p>
            <p className="team-member-description">{member.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TeamPage;
