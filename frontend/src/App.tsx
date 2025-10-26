import React from 'react';
import DroneMissionsMap from './DroneMissionsMap';

/**
 * Main App Component
 *
 * Example usage of the DroneMissionsMap component
 */
function App() {
  return (
    <div className="App" style={{
      width: '100vw',
      height: '100vh',
      backgroundColor: '#0a0e1a',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden'
    }}>
      <header style={{
        padding: '16px 32px',
        background: 'linear-gradient(135deg, #1a1f35 0%, #0f1420 100%)',
        borderBottom: '1px solid rgba(99, 102, 241, 0.2)',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
        flexShrink: 0,
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '2px',
          background: 'linear-gradient(90deg, transparent, #6366f1, #8b5cf6, transparent)',
          opacity: 0.6
        }} />
        <h1 style={{
          margin: 0,
          fontSize: '24px',
          fontWeight: '700',
          background: 'linear-gradient(135deg, #818cf8 0%, #c084fc 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          letterSpacing: '-0.5px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <span style={{
            fontSize: '26px',
            filter: 'drop-shadow(0 0 8px rgba(99, 102, 241, 0.5))'
          }}>🚁</span>
          Drone Missions Visualization
        </h1>
        <p style={{
          margin: '6px 0 0 36px',
          fontSize: '13px',
          color: '#94a3b8',
          fontWeight: '400'
        }}>
          Real-time mission tracking and flight zone visualization
        </p>
      </header>

      <main style={{ flex: 1, overflow: 'hidden' }}>
        <DroneMissionsMap
          width="100%"
          height="100%"
        />
      </main>
    </div>
  );
}

export default App;
