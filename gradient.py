import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Example Dataset with 5 independent variables (x1, x2, x3, x4, x5) and 1 dependent variable (y)
data = {
    'x1': [1, 2, 3, 4, 5],
    'x2': [2, 4, 6, 8, 10],
    'x3': [5, 7, 9, 11, 13],
    'x4': [3, 6, 9, 12, 15],
    'x5': [10, 20, 30, 40, 50],
    'y': [1, 2, 3, 4, 5]
}

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Independent variables (x1, x2, x3, x4, x5) and dependent variable (y)
X = df[['x1', 'x2', 'x3', 'x4', 'x5']].values
y = df['y'].values.reshape(-1, 1)

# Normalize the data for better visualization
X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

# Initialize parameters (weights and bias), let's start them at zero
m = len(y)  # number of training examples
beta_0 = 0  # Intercept
beta = np.zeros((X.shape[1], 1))  # Coefficients for x1, x2, x3, x4, x5

# Define the learning rate and the number of iterations
learning_rate = 0.01
num_iterations = 100

# To store the history of the cost function
cost_history = []

# Define the cost function (Mean Squared Error)
def compute_cost(X, y, beta_0, beta):
    predictions = beta_0 + np.dot(X, beta)
    errors = predictions - y
    cost = (1 / (2 * m)) * np.sum(errors ** 2)
    return cost

# Gradient Descent function
def gradient_descent(X, y, beta_0, beta, learning_rate, num_iterations):
    for iteration in range(num_iterations):
        # Predictions
        predictions = beta_0 + np.dot(X, beta)
        
        # Compute the error (difference between predictions and actual values)
        errors = predictions - y
        
        # Compute gradients for beta_0 and beta
        gradient_beta_0 = (1 / m) * np.sum(errors)
        gradient_beta = (1 / m) * np.dot(X.T, errors)
        
        # Update parameters using gradient descent formula
        beta_0 = beta_0 - learning_rate * gradient_beta_0
        beta = beta - learning_rate * gradient_beta
        
        # Calculate and store the cost
        cost = compute_cost(X, y, beta_0, beta)
        cost_history.append(cost)
        
        # Yield parameters for animation
        yield iteration, beta_0, beta, cost

# Create figure for animation
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("Cost Function Minimization")
ax.set_xlabel("Iteration")
ax.set_ylabel("Cost (MSE)")

# Animation data (cost values and lines)
line, = ax.plot([], [], 'b-', label='Cost Function')
text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# Initialization function for animation
def init():
    ax.set_xlim(0, num_iterations)
    ax.set_ylim(0, 10)
    line.set_data([], [])
    text.set_text('')
    return line, text

# Animation update function
x_data, y_data = [], []
def update(frame):
    iteration, beta_0, beta, cost = frame
    x_data.append(iteration)
    y_data.append(cost)
    
    line.set_data(x_data, y_data)
    text.set_text(f"Iteration {iteration+1}\nCost: {cost:.5f}\nbeta_0: {beta_0:.5f}\nbeta: {beta.T}")
    
    return line, text

# Run the gradient descent with animation
anim_data = gradient_descent(X, y, beta_0, beta, learning_rate, num_iterations)
anim = FuncAnimation(fig, update, frames=anim_data, init_func=init, blit=True, repeat=False)
anim.save('animation.gif', writer='pillow', fps=20)
#anim.save('animation.mp4', writer='ffmpeg', fps=2)
# Show the animation and plot
#plt.legend()
#plt.show()

# Final parameter values
print(f"Final beta_0 (intercept): {beta_0}")
print(f"Final beta (coefficients): {beta.T}")