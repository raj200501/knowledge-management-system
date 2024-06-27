import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css';

const App = () => {
    const [entries, setEntries] = useState([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    useEffect(() => {
        axios.get('/entries')
            .then(response => {
                setEntries(response.data);
            });
    }, []);

    const addEntry = () => {
        axios.post('/entry', { title, content })
            .then(response => {
                setEntries([...entries, response.data]);
                setTitle('');
                setContent('');
            });
    };

    return (
        <div className="app">
            <h1>Knowledge Management System</h1>
            <div className="form">
                <input 
                    type="text" 
                    value={title} 
                    onChange={e => setTitle(e.target.value)} 
                    placeholder="Title" 
                />
                <textarea 
                    value={content} 
                    onChange={e => setContent(e.target.value)} 
                    placeholder="Content"
                ></textarea>
                <button onClick={addEntry}>Save Entry</button>
            </div>
            <div className="entries">
                {entries.map(entry => (
                    <div key={entry.id} className="entry">
                        <h2>{entry.title}</h2>
                        <p>{entry.content}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default App;
