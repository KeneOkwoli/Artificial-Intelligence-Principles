# CircuitPython code for controlling servos with PCA9685 on a Raspberry Pi Pico
import board
import busio
import time
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Initialize I2C bus using GP21 for SCL and GP20 for SDA
i2c = busio.I2C(board.GP21, board.GP20)  # SCL, SDA pins on the Pico
# Initialize the PCA9685 using the default address (0x40)
pca = PCA9685(i2c)
pca.frequency = 50  # Set the PWM frequency to 50Hz (good for servos)

# Define all servo channel assignments
servo_channels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

# Create a dictionary to store servo objects with meaningful names - initialized directly
servo_dict = {
    "left_wing": servo.Servo(pca.channels[0]),   # channel 0
    "right_wing": servo.Servo(pca.channels[1]),  # channel 1
    "servo11": servo.Servo(pca.channels[2]),     # channel 2
    "servo12": servo.Servo(pca.channels[3]),     # channel 3
    "servo9": servo.Servo(pca.channels[4]),      # channel 4
    "servo1": servo.Servo(pca.channels[5]),      # channel 5
    "servo10": servo.Servo(pca.channels[6]),     # channel 6
    "servo2": servo.Servo(pca.channels[7]),      # channel 7
    "servo8": servo.Servo(pca.channels[8]),      # channel 8
    "servo7": servo.Servo(pca.channels[9]),      # channel 9
    "servo4": servo.Servo(pca.channels[10]),     # channel 10
    "servo3": servo.Servo(pca.channels[11]),     # channel 11
    "servo5": servo.Servo(pca.channels[12]),     # channel 12
    "servo6": servo.Servo(pca.channels[13]),      # channel 13
    "head": servo.Servo(pca.channels[14])      # channel 14
}

# Function to set angle for a specific servo by name
def set_servo_by_name(servo_name, angle):
    if servo_name in servo_dict and servo_dict[servo_name] is not None:
        if 0 <= angle <= 180:
            servo_dict[servo_name].angle = angle
            return True
    return False

# Function to move two servos at the same time
def left_body_servos(servo_name1, angle1, servo_name2, angle2, servo_name3, angle3):
    
    if servo_name1 in servo_dict and servo_dict[servo_name1] is not None:
        if 0 <= angle1 <= 180:
            servo_dict[servo_name1].angle = angle1
            
    if servo_name2 in servo_dict and servo_dict[servo_name2] is not None:
        if 0 <= angle2 <= 180:
            servo_dict[servo_name2].angle = angle2
            
    if servo_name3 in servo_dict and servo_dict[servo_name3] is not None:
        if 0 <= angle3 <= 180:
            servo_dict[servo_name3].angle = angle3
            

def left_joint_servos(servo_name1, angle1, servo_name2, angle2, servo_name3, angle3):
    
    if servo_name1 in servo_dict and servo_dict[servo_name1] is not None:
        if 0 <= angle1 <= 180:
            servo_dict[servo_name1].angle = angle1
            
    if servo_name2 in servo_dict and servo_dict[servo_name2] is not None:
        if 0 <= angle2 <= 180:
            servo_dict[servo_name2].angle = angle2
            
    if servo_name3 in servo_dict and servo_dict[servo_name3] is not None:
        if 0 <= angle3 <= 180:
            servo_dict[servo_name3].angle = angle3

            
            
def right_body_servos(servo_name1, angle1, servo_name2, angle2, servo_name3, angle3):
    
    if servo_name1 in servo_dict and servo_dict[servo_name1] is not None:
        if 0 <= angle1 <= 180:
            servo_dict[servo_name1].angle = angle1
            
    if servo_name2 in servo_dict and servo_dict[servo_name2] is not None:
        if 0 <= angle2 <= 180:
            servo_dict[servo_name2].angle = angle2
            
    if servo_name3 in servo_dict and servo_dict[servo_name3] is not None:
        if 0 <= angle3 <= 180:
            servo_dict[servo_name3].angle = angle3

            
def right_joint_servos(servo_name1, angle1, servo_name2, angle2, servo_name3, angle3):
    
    if servo_name1 in servo_dict and servo_dict[servo_name1] is not None:
        if 0 <= angle1 <= 180:
            servo_dict[servo_name1].angle = angle1
            
    if servo_name2 in servo_dict and servo_dict[servo_name2] is not None:
        if 0 <= angle2 <= 180:
            servo_dict[servo_name2].angle = angle2
            
    if servo_name3 in servo_dict and servo_dict[servo_name3] is not None:
        if 0 <= angle3 <= 180:
            servo_dict[servo_name3].angle = angle3
            
