import numpy as np
import matplotlib.pyplot as plt

# Create a figure and an axes object.
fig, ax = plt.subplots()

# Plot a line.
line, = ax.plot(np.linspace(0, 10, 100), np.sin(np.linspace(0, 2 * np.pi, 100)))

# Define a function to handle keyboard input.
def on_key_press(event):
    global line

    # Move the line up when the Up arrow key is pressed.
    if event.key == "Up":
        line.set_ydata(line.get_ydata() + 0.1)

    # Move the line down when the Down arrow key is pressed.
    elif event.key == "Down":
        line.set_ydata(line.get_ydata() - 0.1)

    # Redraw the plot.
    plt.draw()

# Connect the `on_key_press` function to the `key_press` event.
fig.canvas.mpl_connect("key_press_event", on_key_press)

# Show the plot.
plt.show()
