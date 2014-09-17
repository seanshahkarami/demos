#
# Mean Field XY Model Simulation via the Metropolis Algorithm
#
# Author: Sean Shahkarami <sean.shahkarami@gmail.com>
#
# About: This was written for a talk with Mark Schubel and Tayyab Nawaz. It's
# an animated demo of using the Metropolis algorithm to simulate the classical
# mean field XY model.
#

import numpy as np
from numpy import pi, cos, sin, sum
import numpy.linalg as la
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import time


# Initialize our spin lattice.
width = 64
height = 64
ncells = width * height
angles = np.random.rand(ncells) * 2.0 * pi
spins = np.column_stack([cos(angles), sin(angles)])


# Initialize system parameters.
J = -1.0
z = 1.0
temperature = 1.0
external_field = np.array([0.0, 0.0])


# Initialize image related data. right is just a vector pointed to the right,
# used as a reference spin to compare other spins to when coloring the image.
right = np.array([1.0, 0.0])
image1d = np.inner(spins, right)
image2d = image1d.reshape(width, height)


# Compute initial macroscopic quantities.
sum_of_spins = np.sum(spins, axis=0)
magnetization = sum_of_spins / ncells
energy = J * z * np.inner(sum_of_spins, magnetization) + np.inner(sum_of_spins, external_field)


def animate(i):
	global iters
	global spins
	global sum_of_spins
	global magnetization
	global energy

	new_spin = np.zeros(2) # Preallocate storage for new spin.

	runtime = time.time() + 0.90 / fps # Compute the amount of time to run the frame. (90% of frame time)

	while time.time() < runtime:
		iters += 1

		#
		# This is really the heart of the Metroplis algorithm. During each iterations
		# we choose a random cell and a random spin we will potentially assign to it.
		# We accept the new spin with probability min(1, exp(-dE / T)) where dE is the
		# change in energy.
		#
		# In order to relate this to the Metropolis algorithm, notice that we divided
		# the iterations into two steps: selection and acceptance.
		#
		# Recall that this essentially means we factor the transition probability
		#
		# P(x -> y) = A(x -> y) * S(x -> y)
		#
		# where A is the acceptance probability and S is the selection probability. In
		# our case, the selection probability staisfies the nice condition that the ratio
		#
		#   S(x -> y)
		#   --------- = 1
		#   S(y -> x)
		#
		# Thus, the Metropolis algorithm tells us we should choose the acceptance probability
		#
		#                    P(y) * S(y -> x)           P(y)
		# A(x -> y) = min(1, ----------------) = min(1, ----)
		#                    P(x) * S(x -> y)           P(x)
		#
		# where P(E) is the Boltzmann distribution, P(E) = exp(-E / T).
		#

		# Select a new state by flipping a spin.
		i = np.random.randint(0, ncells)

		angle = np.random.rand() * 2.0 * pi
		new_spin[0] = cos(angle)
		new_spin[1] = sin(angle)

		new_sum_of_spins = sum_of_spins + new_spin - spins[i]
		new_magnetization = new_sum_of_spins / ncells
		new_energy = J * z * np.inner(new_sum_of_spins, new_magnetization) + \
			np.inner(new_sum_of_spins, external_field)

		# Check if we accept the state.
		if new_energy < energy or np.random.rand() < np.exp(-(new_energy - energy) / temperature):
			spins[i] = new_spin
			
			# Update macroscopic quantities.
			sum_of_spins = new_sum_of_spins
			magnetization = new_magnetization
			energy = new_energy

			# Update image cell.
			image1d[i] = np.inner(spins[i], right)

	im.set_data(image2d)

	stddev = la.norm(spins - magnetization)

	# Update the text display.
	text_iters.set_text('Iterations\n' + str(iters))
	text_energy.set_text('Energy\n' + str(J * z * np.inner(magnetization, magnetization)))
	text_magnetization.set_text('Magnetization\n' + str(la.norm(magnetization)))
	text_stddev.set_text('Std. Dev.\n' + str(stddev))


mpl.rcParams['toolbar'] = 'None' # Hides the mpl toolbar.

fig = plt.figure()


# Setup animation axes.
anim_ax = fig.add_subplot(1, 2, 1)
anim_ax.axis('off')
im = anim_ax.imshow(image2d, interpolation='nearest', cmap='jet', vmin=-1.0, vmax=1.0)


# Setup the temperature slider axes.
def update(val):
	global iters
	global temperature
	iters = 0
	temperature = val

temperature_slider_ax = plt.axes([0.20, 0.10, 0.60, 0.025])
temperature_slider = Slider(temperature_slider_ax, 'Temperature', 0.0, 5.0, temperature)
temperature_slider.on_changed(update)


# Setup the text display axes.
text_ax = fig.add_subplot(1, 2, 2)
text_ax.axis('off')
text_iters = text_ax.text(0.1, 0.70, '')
text_energy = text_ax.text(0.1, 0.60, '')
text_magnetization = text_ax.text(0.1, 0.50, '')
text_stddev = text_ax.text(0.1, 0.40, '')


# Start the animation.
fps = 60.0
iters = 0
anim = animation.FuncAnimation(fig, animate, 200, interval=1000.0/fps, blit=False)
plt.show()
