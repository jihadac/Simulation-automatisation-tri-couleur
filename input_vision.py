import random

"""
Goal: Simulate detection of 0–4 random pieces

- Detected pieces stored in a list of dictionaries  
- Dictionary in form of {'id':1, 'x': 0.1, 'y': 0.2, 'z': 0.3, 'theta': 0.4, 'label': 'blue' | 'red'}
- Distances in [m], angles in [rad]
- Precision: 0.001 (both for distance and angle)
- Update frequency: 5Hz

"""
def detect_pieces():
    
    COLORS = ["red","blue"]
    number_of_pieces = random.choice([0, 1, 2, 3, 4])
    detected_pieces = []

    for i in range(number_of_pieces):
        piece = {'id': i,
                 'x':round(random.uniform(-0.2, 0.2), 3), # Conveyor width approx 0.2 m
                 'y':round(random.uniform(0.0, 0.3), 3), # Conveyor length approx 0.0 to 0.3 m
                'z':1, # Fixed height Z (camera height above conveyor)
                'theta': round(random.random(), 3),
                'label': random.choice(COLORS)
                }
        detected_pieces.append(piece)
    
    return detected_pieces


"""
while geen pieces detected of (<3pieces && tijd <3s)
camera blijft trekken

"""

