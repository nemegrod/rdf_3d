# 🐆 Jaguar RDF 3D Visualization

A **Flask web application** that provides an interactive **3D force-directed graph visualization** of RDF (Resource Description Framework) data about jaguar conservation. The application parses Turtle (.ttl) files on the backend and renders an immersive 3D knowledge graph using **3d-force-graph** and **Three.js**.

## 🌟 Features

### 🎨 **Interactive 3D Visualization**
- **Force-directed graph layout** with realistic physics simulation
- **Color-coded nodes** by entity type (Jaguars, Countries, Organizations, Habitats, etc.)
- **Always-visible labels** on nodes and links using SpriteText
- **Animated particles** showing relationship directions
- **Smooth camera controls** - rotate, zoom, pan with mouse/trackpad
- **Hover tooltips** displaying detailed node information

### 📊 **RDF Knowledge Graph**
- **Comprehensive jaguar ontology** with multiple entity types
- Individual jaguar tracking (names, monitoring data)
- Conservation organizations (NGOs, Government Agencies)
- Geographic data (Countries, States, Regions, Habitats)
- Threats and conservation efforts
- Relationships between all entities

### 🔧 **Technical Features**
- **Server-side RDF parsing** using rdflib in Python
- **Clean data pipeline** from TTL files to JSON graph format
- **Local JavaScript libraries** for better compatibility
- **Responsive design** adapts to any screen size
- **Efficient rendering** handles 100+ nodes and 136+ relationships

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Modern web browser** with WebGL support

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rdf_3d
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

Open your browser and navigate to this address to see the 3D visualization.

## 📁 Project Structure

```
rdf_3d/
├── app.py                      # Flask application and RDF parsing logic
├── templates/
│   └── index.html             # 3D visualization frontend
├── static/
│   └── js/                    # Local JavaScript libraries
│       ├── three.min.js       # Three.js 3D library
│       ├── three-spritetext.js # Text label library
│       └── 3d-force-graph.min.js # Force-directed graph library
├── data/
│   └── jaguars.ttl           # Jaguar RDF data in Turtle format
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Lightweight web framework
- **rdflib 7.0+** - RDF parsing and SPARQL querying
- **Python 3** - Core application logic

### Frontend
- **3d-force-graph 1.70.0** - Force-directed graph visualization
- **Three.js 0.152.0** - WebGL 3D graphics library
- **three-spritetext 1.8.2** - Text label rendering
- **Jinja2** - Template rendering

### Data Format
- **RDF/Turtle (.ttl)** - Knowledge graph data format
- **RDFS/RDF** - Schema and vocabulary
- **JSON** - Graph data transfer format

## 💡 How It Works

1. **Flask Server Starts** - `app.py` initializes the web server
2. **User Accesses Page** - Browser requests the visualization
3. **RDF Parsing** - Backend parses `jaguars.ttl` using rdflib
4. **Data Transformation**:
   - Extracts all entities (subjects and objects)
   - Assigns unique IDs to each node
   - Determines node types from RDF classes
   - Creates links from RDF predicates
   - Sizes nodes by importance (entity type)
5. **JSON Generation** - Converts RDF graph to 3d-force-graph format
6. **Template Rendering** - Jinja2 injects data into HTML
7. **3D Visualization**:
   - Three.js creates WebGL scene
   - Force simulation positions nodes
   - SpriteText renders labels
   - Particles animate along links
8. **User Interaction** - Mouse controls camera, hover shows details

## 🎨 Node Color Scheme

The visualization uses distinct colors for different entity types:

- 🔴 **Jaguar** - Red (`#ff6b6b`) - Individual jaguars
- 🔵 **Country** - Cyan (`#4ecdc4`) - Countries
- 🔵 **State** - Light Blue (`#45b7d1`) - States/provinces
- 🟢 **Region** - Seafoam (`#96ceb4`) - Geographic regions
- 🟡 **MountainRange** - Yellow (`#ffeaa7`) - Mountain ranges
- 🟤 **HabitatArea** - Brown (`#dda15e`) - Habitat areas
- 🟢 **NGO** - Mint (`#a8e6cf`) - Non-governmental organizations
- 🟠 **GovernmentAgency** - Peach (`#ffd3a5`) - Government agencies
- 🟣 **AcademicInstitution** - Lavender (`#c7ceea`) - Academic institutions
- 🔴 **Threat** - Light Red (`#ff8a80`) - Conservation threats
- 🟢 **Wetland/Forest** - Green shades - Habitat types
- 🟣 **Observation** - Purple (`#ba68c8`) - Monitoring observations
- 🔵 **Person** - Sky Blue (`#90caf9`) - People
- 🟢 **Habitat** - Teal (`#4db6ac`) - General habitats
- 🟠 **RecoveryPlan** - Orange (`#ffb74d`) - Recovery plans
- 🟣 **RewildingProgram** - Pink Purple (`#ce93d8`) - Rewilding programs
- 🟪 **JaguarPopulation** - Pink (`#f48fb1`) - Population data
- ⚫ **Entity** - Gray (`#9e9e9e`) - Default/unknown type

