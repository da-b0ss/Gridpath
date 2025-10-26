# Drone Missions Map - React TypeScript Component

This project integrates the `drone_missions_map.html` Plotly visualization into a React TypeScript application.

## Project Structure

```
frontend/
├── public/
│   ├── index.html              # Main HTML template
│   └── drone_missions_map.html # Plotly visualization (embedded via iframe)
├── src/
│   ├── App.tsx                 # Main application component
│   ├── DroneMissionsMap.tsx    # Drone map component
│   └── index.tsx               # Application entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## Features

- **React 19** with TypeScript
- **Vite** for fast development and building
- **DroneMissionsMap Component** - A reusable component that displays the Plotly map
- **Responsive Design** - The map adapts to different screen sizes
- **Type Safety** - Full TypeScript support

## Installation

1. Install dependencies:

```bash
cd frontend
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

This will start the Vite dev server at `http://localhost:3000`

## Building for Production

Build the project:

```bash
npm run build
```

The built files will be in the `dist/` directory.

Preview the production build:

```bash
npm run preview
```

## Component Usage

### Basic Usage

```tsx
import DroneMissionsMap from './DroneMissionsMap';

function App() {
  return (
    <div>
      <DroneMissionsMap />
    </div>
  );
}
```

### With Custom Dimensions

```tsx
import DroneMissionsMap from './DroneMissionsMap';

function App() {
  return (
    <DroneMissionsMap
      width="100%"
      height="800px"
    />
  );
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `width` | `string \| number` | `"100%"` | Width of the map container (e.g., "100%", "800px", 800) |
| `height` | `string \| number` | `"100vh"` | Height of the map container (e.g., "100vh", "600px", 600) |

## How It Works

The component uses an iframe to embed the original `drone_missions_map.html` file, which contains:

- **Plotly.js** - The full Plotly library embedded inline
- **MapLibre GL JS** - For rendering the map layers
- **Flight Zone Data** - Polygon coordinates defining the drone flight zone
- **Mission Data** - Lat/lon coordinates of drone missions with clustering support

This approach preserves the original Plotly visualization while making it easy to integrate into a React application.

## Technologies Used

- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Plotly.js** - Data visualization (embedded in HTML)
- **MapLibre GL JS** - Map rendering (embedded in HTML)

## File Locations

- **Source Component**: [src/DroneMissionsMap.tsx](src/DroneMissionsMap.tsx)
- **Example App**: [src/App.tsx](src/App.tsx)
- **Plotly HTML**: [public/drone_missions_map.html](public/drone_missions_map.html)

## Notes

- The `drone_missions_map.html` file is ~5MB due to the embedded Plotly library
- The component uses an iframe for isolation and simplicity
- For production, consider extracting the Plotly data and using react-plotly.js instead of an iframe
- The map includes interactive features like zoom, pan, and clustering

## License

ISC
