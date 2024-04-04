import numpy as np
import matplotlib.pyplot as plt
import math
import time


# Function to generate points on a line with a given slope and spacing within the boundary
def generate_points(start_point, slope, spacing, num_points):
    points = np.zeros((num_points, 2))
    points[0] = start_point
    delta_x = spacing * np.cos(np.radians(slope))
    delta_y = spacing * np.sin(np.radians(slope))
    for i in range(1, num_points):
        new_x = points[i-1, 0] + delta_x
        new_y = points[i-1, 1] + delta_y
        if 0 <= new_x <= 1 and 0 <= new_y <= 1:  # Check if new point is within boundary
            points[i, 0] = new_x
            points[i, 1] = new_y
        else:
            break  # Stop generating points if line crosses boundary
    return points[:i+1]  # Return only the points within boundary

# Function to check if two line segments intersect
def check_intersection(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[-1]
    x3, y3 = line2[0]
    x4, y4 = line2[-1]
    
    dx12 = x2 - x1
    dy12 = y2 - y1
    dx34 = x4 - x3
    dy34 = y4 - y3
    
    denominator = (dy12 * dx34 - dx12 * dy34)
    
    if denominator == 0:
        return False  # Parallel lines, no intersection
    
    t1 = ((x1 - x3) * dy34 + (y3 - y1) * dx34) / denominator
    t2 = ((x3 - x1) * dy12 + (y1 - y3) * dx12) / (-denominator)
    
    return (0 <= t1 <= 1) and (0 <= t2 <= 1)

# Generate obstacle lines with random start points and slopes, avoiding intersections
def generate_obstacle_lines(num_lines, num_points_per_line, slopes, spacing):
    obstacle_lines = []
    exclusion_radius = 2 * spacing  # Radius of exclusion zone around each obstacle line
    exclusion_zones = []  # List to store exclusion zones for each obstacle line
    
    for _ in range(num_lines):
        while True:
            # Generate a random start point in the 1x1 2D plane
            start_point = np.random.rand(2)
            
            # Randomly select a slope from the given list of slopes
            slope = np.random.choice(slopes)
            
            # Generate the closely spaced points for the obstacle line
            new_line = generate_points(start_point, slope, spacing, num_points_per_line)
            
            # Check for intersections with existing lines
            if all(not check_intersection(new_line, line) for line in obstacle_lines):
                break  # No intersection found, exit loop
            
        # Update exclusion zones with the circle around the new obstacle line
        exclusion_zones.append(new_line.mean(axis=0))
        obstacle_lines.append(new_line)
        
    return obstacle_lines

def main():
    num_lines = round(float(input("Enter number of precipitates lines ")))
    num_points_per_line = round(float(input("Enter the aspect ratio "))) 
    image = int(input("Do you want to see the image type (0/1) "))
    mode = input("If you wish to generate obstacle coordinates for circle rolling type 'cr' and for aerial glide type 'ag' ")
    seed_value = int(input("Enter seed value ")) # 42
    spacing = 1/70

    # Setting up the seed value
    np.random.seed(seed_value)

    # Setting the initial time
    t_initial = time.time()

    # List of slopes in degrees
    slopes = [60, 0, -60]

    # Generate obstacle lines with random start points and slopes, avoiding intersections
    obstacle_lines = np.concatenate(generate_obstacle_lines(num_lines, num_points_per_line, slopes, spacing))
    if mode =='cr':
        np.savetxt(f'aspect{num_points_per_line}_multi_{num_lines}_{mode}{seed_value}.txt',obstacle_lines)
    elif mode=='ag':
        val = math.radians(float(input("Enter the breaking angle (in degrees) ")))
        dist = np.array([val]*len(obstacle_lines))
        obsarr = np.column_stack(((obstacle_lines, dist)))
        np.savetxt(f"aspect{num_points_per_line}_multi_{num_lines}_{mode}{seed_value}.txt", obsarr)


    # Plot the concatenated array of obstacle lines
    if image==1:
        plt.figure(figsize=(8, 6))
        plt.plot(obstacle_lines[:, 0], obstacle_lines[:, 1], marker='o', ms=3, linestyle='', color='blue')
        plt.title('Obstacle Lines with Closely Spaced Points within Boundary')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.xlim(0, 1)  # Set x-axis limits to [0, 1]
        plt.ylim(0, 1)  # Set y-axis limits to [0, 1]
        plt.gca().set_aspect('equal', adjustable='box')  # Ensure aspect ratio is equal
        plt.savefig(f"aspect{num_points_per_line}_multi_{num_lines}_{seed_value}.png")
        plt.show()
        
    print(f"Time taken to execute the code is {time.time()-t_initial}")
    
if __name__ == "__main__":
    main()    
    
