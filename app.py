from flask import Flask, render_template
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDFS, RDF
import json
import os

app = Flask(__name__)

# Namespaces
EX = Namespace("http://example.org/resource/")
ONT = Namespace("http://example.org/ontology#")
RDFS_NS = Namespace("http://www.w3.org/2000/01/rdf-schema#")


def get_short_name(uri):
    """Extract a short name from a URI for display"""
    if isinstance(uri, URIRef):
        uri_str = str(uri)
    else:
        uri_str = str(uri)
    
    # Extract local name
    if '#' in uri_str:
        return uri_str.split('#')[-1]
    elif '/' in uri_str:
        return uri_str.split('/')[-1]
    return uri_str


def get_node_label(graph, uri):
    """Get rdfs:label for a URI, or generate a short name"""
    label = None
    for obj in graph.objects(uri, RDFS.label):
        label = str(obj)
        break
    
    if not label:
        label = get_short_name(uri)
    
    return label


def get_node_type(graph, uri):
    """Determine the type of a node based on its RDF type"""
    node_types = []
    for obj in graph.objects(uri, RDF.type):
        type_uri = str(obj)
        if 'ontology#' in type_uri:
            # Extract the class name from the ontology namespace
            type_name = type_uri.split('#')[-1]
            node_types.append(type_name)
    
    # Return the first type found, or 'Entity' as default
    if node_types:
        return node_types[0]
    return 'Entity'


def parse_rdf_to_graph_data(ttl_file_path):
    """Parse RDF/TTL file and convert to 3d-force-graph format"""
    # Load the RDF graph
    g = Graph()
    g.parse(ttl_file_path, format='turtle')
    
    # Collect all nodes (entities)
    nodes_dict = {}
    node_id_map = {}  # Map URIs to node IDs
    
    # First pass: collect all entities that appear as subjects or objects
    for s, p, o in g:
        # Add subject as node
        if isinstance(s, URIRef):
            uri_str = str(s)
            if uri_str not in nodes_dict:
                label = get_node_label(g, s)
                node_type = get_node_type(g, s)
                node_id = len(nodes_dict)
                # Calculate node size based on type importance
                size = 5  # Default size
                if node_type == 'Jaguar':
                    size = 10
                elif node_type in ['Country', 'State', 'Region']:
                    size = 8
                elif node_type in ['NGO', 'GovernmentAgency']:
                    size = 7
                
                nodes_dict[uri_str] = {
                    'id': node_id,
                    'uri': uri_str,
                    'name': label,
                    'type': node_type,
                    'group': node_type,  # Use type as group for coloring
                    'val': size  # Node size for visualization
                }
                node_id_map[uri_str] = node_id
        
        # Add object as node if it's a URI
        if isinstance(o, URIRef):
            uri_str = str(o)
            if uri_str not in nodes_dict:
                label = get_node_label(g, o)
                node_type = get_node_type(g, o)
                node_id = len(nodes_dict)
                # Calculate node size based on type importance
                size = 5  # Default size
                if node_type == 'Jaguar':
                    size = 10
                elif node_type in ['Country', 'State', 'Region']:
                    size = 8
                elif node_type in ['NGO', 'GovernmentAgency']:
                    size = 7
                
                nodes_dict[uri_str] = {
                    'id': node_id,
                    'uri': uri_str,
                    'name': label,
                    'type': node_type,
                    'group': node_type,  # Use type as group for coloring
                    'val': size  # Node size for visualization
                }
                node_id_map[uri_str] = node_id
    
    # Second pass: create links (relationships)
    links = []
    seen_links = set()  # Avoid duplicate links
    
    for s, p, o in g:
        # Only create links for object properties (not literals)
        if isinstance(s, URIRef) and isinstance(o, URIRef):
            # Skip RDF.type relationships as they're already captured in node types
            if p == RDF.type:
                continue
            
            source_id = node_id_map.get(str(s))
            target_id = node_id_map.get(str(o))
            
            if source_id is not None and target_id is not None:
                # Get property name for link label
                prop_name = get_short_name(p)
                
                # Create unique link identifier
                link_key = (source_id, target_id, prop_name)
                if link_key not in seen_links:
                    seen_links.add(link_key)
                    links.append({
                        'source': source_id,
                        'target': target_id,
                        'type': prop_name,
                        'label': prop_name
                    })
    
    # Convert nodes dict to list - keep simple, sorted by ID
    nodes = list(nodes_dict.values())
    nodes.sort(key=lambda x: x['id'])
    
    # Create index mapping: node ID -> array index
    id_to_index = {node['id']: i for i, node in enumerate(nodes)}
    
    # Update links to use array indices
    # 3d-force-graph can reference nodes by index or by matching id field
    # We'll use indices for simplicity
    indexed_links = []
    for link in links:
        src_idx = id_to_index.get(link['source'])
        tgt_idx = id_to_index.get(link['target'])
        if src_idx is not None and tgt_idx is not None:
            indexed_links.append({
                'source': src_idx,
                'target': tgt_idx,
                'type': link['type'],
                'label': link['label']
            })
    
    return {
        'nodes': nodes,
        'links': indexed_links
    }


@app.route('/')
def index():
    """Main route that renders the 3D graph visualization"""
    # Get the path to jaguars.ttl
    ttl_file = os.path.join(os.path.dirname(__file__), 'data', 'jaguars.ttl')
    
    # Parse RDF and convert to graph data
    graph_data = parse_rdf_to_graph_data(ttl_file)
    
    # Convert to JSON for template
    graph_json = json.dumps(graph_data)
    
    return render_template('index.html', graph_data=graph_json)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

