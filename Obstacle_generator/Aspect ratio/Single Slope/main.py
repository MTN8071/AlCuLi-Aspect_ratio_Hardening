import numpy as np
import matplotlib.pyplot as plt
import math
import time

def generate_points(start_point, slope, spacing, num_points):
    delta_x = spacing * np.cos(np.radians(slope))
    delta_y = spacing * np.sin(np.radians(slope))
    x_coords = np.cumsum([start_point[0]] + [delta_x] * (num_points - 1))
    y_coords = np.cumsum([start_point[1]] + [delta_y] * (num_points - 1))
    # Filter out points that lie within the range (0, 1)
    mask = (x_coords >= 0) & (x_coords <= 1) & (y_coords >= 0) & (y_coords <= 1)
    x_coords = x_coords[mask]
    y_coords = y_coords[mask]
    points = np.column_stack((x_coords, y_coords))
    return points

def generate_obstacle_lines(num_lines, num_points_per_line, slope, spacing):
    obstacle_lines = []
    exclusion_radius = 2 * spacing
    exclusion_zones = np.zeros((num_lines, 2))
    for i in range(num_lines):
        while True:
            start_point = np.random.rand(2)
            if np.all(np.linalg.norm(exclusion_zones[:i] - start_point, axis=1) > exclusion_radius):
                break
        obstacle_line = generate_points(start_point, slope, spacing, num_points_per_line)
        obstacle_lines.append(obstacle_line)
        exclusion_zones[i] = obstacle_line.mean(axis=0)
    return obstacle_lines

def main():
    # Input Parameters
    num_lines = round(float(input("Enter number of precipitates lines "))) # 400
    num_points_per_line = round(float(input("Enter the aspect ratio "))) # 4
    slope = round(float(input("Enter the slope of precipitates line on your glide plane (in degrees) "))) # 60
    image = int(input("Do you want to see the image type (0/1) "))
    mode = input("If you wish to generate obstacle coordinates for circle rolling type 'cr' and for aerial glide type 'ag' ")
    seed_value = int(input("Enter seed value ")) # 42
    spacing = 1/70

    # Setting up the seed value
    np.random.seed(seed_value)

    # Setting the initial time
    t_initial = time.time()

    # Generate obstacle lines
    obstacle_lines = np.concatenate(generate_obstacle_lines(num_lines, num_points_per_line, slope, spacing))

    if mode == 'cr':
        np.savetxt(f"aspect{num_points_per_line}_{slope}_{num_lines}_{mode}{seed_value}.txt", obstacle_lines)
    elif mode == 'ag':
        val = math.radians(float(input("Enter the breaking angle (in degrees) ")))
        dist = np.array([val]*len(obstacle_lines))
        obsarr = np.column_stack(((obstacle_lines, dist)))
        np.savetxt(f"aspect{num_points_per_line}_{slope}_{num_lines}_{mode}{seed_value}.txt", obsarr)

    if image == 1:
        plt.figure(figsize=(8, 6))
        plt.plot(obstacle_lines[:, 0], obstacle_lines[:, 1], marker='o', ms=3, linestyle='', color='blue')
        plt.title('Obstacle Lines with Closely Spaced Points within Boundary')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.savefig(f"aspect{num_points_per_line}_{slope}_{num_lines}_{seed_value}.png")
        plt.show()

    print(f"Time taken to execute the code is {time.time()-t_initial}")

if __name__ == "__main__":
    main()
