import numpy as np
import matplotlib.pyplot as plt
import math
import time

def generate_cluster_structure(Nc, Nin_per_cluster, Rc):
    # Generate random cluster centers within 1x1 simulation box
    cluster_centers = np.random.rand(Nc, 2)
    
    # Generate random angles and radii for obstacle points
    angles = np.random.uniform(0, 2*np.pi, size=(Nc, Nin_per_cluster))
    radii = np.sqrt(np.random.rand(Nc, Nin_per_cluster)) * Rc
    
    # Compute obstacle coordinates within each cluster
    x_offsets = radii * np.cos(angles)
    y_offsets = radii * np.sin(angles)
    cluster_points = cluster_centers[:, None, :] + np.stack((x_offsets, y_offsets), axis=-1)
    
    # Filter out points lying outside the simulation box
    mask = np.all((cluster_points >= 0) & (cluster_points <= 1), axis=-1)
    cluster_points = cluster_points[mask]
    
    return cluster_points

def main():
    # Input Parameters
    Nc = int(input("Enter the number of cluster centres ")) #2000
    Nin_per_cluster = int(input("Enter the number of obstacles per cluster ")) #5
    Rc = float(input("Enter the critical radius Rc ")) #0.001
    image = int(input("Do you want to see the image type(0/1) "))
    mode = input("If you wish to generate obstacle coordinates for circle rolling type 'cr' and for aerial glide type 'ag' ")
    seed_value = int(input("Enter the seed value ")) #42

    # Seting the seed value for preserving the random coordinates
    np.random.seed(seed_value)

    #Setting the initial time
    t1 = time.time()

    # Generate obstacle coordinates
    obstacle_coordinates = generate_cluster_structure(Nc, Nin_per_cluster, Rc)
    if mode == 'cr':
        np.savetxt(f"cluster{Nin_per_cluster}_{Nc}_{mode}{seed_value}.txt", obstacle_coordinates)
    elif mode == 'ag':
        val = math.radians(float(input("Enter the breaking angle (in degrees) ")))
        dist = np.array([val]*len(obstacle_coordinates))
        obsarr = np.column_stack(((obstacle_coordinates, dist)))
        np.savetxt(f"cluster{Nin_per_cluster}_{Nc}_{mode}{seed_value}.txt", obsarr)

    if image == 1:
        # Visualize obstacle coordinates
        plt.figure(figsize=(8, 8))
        plt.scatter(obstacle_coordinates[:, 0], obstacle_coordinates[:, 1], color='blue', s=5)
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.title('Visualization of Clustered Obstacle Coordinates')
        plt.grid(True)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.savefig(f"cluster{Nin_per_cluster}_{Nc}_{mode}{seed_value}")
        plt.show()
    print(f"Time taken is {time.time()-t1}")

if __name__ == "__main__":
    main()
