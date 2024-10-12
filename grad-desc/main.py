import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation 
from matplotlib.animation import PillowWriter
from Gradient_Descent import f
import pickle
args = {
    'f': f, 'paths' :0 
}

def creat_animation(f, paths, minimum,
                     x_lim, y_lim,
                     colors, labels, n_seconds=7,
                       figsize = (14,16)):
    try :
        path_length = max(len(path) for path in paths)
        n_points = 300
        x = np.linspace(*x_lim, n_points)
        y = np.linspace(*y_lim, n_points)
        X, Y = np.meshgrid(x, y)
        Z = f([X,Y])
        fig, ax = plt.subplots(figsize=figsize)
        ax.contour(X, Y, Z, 90, cmap="jet")
        scatters = [ax.scatter(None,
                            None,
                            label=label,
                            c=c) for c, label in zip(colors, labels)]
        ax.legend(prop={"size": 25})
        
        ax.plot(*minimum, "rD")
        #ax.plot(optimal_points[:,0], optimal_points[:,1], colors)
        
        def animate(i):
            for path, scatter in zip(paths, scatters):
                scatter.set_offsets(path[:i, :])

            ax.set_title(str(i))
        ms_per_frame = 1000 * n_seconds / path_length
        anim = FuncAnimation(fig, animate, frames=path_length, interval=ms_per_frame)
        plt.show()
    except Exception as e :
        print(e)
    return anim
if __name__ == "__main__":
    pickle_filename = 'data.pkl'

    # Read the data from the Pickle file
    with open(pickle_filename, 'rb') as pickle_file:
        data = pickle.load(pickle_file)

    labels = list(data.keys())
    paths =[
        list(list(data.values())[0].values())[0], 
        list(list(data.values())[1].values())[0]
        ] 
    
    optimal_points = [
        paths[0][-1],
        paths[1][-1]
        ]
    paths[ 0] = np.array(list(paths[0][:1000:10]) + list(paths[0][1000::100]))
    colors = ['y', 'b']
    minimum = (1,1)
    x_lim, y_lim = (-4,4),(-4,4)
    print(f"for Gradient Descent with pas optimal |  x* = {optimal_points[0]} | number of iteration is = {len(paths[0])}")
    print(f"for Gradient Descent with pas optimal |  x* = {optimal_points[1]} | number of iteration is = {len(paths[1])}")
    anim = creat_animation(f, paths, minimum,
                     x_lim, y_lim,
                     colors, labels, n_seconds=5,
                       figsize = (14,16))
    anim.save('animation1.gif', writer=PillowWriter(fps=30))
    
    

