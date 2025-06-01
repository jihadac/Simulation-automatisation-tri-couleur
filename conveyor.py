class Conveyor:
    """
    Goal: Simulate movement of conveyor
    """
    def __init__(self):
        self.running = True
        print("Convoyer created!")
    
    def startConveyor(self):
        self.running = True
        print("Conveyor is running!")
    
    def stopConveyor(self):
        self.running = False
        print("Conveyor stopped!")