# Function to move wing servos in opposite directions
def move_wings(angle):
    if 0 <= angle <= 180:
        servo_dict["left_wing"].angle = angle
        servo_dict["right_wing"].angle = 180 - angle
        return True
    return False

def rest_pos_servos(servo_name1, angle1, servo_name2, angle2):
    
    if servo_name1 in servo_dict and servo_dict[servo_name1] is not None:
        if 0 <= angle1 <= 180:
            servo_dict[servo_name1].angle = angle1
            
    if servo_name2 in servo_dict and servo_dict[servo_name2] is not None:
        if 0 <= angle2 <= 180:
            servo_dict[servo_name2].angle = angle2
            
            
def robot_rest():
    print("robot resetting")
    rest_pos_servos("servo1", 90, "servo2", 0)
    rest_pos_servos("servo3", 90, "servo4", 0)
    rest_pos_servos("servo5", 90, "servo6", 0)
    rest_pos_servos("servo7", 90, "servo8", 0)
    rest_pos_servos("servo9", 90, "servo10", 0)
    rest_pos_servos("servo11", 90, "servo12", 0)
    time.sleep(20)
    
def move_reset():
    rest_pos_servos("servo1", 90, "servo2", 0)
    rest_pos_servos("servo3", 90, "servo4", 0)
    rest_pos_servos("servo5", 90, "servo6", 0)
    rest_pos_servos("servo7", 90, "servo8", 0)
    rest_pos_servos("servo9", 90, "servo10", 0)
    rest_pos_servos("servo11", 90, "servo12", 0)
    time.sleep(20)
    
def servo_test(servo_name1, angle1, servo_name2, angle2, servo_name3, angle3, servo_name4, angle4, servo_name5, angle5, servo_name6, angle6,
               servo_name7, angle7, servo_name8, angle8, servo_name9, angle9, servo_name10, angle10, servo_name11, angle11, servo_name12, angle12):
    
    if servo_name1 in servo_dict and servo_dict[servo_name1] is not None:
        if 0 <= angle1 <= 180:
            servo_dict[servo_name1].angle = angle1
            
    if servo_name2 in servo_dict and servo_dict[servo_name2] is not None:
        if 0 <= angle2 <= 180:
            servo_dict[servo_name2].angle = angle2
            
    if servo_name3 in servo_dict and servo_dict[servo_name3] is not None:
        if 0 <= angle3 <= 180:
            servo_dict[servo_name3].angle = angle3
            
    if servo_name4 in servo_dict and servo_dict[servo_name4] is not None:
        if 0 <= angle4 <= 180:
            servo_dict[servo_name4].angle = angle4
            
    if servo_name5 in servo_dict and servo_dict[servo_name5] is not None:
        if 0 <= angle5 <= 180:
            servo_dict[servo_name5].angle = angle5
            
    if servo_name6 in servo_dict and servo_dict[servo_name6] is not None:
        if 0 <= angle6 <= 180:
            servo_dict[servo_name6].angle = angle6

    if servo_name7 in servo_dict and servo_dict[servo_name7] is not None:
        if 0 <= angle7 <= 180:
            servo_dict[servo_name7].angle = angle7
            
    if servo_name8 in servo_dict and servo_dict[servo_name8] is not None:
        if 0 <= angle8 <= 180:
            servo_dict[servo_name8].angle = angle8
            
    if servo_name9 in servo_dict and servo_dict[servo_name9] is not None:
        if 0 <= angle9 <= 180:
            servo_dict[servo_name9].angle = angle9
            
    if servo_name10 in servo_dict and servo_dict[servo_name10] is not None:
        if 0 <= angle10 <= 180:
            servo_dict[servo_name10].angle = angle10
            
    if servo_name11 in servo_dict and servo_dict[servo_name11] is not None:
        if 0 <= angle11 <= 180:
            servo_dict[servo_name11].angle = angle11
            
    if servo_name12 in servo_dict and servo_dict[servo_name12] is not None:
        if 0 <= angle12 <= 180:
            servo_dict[servo_name12].angle = angle12
            
