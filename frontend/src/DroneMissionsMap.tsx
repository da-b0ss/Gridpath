import React, { useEffect, useRef, useState } from 'react';

interface DroneMissionsMapProps {
  /** Optional width of the map container */
  width?: string | number;
  /** Optional height of the map container */
  height?: string | number;
  /** API base URL */
  apiUrl?: string;
}

/**
 * DroneMissionsMap Component
 *
 * This component renders a drone missions map visualization using Plotly.
 * The visualization includes flight zones, drone missions, and various map layers.
 */
const DroneMissionsMap: React.FC<DroneMissionsMapProps> = ({
  width = '100%',
  height = '100vh',
  apiUrl = 'http://localhost:5000'
}) => {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [mapKey, setMapKey] = useState(Date.now());

  useEffect(() => {
    // Any additional initialization logic can go here
  }, []);

  const refreshDisplay = async () => {
    setIsLoading(true);
    setError(null);
    setMessage(null);

    try {
      const response = await fetch(`${apiUrl}/api/run-pipeline`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (data.success) {
        setMessage('Display refreshed successfully!');
        // Force iframe reload by updating the key
        setMapKey(Date.now());
      } else {
        setError(data.message || 'Failed to refresh display');
      }
    } catch (err) {
      setError(`Error: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      style={{
        width: typeof width === 'number' ? `${width}px` : width,
        height: typeof height === 'number' ? `${height}px` : height,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
      }}
    >
      {/* Control Panel */}
      <div style={{
        padding: '12px 20px',
        backgroundColor: '#f5f5f5',
        borderBottom: '1px solid #ddd',
        display: 'flex',
        gap: '12px',
        alignItems: 'center',
        flexWrap: 'wrap'
      }}>
        <button
          onClick={refreshDisplay}
          disabled={isLoading}
          style={{
            padding: '10px 20px',
            backgroundColor: isLoading ? '#ccc' : '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '14px',
            fontWeight: '500',
            transition: 'background-color 0.2s'
          }}
          onMouseEnter={(e) => {
            if (!isLoading) {
              e.currentTarget.style.backgroundColor = '#45a049';
            }
          }}
          onMouseLeave={(e) => {
            if (!isLoading) {
              e.currentTarget.style.backgroundColor = '#4CAF50';
            }
          }}
        >
          {isLoading ? 'Refreshing Display...' : 'Refresh Display'}
        </button>

        {/* Status Messages */}
        {message && (
          <span style={{ color: '#4CAF50', fontSize: '14px' }}>
            ✓ {message}
          </span>
        )}
        {error && (
          <span style={{ color: '#f44336', fontSize: '14px' }}>
            ✗ {error}
          </span>
        )}
      </div>

      {/* Map Container */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <iframe
          ref={iframeRef}
          key={mapKey}
          src={`/drone_missions_map.html?t=${mapKey}`}
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
            margin: 0,
            padding: 0
          }}
          title="Drone Missions Map"
          sandbox="allow-scripts allow-same-origin"
          loading="lazy"
        />
      </div>
    </div>
  );
};

export default DroneMissionsMap;
