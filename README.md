# ECE470_finalproject
 
A robotics project: design, simulate and build a robot which can assemble a simply-designed shelf/furniture automatically.
The Robot is a 6-joint robot arm, UR5. And two sensors are used to stop the conveyor and distinguish colors. when a proximity sensor on the conveyor is triggered, the program will read the data from color sensor. After recognizing color, control part will transmit a message to kinematics part that includes an index which is the one of coordinates list matrices in LUA. This matrix contains all coordinates that will be used in this project. Then inverse kinematics part will calculate joint angles with input coordinates. After that it will set joint angles to reach the expected coordinates with built-in inverse kinematics function.
