// Cube coordinates data for moving cubes
// Each cube has an array of coordinate objects with x, y, z positions
// Time steps are 1 second apart (0s, 1s, 2s, etc.)

// Cube coordinates array - accessible globally
const cubeCoordinates = [
  // Cube 1 coordinates (red) - straight line movement along X-axis
  [
    {x: 0, y: 0, z: 0},    // 0 seconds
    {x: 1, y: 0, z: 0},    // 1 second
    {x: 2, y: 0, z: 0},    // 2 seconds
    {x: 3, y: 0, z: 0},    // 3 seconds
    {x: 4, y: 0, z: 0},    // 4 seconds
    {x: 5, y: 0, z: 0},    // 5 seconds
    {x: 6, y: 0, z: 0},    // 6 seconds
    {x: 7, y: 0, z: 0},    // 7 seconds
    {x: 8, y: 0, z: 0},    // 8 seconds
    {x: 9, y: 0, z: 0},    // 9 seconds
    {x: 10, y: 0, z: 0},   // 10 seconds
  ],
  
  // Cube 2 coordinates (teal) - parallel movement
  [
    {x: 1, y: 0, z: 0},    // 0 seconds
    {x: 2, y: 0, z: 0},    // 1 second
    {x: 3, y: 0, z: 0},    // 2 seconds
    {x: 4, y: 0, z: 0},    // 3 seconds
    {x: 5, y: 0, z: 0},    // 4 seconds
    {x: 6, y: 0, z: 0},    // 5 seconds
    {x: 7, y: 0, z: 0},    // 6 seconds
    {x: 8, y: 0, z: 0},    // 7 seconds
    {x: 9, y: 0, z: 0},    // 8 seconds
    {x: 10, y: 0, z: 0},   // 9 seconds
    {x: 11, y: 0, z: 0},   // 10 seconds
  ],
  
  // Cube 3 coordinates (blue) - parallel movement
  [
    {x: 2, y: 0, z: 0},    // 0 seconds
    {x: 3, y: 0, z: 0},    // 1 second
    {x: 4, y: 0, z: 0},    // 2 seconds
    {x: 5, y: 0, z: 0},    // 3 seconds
    {x: 6, y: 0, z: 0},    // 4 seconds
    {x: 7, y: 0, z: 0},    // 5 seconds
    {x: 8, y: 0, z: 0},    // 6 seconds
    {x: 9, y: 0, z: 0},    // 7 seconds
    {x: 10, y: 0, z: 0},   // 8 seconds
    {x: 11, y: 0, z: 0},   // 9 seconds
    {x: 12, y: 0, z: 0},   // 10 seconds
  ]
];

// Configuration for the coordinate system - accessible globally
const coordinateConfig = {
  timeStepDuration: 1000, // 1 second per step in milliseconds
  totalTimeSteps: cubeCoordinates[0].length,
  updateInterval: 50, // Update frequency in milliseconds (20 times per second)
};

// Helper function to get coordinates for a specific time step
function getCoordinatesAtTimeStep(timeStep) {
  return cubeCoordinates.map(cubeCoords => cubeCoords[timeStep]);
}

// Helper function to get the current time step based on document time
function getCurrentTimeStep(currentTime) {
  return Math.floor(currentTime / coordinateConfig.timeStepDuration) % coordinateConfig.totalTimeSteps;
} 