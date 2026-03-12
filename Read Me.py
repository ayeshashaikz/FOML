import csv
import copy

# Load CSV data
def load_data(filename):
    with open(filename, 'r') as file:
        data = list(csv.reader(file))
    return data

# Candidate Elimination Algorithm
def candidate_elimination(data):
    
    # Number of attributes
    num_attributes = len(data[0]) - 1
    
    # Initialize S and G
    S = data[1][:-1]   # First positive example
    G = [['?' for i in range(num_attributes)]]
    
    print("Initial S:", S)
    print("Initial G:", G)
    print("--------------------------------------------------")
    
    for row in data[1:]:
        attributes = row[:-1]
        target = row[-1]
        
        if target == "Yes":  # Positive example
            
            # Remove inconsistent hypotheses from G
            G = [g for g in G if all(g[i] == '?' or g[i] == attributes[i] for i in range(num_attributes))]
            
            # Update S
            for i in range(num_attributes):
                if S[i] != attributes[i]:
                    S[i] = '?'
                    
        elif target == "No":  # Negative example
            
            new_G = []
            
            for g in G:
                for i in range(num_attributes):
                    if g[i] == '?':
                        if S[i] != attributes[i]:
                            new_hypothesis = copy.deepcopy(g)
                            new_hypothesis[i] = S[i]
                            new_G.append(new_hypothesis)
            
            G = new_G
        
        print("S:", S)
        print("G:", G)
        print("--------------------------------------------------")
    
    return S, G


# Main Program
data = load_data("Read Me.csv")

final_S, final_G = candidate_elimination(data)

print("\nFinal Specific Hypothesis (S):", final_S)
print("Final General Hypotheses (G):", final_G)
