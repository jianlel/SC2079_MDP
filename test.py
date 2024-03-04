import math

# Define distances for each character
distances = {
    's': 10,
    'b': 10,
    'd': 10 * math.pi,
    'u': 10 * math.pi,
    'w': 10 * math.pi,
    'v': 10 * math.pi
}

# Given string
data = [('2', 's,s,s,s,s,s,s,s,s,s,s,d,s'), 
        ('1', 'b,v,s,s,s,s,s,s,s,s,s,s,u,u'), 
        ('5', 'v,s,s,s,s,s,s,s,s,s'), 
        ('3', 'v,s,s,s,u,s,s,s,s,u,s,s,s,s,u,b'), 
        ('4', 'd,s')]

# Function to calculate total distance
def calculate_distance(data):
    total_distance = 0
    for count in data:
        stringOfCommands = count[1]
        print(stringOfCommands)
        for char in stringOfCommands.split(','):
            total_distance += distances[char]
    return total_distance

# Calculate total distance
total_distance = calculate_distance(data)
print("Total distance traveled by the robot:", total_distance)