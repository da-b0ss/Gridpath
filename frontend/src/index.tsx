import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Global dark theme styles
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: #0a0e1a;
    color: #e2e8f0;
    overflow: hidden;
  }

  #root {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  }

  /* Scrollbar Styling */
  ::-webkit-scrollbar {
    width: 10px;
    height: 10px;
  }

  ::-webkit-scrollbar-track {
    background: #0f1420;
    border-radius: 5px;
  }

  ::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 5px;
    border: 2px solid #0f1420;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
  }

  /* Animations */
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.6;
    }
  }

  @keyframes slideIn {
    from {
      transform: translateX(-100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes glow {
    0%, 100% {
      box-shadow: 0 0 5px rgba(99, 102, 241, 0.3);
    }
    50% {
      box-shadow: 0 0 20px rgba(99, 102, 241, 0.6);
    }
  }

  /* Selection styling */
  ::selection {
    background: rgba(99, 102, 241, 0.3);
    color: #e2e8f0;
  }

  /* Focus styling */
  button:focus-visible,
  input:focus-visible,
  select:focus-visible {
    outline: 2px solid #6366f1;
    outline-offset: 2px;
  }
`;
document.head.appendChild(styleSheet);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
