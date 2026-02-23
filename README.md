# OSPF LSDB Visualizer

OSPF LSDB Visualizer is a Python-based tool that converts raw OSPF LSDB output collected from routers into an interactive topology graph.  
The goal is to simplify network topology analysis by transforming Link-State Database information into a structured and visual representation.

---

## 🎯 Objective

Convert OSPF LSDB data into a graph structure to enable:

- Topology visualization  
- OSPF adjacency analysis  
- Faster troubleshooting  
- Network structure validation  

The project is designed to assist network engineers in understanding real OSPF topologies directly from LSDB data.

---

## 🏗 Architecture Overview

Processing pipeline:

```
Raw LSDB Output
        ↓
TextFSM Template (FSM-based parsing)
        ↓
Structured Python Data
        ↓
NetworkX Graph
        ↓
PyVis Interactive HTML
```

### Core Technologies

- Python 3.12+
- TextFSM (FSM-based parsing)
- NetworkX (graph modeling)
- PyVis (interactive HTML visualization)

---

## 🔎 Parsing Model (FSM)

The LSDB parsing is based on TextFSM templates using a Finite State Machine (FSM) model.

This allows:

- Extraction of Router LSAs  
- Identification of `Ls id` and `Adv rtr`  
- Detection of PTP adjacencies  
- Structured transformation of raw CLI output into graph-ready data  

FSM ensures predictable parsing and makes vendor-specific templates easier to maintain.

---

## 📥 Data Collection (Huawei)

Currently supported vendor: Huawei

The command must be executed on ABR routers to ensure complete topology visibility.

### Required Command

```bash
display ospf lsdb router
```

Save the full output into a file inside the `input/` directory.

File naming convention must include the vendor name:

```
input/huawei_example.txt
```

---

## 📂 Project Structure

```
ospf-lsdb-visualizer/
│
├── input/
│   └── example.txt
│
├── output/
│   │── graph.graphml
│   └── graph.html
│
├── template/
│   └── template.textsfm
│
├── src/
│   │── graph/
│   │   │── graph_builder.py
│   │   └── graph_options.json
│   └── parser/
│       │── vendorA.py
│       └── graph_options.json
│
├── requirements.txt
└── main.py
```

---

## ⚙️ Installation

Recommended:

```
Python 3.12 or higher
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Main dependencies:

- networkx  
- pyvis  
- textfsm  

---

## 🚀 Execution

Run:

```bash
python main.py output_name
```

This will generate:

```
output_name.html
output_name.graphml
```

The output file is an interactive HTML graph visualization and a structural graph.

---

## 🌐 HTML Visualization

The generated HTML file contains an interactive topology graph rendered with PyVis.

Features include:

- Node dragging  
- Zoom  
- Dynamic physics simulation  
- Interactive edge inspection  

---

## 🎛 Graph Customization

Graph behavior can be adjusted via:

```
ospf-lsdb-visualizer/src/graph/graph_options.json
```

Changes directly affect the generated HTML visualization.

---

## 📌 Current Limitations

- Supports Huawei only  
- Supports PTP adjacencies only  
- Single input file per execution  
- Must be executed on ABR routers  

---

## 🔮 Roadmap

Planned improvements:

- Multi-vendor suport  
- Multiple input file support 

---

## 🧪 Example Dataset

The example dataset included in the repository is synthetic and does not represent a real network.

It is provided only for demonstration purposes.

---

## 💡 Use Cases

- OSPF troubleshooting  
- Topology validation  
- Redundancy verification  
- Network documentation automation  
- Pre-change topology simulation baseline  

---

## 📜 License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Filipe Pena  
Network Automation  
Brazil  