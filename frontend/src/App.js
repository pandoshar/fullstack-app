import React, { useState, useEffect } from 'react';
const API_URL = 'https://fullstack-app-production-fceb.up.railway.app';

function App() {
  const [tasks, setTasks] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => { fetchTasks(); }, []);

  const fetchTasks = () => {
    fetch(`${API_URL}/api/data`).then(res => res.json()).then(setTasks);
  };

  const addTask = (e) => {
    e.preventDefault();
    fetch(`${API_URL}/api/data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: input })
    }).then(() => { setInput(''); fetchTasks(); });
  };

  const deleteTask = (id) => {
    fetch(`${API_URL}/api/data/${id}`, { method: 'DELETE' }).then(fetchTasks);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Student: Adilet Askarbekov (ID: 230141034)</h1>
      <form onSubmit={addTask}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="New task..." />
        <button type="submit">Add</button>
      </form>
      <ul>
        {tasks.map(t => (
          <li key={t.id}>
            {t.title} <button onClick={() => deleteTask(t.id)}>x</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
