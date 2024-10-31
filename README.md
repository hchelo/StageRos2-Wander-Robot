# StageRos2-Wander-Robot
![Descripción de la imagen](stage1.png)
# Instrucciones para ejecutar el proyecto

1. **Correr el stage**:
   ros2 launch stage_ros2 stage.launch.py world:=cave enforce_prefixes:=false one_tf_tree:=true

2. **Elaborar el SLAM: Ejecuta el siguiente comando**:
  ros2 launch navigation_tb3 mapping.launch.py

3. **Visualizar el SLAM: Abre RViz con el siguiente comando**:
  rviz2 src/navigation_tb3/config/mapping.rviz

4. **Correr el algoritmo wander: Ejecuta el siguiente comando**:
  python3 src/controlador/pioneer_behavior10.py 
