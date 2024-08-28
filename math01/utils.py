import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def visualize_configuration(screen, observer, point):

    # Create a figure and a 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # define faces
    faces = [screen] 

    # plot objects
    ax.add_collection3d(Poly3DCollection(faces, 
                                         facecolors='cyan', 
                                         linewidths=1, 
                                         edgecolors='r', 
                                         alpha=.5))

    # Plot the line connecting the vertex (Point D) with the arbitrary point
    ax.plot([observer[0], point[0]],
            [observer[1], point[1]],
            [observer[2], point[2]], color='black', linestyle='-.', linewidth=1)


    # Set the labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Show the plot
    plt.show()

