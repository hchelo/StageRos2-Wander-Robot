# StageRos2-Wander-Robot
![Descripción de la imagen](stage1.png)
# Instrucciones para ejecutar el proyecto

1. **Run the Stage Ros2**:
   ros2 launch stage_ros2 stage.launch.py world:=cave enforce_prefixes:=false one_tf_tree:=true

2. **Create the SLAM**:
  ros2 launch navigation_tb3 mapping.launch.py

3. **Visualize the SLAM**:
  rviz2 src/navigation_tb3/config/mapping.rviz

4. **Run the Wander Algorithm**:
  python3 src/controlador/pioneer_behavior10.py 