## 🎮 Controls

- **Left Click + Drag** - Rotate camera around the graph
- **Right Click + Drag** - Pan camera
- **Scroll Wheel** - Zoom in/out
- **Hover** - Show node details (name and type)

## 📊 Graph Data Format

### Nodes
```json
{
  "id": 0,
  "uri": "http://example.org/resource/Entity",
  "name": "Entity Name",
  "type": "EntityType",
  "group": "EntityType",
  "val": 10
}
```

### Links
```json
{
  "source": 0,
  "target": 1,
  "type": "relationshipType",
  "label": "relationshipType"
}
```

## 🔧 Customization

### Adjust Node Sizes
Edit the size values in `app.py` in the `parse_rdf_to_graph_data` function:

```python
size = 5  # Default size
if node_type == 'Jaguar':
    size = 10  # Jaguars are larger
elif node_type in ['Country', 'State', 'Region']:
    size = 8   # Geographic entities are medium
```

### Modify Force Simulation
Edit the force strength in `templates/index.html`:

```javascript
Graph.d3Force('charge').strength(-220); // Adjust repulsion strength
```

### Change Label Sizes
Edit text height in `templates/index.html`:

```javascript
sprite.textHeight = 8;  // Node labels
sprite.textHeight = 1.5; // Link labels
```

## 📚 RDF Data Structure

The `jaguars.ttl` file contains:

- **Classes**: Jaguar, Country, State, NGO, Threat, Habitat, etc.
- **Properties**: locatedIn, threatens, protects, monitors, rescuedBy, etc.
- **Individuals**: Specific jaguars, organizations, locations, and observations

Example RDF:
```turtle
ex:Isa_BR a ont:Jaguar ;
    rdfs:label "Isa_BR" ;
    ont:locatedIn ex:Brazil ;
    ont:monitoredBy ex:Panthera .
```

## 🔒 Security

- No authentication required (local development)
- No external API keys needed
- All data processed locally
- Static file serving for JavaScript libraries

## 🐛 Troubleshooting

### Graph Not Rendering
- Check browser console for errors
- Verify Flask server is running on port 5000
- Ensure `data/jaguars.ttl` file exists
- Clear browser cache and refresh

### Labels Not Showing
- Verify JavaScript libraries loaded (check Network tab)
- Ensure `static/js/` contains all three JS files
- Check console for `SpriteText is not defined` errors

### Performance Issues
- Reduce node/link count in TTL file
- Adjust force strength (lower = faster)
- Disable particles: remove `.linkDirectionalParticles(2)`

## 📝 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional RDF data sources
- More entity types and colors
- Enhanced node/link styling
- SPARQL query interface
- Graph filtering controls
- Export functionality

---

**Built with Flask, Three.js, and rdflib** 🚀
