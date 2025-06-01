import array as arr
import random
import time

class Robot:
    def __init__(self):
        self.home_configuration = [0,0,0,0,0,0] # 6DOF, joint_angles of home pose robot. At start, robot is in home configuration
        self.gripper = False # Open gripper
        print("Robot created!")

    def getCurrentPose(self):
        """
        Goal: get the current pose of the robot's end effector (x,y,z,theta) expressed in robot's base frame

        Assume pose is returned in dictionary form: {'x': 1, 'y': 2, 'z': 3, 'theta': 0}
        """
        pose = {'x': 1, 'y': 2, 'z': 3, 'theta': 0} # Dummy values

        print(f"Returning robot's current pose: {pose}")
        return pose
    
    def createPath(self,current_pose,target_pose):
        """
        Goal: compute waypoints/intermediate points robot needs to go through to move from current pose to target pose

        Inputs:
         - current_pose: characterized by x1, y1, z1, theta1 as dictionary: {'x': 1, 'y': 2, 'z': 3, 'theta': 0}
         - target_pose: characterized by x2, y2, z2, theta2 as dictionary: {'x': 1, 'y': 2, 'z': 3, 'theta': 0}

        Call planning solver:
         - Should be taken into account: kinematics robot, joint limits, environment (obstacles, boundaries)
         - In real robotic systems, path planning usually performed using motion planning algorithm
         - Since no obstacles are assumed here, linear interpolation can be applied for simplicity & as an example

        Output:
         - waypoints: list of intermediate points (x, y, z) robot needs to go through to go from current pose to target pose         
        """
        steps = 10
        waypoints = [current_pose]
        for i in range(1,steps+1):
            k = i/steps
            x = round((1-k)*current_pose['x'] + k*target_pose['x'],3)
            y = round((1-k)*current_pose['y'] + k*target_pose['y'],3)
            z = round((1-k)*current_pose['z'] + k*target_pose['z'],3)
            waypoint = {'number':i,'x': x,'y': y, 'z': z, 'theta': target_pose['theta']}  # 'number' only for visualization
            waypoints.append(waypoint)
        
        print(f"Returning waypoints: {waypoints}")
        return waypoints

    def applyInverseKinematics(self,x,y,z,theta):
        """    
        Goal: compute joint angles to reach x, y, z and theta

        Inputs:
         - x, y: position end effector in base frame (z=1 assumed)
         - theta: orientation end effector (rotation around z-axis of base frame)

        Call IK solver
        
        Returns:
         - joint_angles: a list of 6 joint angles (radians or degrees) --> kies zelf wat vision geeft
        """
        
        joint_angles = [0.5,0.5,0.5,0.5,0.5,0.5] # Dummy values

        print(f"Computed joint angles using IK: {joint_angles}")
        return joint_angles

    def move(self,target_pose):
        """
        Goal: move the robot's end effector from current pose to target pose
        
        Joint angles are first computed for every corresponding waypoint. Then movement is made.

        Input:
         - target_pose: x, y, z coordinates & theta angle of target pose in form of dictionary: {'x': 1, 'y': 2, 'z': 3, 'theta': 0}
        """

        waypoints = self.createPath(self.getCurrentPose(),target_pose)
        time.sleep(1)           # for simulation, to visualize results

        joint_trajectory = []   # list of all joint angles
        for pose in waypoints:
            joint_angles = self.applyInverseKinematics(pose['x'],pose['y'],pose['z'],pose['theta'])
            joint_trajectory.append(joint_angles)
            time.sleep(0.5)     # for simulation, to visualize results
        
        for joint_angles in joint_trajectory:
            print(f'Robot moves to pose corresponding to joint angles: {joint_angles}')
            time.sleep(0.5)     # for simulation, to visualize results

    def moveDown(self):
        print('Moving down...')
        pose = self.getCurrentPose()
        pose['z'] -= 0.3        # end effector moves 30cm down --> dummy value!
        self.move(pose)
        print('Moved down!')
        time.sleep(0.5)         # for simulation, to visualize results

    def moveUp(self):
        print('Moving up...')
        pose = self.getCurrentPose()
        pose['z'] += 0.3       # end effector moves 30cm up --> dummy value!
        self.move(pose)
        print('Moved up!')
        time.sleep(0.5)  

    def openGripper(self):
        self.gripper = False
        time.sleep(0.5)        # for simulation, to visualize results
        print('Gripper open!')
    
    def closeGripper(self):
        self.gripper = True
        time.sleep(0.5)        # for simulation, to visualize results
        print('Gripper closed!')

    def verifyPickSuccess(self):
        """
        Goal: simulate whether picking piece was successful
        """
        return random.random() > 0.02  # 98% succes

    def verifyPlaceSuccess(self):
        """
        Goal: simulate whether place was successful
        """
        return random.random() > 0.02  # 98% succes

    def pick(self,target_pose):
        """
        Goal: picking of piece (combines moving to piece + closing gripper) + verifying if picking successfull

        Input:
         - target_pose: x, y, z coordinates & theta angle of target pose in form of dictionary: {'x': 1, 'y': 2, 'z': 3, 'theta': 0}
        """
        
        print('Piece being picked...')
        self.move(target_pose)
        self.closeGripper()
        
        success= self.verifyPickSuccess()
        if success:
            print('Piece is picked!')
        else:
            print('Picking piece failed!')
        return success

    def place(self,pose_color):
        """
        Goal: placing of piece in bin (combines moving robot's end effector above bin, going down, opening gripper and going back up)
        + verifying if placing successfull

        Input:
         - pose_color: x, y, z coordinates & theta angle of robot's pose above the red or blue bin, defined in robot's base frame in form of dictionary: {'x': 1, 'y': 2, 'z': 3, 'theta': 0}
        """
        print('Piece being placed...')        
        self.move(pose_color)
        self.moveDown()
        self.openGripper()

        success = self.verifyPlaceSuccess()
        if success:
            print('Piece is placed!')
        else:
            print('Placing piece failed!')
        self.moveUp()
        
        return success

    def moveHomeJointAngles(self):
        """
        Goal: move robot back to it's home configuration with joint angles in home_configuration  

        Go back to home configuration once every detected piece has been placed.
        """
        print(f"Robot's joint angles put back to home configuration: {self.home_configuration}")
        time.sleep(1)           # for simulation, to visualize results




