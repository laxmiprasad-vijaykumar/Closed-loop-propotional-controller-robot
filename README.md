# Closed-loop-propotional-controller-robot
this is a short-project, the goal is to design a closed loop propotional (P) controller, which allows the robot to move to a user specified (x,y) position. the movement happens by using non-holonomic constraints, in which we can control only two DOF of the robot and have limited capablities.
For reaching the position (x,y), a tolerance setting is also given by the user, which corresponds to the euclidean distance between the robot's pose and the final, user-defined (x,y) position , being considered as ''close enough to the goal'' .
