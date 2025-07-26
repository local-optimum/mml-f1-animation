# MML F1 Race Visualization 🏎️🏁

An immersive 3D Formula 1 race visualization built with MML (Metaverse Markup Language) that replays actual F1 telemetry data from the 2025 Silverstone Grand Prix. Watch all 20 drivers race around the iconic Silverstone circuit in real-time with team colors, driver abbreviations, and professional lighting.

## 🏆 Features

### Complete F1 Grid
- **20 Drivers**: Full grid from the 2025 Silverstone Grand Prix
- **Real Telemetry**: Actual position data from the race
- **Team Colors**: Each cube colored by their F1 team
- **Driver Abbreviations**: F1-style 3-letter codes (VER, HAM, NOR, etc.)

### Visual Excellence
- **Dynamic Labels**: Driver names follow their cubes as they race
- **Professional Lighting**: 4-point lighting system for perfect illumination
- **Smooth Animation**: 8,468 coordinate positions per driver
- **10x Movement Scale**: Dramatic visualization of race movement
- **30x Speed Replay**: 4.7-minute race duration

### Technical Innovation
- **Real F1 Data**: Extracted using `fastf1` Python library
- **Coordinate Transformation**: Proper mapping from F1 (Z-up) to MML (Y-up)
- **Data Filtering**: Removes stationary positions for clean animation
- **Team Color Mapping**: Accurate F1 team colors

## 🏎️ The Complete F1 Grid

### Red Bull Racing (Blue #3671C6)
- **VER** - Max Verstappen (Driver 1)
- **TSU** - Yuki Tsunoda (Driver 22)

### Ferrari (Red #F91536)
- **HAM** - Lewis Hamilton (Driver 44)
- **LEC** - Charles Leclerc (Driver 16)

### McLaren (Orange #FF8700)
- **NOR** - Lando Norris (Driver 4)
- **PIA** - Oscar Piastri (Driver 81)

### Mercedes (Teal #6CD3BF)
- **RUS** - George Russell (Driver 63)
- **ANT** - Kimi Antonelli (Driver 12)

### Aston Martin (Green #358C75)
- **STR** - Lance Stroll (Driver 18)
- **ALO** - Fernando Alonso (Driver 14)

### Alpine (Blue #2293D1)
- **GAS** - Pierre Gasly (Driver 10)
- **COL** - Franco Colapinto (Driver 43)

### Williams (Blue #37BEDD)
- **ALB** - Alexander Albon (Driver 23)
- **SAI** - Carlos Sainz (Driver 55)

### Haas F1 Team (Gray #B6BABD)
- **BEA** - Oliver Bearman (Driver 87)
- **OCO** - Esteban Ocon (Driver 31)

### Other Teams
- **HUL** - Nico Hulkenberg (Driver 27) - Kick Sauber
- **HAD** - Isack Hadjar (Driver 6) - Racing Bulls
- **BOR** - Gabriel Bortoleto (Driver 5) - Kick Sauber
- **LAW** - Liam Lawson (Driver 30) - Racing Bulls

## 🚀 Getting Started

### Prerequisites
- Node.js
- Python 3.8+
- `fastf1` library for F1 data extraction

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/local-optimum/mml-f1-animation.git
   cd mml-f1-animation
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate F1 coordinate data**
   ```bash
   python3 extract_f1_coordinates.py
   ```

5. **Start the MML server**
   ```bash
   npm start
   ```

6. **View the race**
   Open `http://localhost:8080` in your browser

## 📊 Data Processing

### F1 Data Extraction
The `extract_f1_coordinates.py` script:
- Downloads 2025 Silverstone Grand Prix telemetry data
- Extracts position data for all 20 drivers
- Scales coordinates by 100x for dramatic visualization
- Downsamples to 1 position per second
- Filters out stationary positions
- Transforms coordinates from F1 (Z-up) to MML (Y-up)
- Generates `assets/f1-coordinates.js` with 8,468 positions per driver

### Technical Details
- **Data Source**: 2025 British Grand Prix (Silverstone)
- **Coordinate Scale**: 1/100 (10x larger than original)
- **Update Frequency**: 20 times per second
- **Replay Speed**: 30x faster than real-time
- **Total Duration**: 4.7 minutes
- **Data Points**: 169,360 total coordinate positions

## 🎮 Controls

- **Automatic Playback**: Race starts automatically when page loads
- **Real-time Labels**: Driver abbreviations follow their cubes
- **Team Identification**: Colors match official F1 team liveries
- **Smooth Animation**: 50ms update intervals for fluid movement

## 🏗️ Architecture

### MML Document Structure
- **20 m-cube elements**: One for each F1 driver
- **20 m-label elements**: Driver abbreviations above each cube
- **4 m-light elements**: Professional lighting setup
- **JavaScript animation**: Coordinate-based position updates

### Data Flow
1. Python script extracts F1 telemetry data
2. Coordinates processed and scaled
3. JavaScript file generated with coordinate arrays
4. MML document loads coordinates asynchronously
5. Real-time position updates drive cube movement

## 🌟 Features in Detail

### Professional Lighting
- **Main Overhead Light**: High-intensity illumination from above
- **Front Lighting**: Eliminates shadows from camera perspective
- **Back Lighting**: Provides depth and contrast
- **Side Lighting**: Fills in remaining shadows

### Dynamic Labels
- **F1 Abbreviations**: VER, HAM, NOR, PIA, etc.
- **Following Movement**: Labels stay above their cubes
- **Black Text**: High contrast for readability
- **Real-time Updates**: Synchronized with cube positions

### Team Color Accuracy
- **Official F1 Colors**: Matches team liveries
- **Consistent Branding**: Same colors for teammates
- **Visual Clarity**: Easy team identification during race

## 🔧 Customization

### Adding New Races
1. Update the session in `extract_f1_coordinates.py`
2. Run the script to generate new coordinates
3. The MML document automatically uses the new data

### Adjusting Speed
- Modify `timeStepDuration` in the generated JavaScript
- Lower values = faster replay
- Higher values = slower replay

### Changing Scale
- Adjust the scaling factor in the Python script
- Currently set to 1/100 for dramatic effect
- Can be modified for different visualization styles

## 📈 Performance

- **Smooth 60fps**: Optimized for fluid animation
- **Efficient Data Loading**: Asynchronous coordinate loading
- **Memory Efficient**: Streamlined coordinate arrays
- **Real-time Updates**: 20Hz position updates

## 🎯 Use Cases

- **F1 Analysis**: Study race strategies and driver performance
- **Educational**: Learn about F1 racing and telemetry
- **Entertainment**: Immersive F1 race visualization
- **Research**: Analyze racing data and patterns

## 🤝 Contributing

This project demonstrates the power of MML for creating immersive 3D visualizations. Feel free to:
- Add new races or tracks
- Improve the lighting or visual effects
- Add more driver information
- Create additional F1-themed features

## 📄 License

This project is open source and available under the MIT License.

---

**Experience the thrill of Formula 1 racing in 3D!** 🏎️🏁
