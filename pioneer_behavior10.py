#!/usr/bin/env python

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time
import random

class PioneerObstacleAvoidance(Node):
    '''
    Un nodo de ROS 2 para monitorear datos de escaneo láser y evitar obstáculos solo en los sectores izquierdo y derecho.
    '''
    def __init__(self):
        super().__init__('pioneer_obstacle_avoidance')

        # Crear un publicador para controlar el movimiento del robot
        self.pub_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Comportamiento de evitación de obstáculos iniciado!')

        # Suscribirse al tema /base_scan para obtener los datos del escáner láser
        self.create_subscription(LaserScan, "/base_scan", self.laser_callback, 10)

        # Estado para gestionar el giro de 189 grados cuando el robot está trabado
        self.is_stuck = False

    def laser_callback(self, msg):
        '''
        Esta función se ejecuta cada vez que se recibe un mensaje de LaserScan.
        '''
        ranges = msg.ranges
        total_points = len(ranges)

        # Determinar los índices para cada sector (izquierda y derecha)
        left_start_index = int(total_points * (220 / 360))  # 220 grados
        left_end_index = int(total_points * (230 / 360))    # 230 grados
        right_start_index = int(total_points * (130 / 360)) # 130 grados
        right_end_index = int(total_points * (140 / 360))   # 140 grados

        # Obtener las distancias mínimas en cada sector
        min_left = min(ranges[left_start_index:left_end_index + 1])
        min_right = min(ranges[right_start_index:right_end_index + 1])

        # Registrar distancias mínimas para depuración
        self.get_logger().info(f'Min Izquierda: {min_left:.2f}, Min Derecha: {min_right:.2f}')

        # Tomar decisiones de movimiento basadas en las distancias
        self.decide_movement(min_left, min_right)

    def decide_movement(self, min_left, min_right):
        '''
        Controla el movimiento del robot en función de las distancias de los sectores izquierdo y derecho.
        '''
        twist_msg = Twist()
        twist_msg.linear.x = 0.0
        twist_msg.angular.z = 0.0
        tope=1.0

        # Lógica de decisión
        if min_left > tope and min_right > tope:
            self.get_logger().info('ADELANTE...')
            twist_msg.linear.x = 0.2      # Avanza
            numero_randomico = random.uniform(-0.3, 0.3)
            twist_msg.angular.z = numero_randomico  # Gira a la izquierda
            print(numero_randomico)

        elif min_right < tope and min_left < tope:
            self.get_logger().info('Atras...')
            twist_msg.linear.x = 0.0  # Avanza
            twist_msg.angular.z = 1.5  # Gira a la izquierda

        elif min_left < tope and min_right > tope:
            self.get_logger().info('Derecha...')
            twist_msg.linear.x = -0.01  # Avanza
            twist_msg.angular.z = -0.1  # Gira a la derecha

        elif min_right < tope and min_left > tope:
            self.get_logger().info('Izquierda...')
            twist_msg.linear.x = -0.01  # Avanza
            twist_msg.angular.z = 0.1  # Gira a la izquierda

        self.pub_cmd_vel.publish(twist_msg)
        time.sleep(1.5)

    def reset_stuck_state(self):
        '''
        Función de callback para restablecer el estado de "trabado" después de completar el giro.
        '''
        twist_msg = Twist()
        twist_msg.angular.z = 0.0  # Detener el giro
        twist_msg.linear.x = 0.0   # Asegurar que no haya movimiento de avance
        self.pub_cmd_vel.publish(twist_msg)  # Publicar el mensaje de parada

        self.is_stuck = False
        self.get_logger().info('Estado de trabado restablecido, reanudando comportamiento normal.')

    def run_behavior(self):
        '''
        Bucle principal que mantiene el nodo activo y procesa callbacks.
        '''
        rclpy.spin(self)  # Mantener el nodo activo

def main(args=None):
    rclpy.init(args=args)  # Inicializar ROS 2
    node = PioneerObstacleAvoidance()  # Crear el nodo
    node.run_behavior()  # Ejecutar el comportamiento
    node.destroy_node()  # Limpiar el nodo después de la ejecución
    rclpy.shutdown()  # Apagar ROS 2

if __name__ == '__main__':
    main()
