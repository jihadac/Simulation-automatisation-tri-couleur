############# Test technique - Simulation projet robotique (automatisation d’un tri couleur) #############
import time
import conveyor as c
import robot as r
import input_vision as vision

def conversionReferenceFrame(piece):
    print('Piece expressed with respect to base frame robot.')
    return piece                 # in reality coordinates piece after transformation from camera frame to base frame robot

def main():

    ### PARAMETERS ###
    TIMEOUT = 2                  # seconds to wait after last piece detection
    MAX_WAIT_TIME = 4            # max wait from first detection before forcing stop
    MIN_PIECES = 3               # stop conveyor if 3 or more pieces detected
    first_detection_time = None  # time when first piece of current batch detected
    last_detection_time = None   # time when last piece was detected
    stored_pieces = []           # store detected pieces waiting to be picked

    pose_red = {'x':0,'y':-0.5,'z':0.5,'theta':0}  # defined in robot's base frame
    pose_blue = {'x':0,'y':0.5,'z':0.5,'theta':0}  # defined in robot's base frame

    ### INSTANCES ###
    conveyor = c.Conveyor() #Conveyor starts running!
    robot = r.Robot()

    while True:                  # continuous operation

        time.sleep(2)            # for simulation, to visualize results

        detected_pieces = vision.detect_pieces()
        now = time.time()

        if detected_pieces:
            stored_pieces.extend(detected_pieces)
            last_detection_time = now
            if first_detection_time is None:
                first_detection_time = now
            
            print(f"Detected {len(detected_pieces)} pieces: \n {stored_pieces}")

        
        if conveyor.running:
            if len(stored_pieces) >= MIN_PIECES:
                conveyor.stopConveyor()
                print('Reason: number of detected pieces >= 3')
            elif stored_pieces and (now-last_detection_time)>TIMEOUT:
                conveyor.stopConveyor()
                print('Reason: timeout exceeded')
            elif stored_pieces and first_detection_time and (now-first_detection_time)>MAX_WAIT_TIME:
                conveyor.stopConveyor()
                print('Reason: max wait time exceeded')

            time.sleep(0.5)      # for simulation, to visualize results

        if not conveyor.running:
            counter = 0          # for simulation, to visualize results
            for piece in stored_pieces:
                print(f"Remaining number of pieces to be placed: {len(stored_pieces)-counter}")
                piece = conversionReferenceFrame(piece)
                success = robot.pick(piece)
                time.sleep(3)    # for simulation, to visualize results
                if not success:
                    counter += 1
                    print("Skipping placement piece due to pick failure.")
                    continue
                if(piece['label'] == 'red'):
                    print('Target: red container')
                    robot.place(pose_red)
                elif(piece['label'] == 'blue'):
                    print('Target: blue container')
                    robot.place(pose_blue)
                counter += 1
                time.sleep(3)    # for simulation, to visualize results
            stored_pieces.clear()
            print('No more stored pieces...')
            robot.moveHomeJointAngles()
            first_detection_time = None
            last_detection_time = None
            conveyor.startConveyor()

if __name__ == "__main__":
    main()