# try:
#     print("Testing I2C connection to PCA9685...")
#     pca.frequency = 50
#     print("PCA9685 found and initialized!")
#     
#     # Example: Move just the wings to 90 degrees (center position)
#     print("Moving wings to center position")
#     set_servo_by_name("left_wing", 90)
#     set_servo_by_name("right_wing", 90)
#     time.sleep(1)
#     
# #     # Example: Flap wings only
# #     print("Flapping wings")
# #     for angle in range(45, 180, 10):
# #         move_wings(angle)
# #         time.sleep(0.05)
# #     
# #     # Example: Move a single specific servo
# #     print("Moving servo1 to different positions")
# #     set_servo_by_name("servo1", 45)
# #     time.sleep(1)
# #     set_servo_by_name("servo1", 135)
# #     time.sleep(1)
# #     set_servo_by_name("servo1", 90)  # Back to center
#     
#     # Detach all servos (stop sending signal)
#     left_servos("head", 10, "servo5", 10, "servo9", 170)
#     time.sleep(1)
#     right_servos("head", 10, "servo5", 10, "servo9", 170)
#     time.sleep(1)
  
def starting_movement():
    print("setting position for movement")
    servo_test("servo2", 0, "servo4", 0, "servo6", 0, "servo8", 0, "serv10", 0, "servo12", 0, "servo1", 150, "servo3", 30, "servo5", 90, "servo7", 150, "servo9", 30, "servo11", 90) # position 0
    
def move_forward():
    test = 1
    while (test == 1):
        print("moving forward")
        time.sleep(0.5)
        servo_test("servo2", 180, "servo4", 0, "servo6", 180, "servo8", 0, "serv10", 180, "servo12", 0, "servo1", 150, "servo3", 0, "servo5", 90, "servo7", 30, "servo9", 30, "servo11", 150) # position 1
        time.sleep(0.5)
#         servo_test("servo2", 0, "servo4", 0, "servo6", 0, "servo8", 0, "serv10", 0, "servo12", 0, "servo1", 150, "servo3", 0, "servo5", 90, "servo7", 30, "servo9", 30, "servo11", 150)# positition 2
#         time.sleep(0.5)
#         servo_test("servo2", 0, "servo4", 180, "servo6", 0, "servo8", 180, "serv10", 0, "servo12", 180, "servo1", 180, "servo3", 0, "servo5", 30, "servo7", 30, "servo9", 150, "servo11", 150) # position 3
#         time.sleep(0.5)
#         servo_test("servo2", 0, "servo4", 0, "servo6", 0, "servo8", 0, "serv10", 0, "servo12", 0, "servo1", 150, "servo3", 0, "servo5", 30, "servo7", 30, "servo9", 150, "servo11", 150) # position 4
#         time.sleep(0.5)
#         servo_test("servo2", 0, "servo4", 0, "servo6", 0, "servo8", 0, "serv10", 0, "servo12", 0, "servo1", 150, "servo3", 30, "servo5", 90, "servo7", 150, "servo9", 30, "servo11", 90) # position 5
#         time.sleep(0.5)
    
    
    
#     servo_test("servo1", 10, "servo5", 130, "servo9", 10)
#     time.sleep(0.5)
#     servo_test("servo2", 0, "servo6", 0, "servo10", 0)
#     time.sleep(0.5)
#     servo_test("servo1", 130, "servo5", 10, "servo9", 130)
#     time.sleep(0.5)
#     
#     servo_test("servo4", 130, "servo8", 130, "servo12", 130)
#     time.sleep(2)
#     servo_test("servo3", 130, "servo7", 10, "servo11", 130)
#     time.sleep(2)
#     servo_test("servo4", 0, "servo8", 0, "servo12", 0)
#     time.sleep(2)
#     servo_test("servo3", 10, "servo7", 130, "servo11", 10)
#     time.sleep(2)    
#     
#right_joint_servos("servo8", 0, "servo10", 0, "servo12", 0)

starting_movement()
#move_forward()
#robot_rest()

# rest_pos_servos("servo10", 0, "servo11", 180)
# time.sleep(1)
# rest_pos_servos("servo10", 180, "servo11", 180)
# time.sleep(1)
#testing_servo()

# except KeyboardInterrupt:
#     print("Program stopped")
#     for servo_name in servo_dict:
#         if servo_dict[servo_name] is not None:
#             servo_dict[servo_name].angle = None
# except Exception as e:
#     print(f"Error: {e}")
#     print("Check your connections and make sure the PCA9685 is properly connected to GP20 (SDA) and GP21 (SCL).")
#     try:
#         for servo_name in servo_dict:
#             if servo_dict[servo_name] is not None:
#                 servo_dict[servo_name].angle = None
#     except:
#         pass