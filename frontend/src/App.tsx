import React from 'react';
import DroneMissionsMap from './DroneMissionsMap';

/**
 * Main App Component
 *
 * Example usage of the DroneMissionsMap component
 */
function App() {
  return (
    <div className="App">
      <header style={{
        padding: '20px',
        backgroundColor: '#282c34',
        color: 'white',
        textAlign: 'center'
      }}>
        <h1>Drone Missions Visualization</h1>
      </header>

      <main>
        <DroneMissionsMap
          width="100%"
          height="calc(100vh - 80px)"
        />
      </main>
    </div>
  );
}

export default App;
