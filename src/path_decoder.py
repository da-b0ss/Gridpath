import numpy as np

def reconstruct_path(start_node: int, end_node: int, predecessors: np.ndarray) -> list[int]:
    """
    Reconstructs the full path from a start_node to an end_node
    using the Scipy-style predecessor matrix.
    """
    path = [end_node]
    current = end_node
    
    # Loop until we backtrack to the start_node
    # The predecessor for the start_node itself is -9999
    while current != start_node:
        current = predecessors[start_node, current]
        
        if current == -9999:
            # This means no path exists, which shouldn't happen
            print(f"Error: No path found from {start_node} to {end_node}")
            return [] 
            
        path.append(current)
    
    # The path is built backward (end -> start), so reverse it
    return path[::-1]