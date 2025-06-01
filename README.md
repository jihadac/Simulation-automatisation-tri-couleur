# Simulation automatisation d'un tri couleur
## Project Description

This project simulates the automated sorting of red and blue parts arriving in a mixed flow on a motorized conveyor. The parts are similar in size and shape, placed in a single layer without overlap. A Techman TM25S robotic arm is installed next to the conveyor. A color camera provides a zenithal view of the scene.

The goal is to design and implement a simulated or partial robotic solution able to detect pieces, classify them by color, and place them into the correct bin focusing on pick-and-place logic and sequencing of actions.

## Assumptions

- Detected pieces stored as a list of dictionaries, e.g.:  
  `{'id': 1, 'x': 0.1, 'y': 0.2, 'z': 0.3, 'theta': 0.4, 'label': 'blue'}`  
- Distances in meters [m], angles in radians [rad]  
- Precision of 0.001 for both distance and angle  
- Update frequency approximately 5 Hz  
- Conveyor and robot base assumed to be at the same height  
- Dummy values used for simulation
- Pick/place failures simulated to mimic real-world exceptions (label (=color) assumed to be always correct)
- Camera coordinates transformed into robot’s base frame using a known transformation matrix (simulated) to express everything wrt robot's base frame
- Time delays are used for readability of logs and roughly simulate real motion times

## Code Structure

### `main.py`

- Initialize robot and conveyor  
- Main loop:  
  - Receive input from vision system  
    - If number of detected pieces ≥ `MIN_PIECES` → stop conveyor  
    - If time since last detection > `TIMEOUT` → stop conveyor  
    - If total time since first detection > `MAX_WAIT_TIME` → stop conveyor  
  - For each detected piece:  
    - Convert coordinates from camera reference frame to robot base frame  
    - Execute `pick(piece)`  
      - If success → execute `place(piece)`  
        - If label == red → place in red container  
        - If label == blue → place in blue container  
      - Else → skip placement  
  - When no pieces remain:  
    - Restart conveyor  
    - Move robot to home position  
  - Repeat loop  

### `pick(piece)`

- Move from current pose to target pick pose  
  - Generate waypoints using linear interpolation  
  - Convert waypoints to joint angles using inverse kinematics (IK) solver  
  - Execute movement  
- When at pick location → close gripper  
- Check if grip was successful  
 - If yes → Return success
 - If no → Return failure
 
### `place(piece)`

- Move from current pose to target place pose (= (well) above red or blue container)  
  - Generate waypoints using linear interpolation  
  - Convert waypoints to joint angles using IK solver  
  - Execute movement  
- When above container → move down slightly (to get closer to the edge height of container)
- Open gripper  
- Check if release was successful  
- Move slightly upward again

## Current Limitations

- No `config.py`: all parameters are hardcoded within scripts  
- Conveyor simulated as stopped during picking; no "pick-on-the-fly" functionality  
- No real calibration between camera and robot  
- Inverse kinematics is simulated (no real IK solver used)  

## Future Improvements

- Implement "pick-on-the-fly" (picking parts while conveyor is moving) which requires:  
  - Higher update frequency 
  - Accurate motion prediction  
  - Tighter real-time control  

- Add a `config.py` to centralize and easily modify parameters  
- Integrate with a real robot and calibrated camera system  

## How to Run

1. Ensure Python 3.x is installed  
2. Run the main simulation script:  
   python main.py

## Visualizations

Scene images were created with Figma.


