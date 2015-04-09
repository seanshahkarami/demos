import numpy as np
import matplotlib.pyplot as plt


def complex_plot(w, N=1024):
    cm = plt.get_cmap('hsv', N)
    colors = cm(np.linspace(0, 1, cm.N))[:, [0, 1, 2]]

    mag = np.abs(w)

    phase = (np.angle(w) / (2.0*np.pi)) + 0.5
    phase[phase < 0.0] = 0.0
    phase[phase > 1.0] = 1.0

    t = (phase % 0.0125) / 0.0125
    s = (np.log(mag+1.0) % 0.075) / 0.075

    rad = 0.6*(1-t) + 0.4*t + 0.4*(1-s) + 0.2*s

    col = colors[np.floor(phase * (cm.N-1)).astype(np.int)]

    return plt.imshow(col * rad[:, :, None])


#xs = np.linspace(-1.5, 1.5, 2000)
#ys = np.linspace(-1.5, 1.5, 2000)
#xs = np.linspace(-2.0, 2.0, 2500)
#ys = np.linspace(-2.0, 2.0, 2500)
#x, y = np.meshgrid(xs, ys)

#z = x + y*1.0j
#w = (z-0.5)*(z+0.5)*(z-0.5j)*(z+0.5j)
#w = (z-(-0.5-0.5j)) * (z-(0.5-0.5j)) * (z - 0.5j)
#w = (1.0 - z**2.0)**0.5
#w = np.log(z+0.25) * (z-(-0.75 + 0.5j)) * (z-(-0.75 - 0.5j)) * (z-(0.5 - 0.75j)) * (z-(0.5 + 0.75j))
#w = (z - 0.75) * (z-(-0.75 + 0.5j)) * (z-(-0.75 - 0.5j)) * (z-(0.3 - 0.75j)) * (z-(0.3 + 0.75j))
#w = z**2 + 2.0 * np.conj(z)
#w = 1.0/(z**4 + 4.0*z + 4.0)**2

#mag = np.abs(w)

#phase = (np.angle(w) / (2.0*np.pi)) + 0.5
#phase[phase < 0.0] = 0.0
#phase[phase > 1.0] = 1.0

#t = (phase % 0.0125) / 0.0125
#s = (np.log(mag+1.0) % 0.075) / 0.075
#s = (mag % 0.075) / 0.075

#rad = 0.6*(1-t) + 0.4*t + 0.4*(1-s) + 0.2*s

#col = colors[np.floor(phase * (cm.N-1)).astype(np.int)]

#plt.imsave('plot.png', col * rad[:, :, None])
