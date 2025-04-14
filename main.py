import pygame
import pyaudio
import numpy as np
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import butter, lfilter


# file_path = pygame.__file__

# print(file_path)

# pygame.init()

# screen = pygame.display.set_mode([500, 500])

# running = True
# while running:

#     addH = 0

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
    
#     screen.fill((255,255,255))



#     pygame.draw.rect(screen,(100,200,100),(200,200+addH,100,100))

#     pygame.display.flip()




import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import butter, lfilter

# Constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# ===== Bandpass Filter (optional) =====
def butter_bandpass(lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_bandpass(data, lowcut=80.0, highcut=1200.0):
    b, a = butter_bandpass(lowcut, highcut, RATE)
    return lfilter(b, a, data)

# ===== PyAudio Setup =====
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=3,
                frames_per_buffer=CHUNK)

# ===== Plot Setup =====
fig, ax = plt.subplots()
bar, = ax.plot([], [], lw=6)
ax.set_ylim(0, 0.3)   # Adjust max if needed
ax.set_xlim(0, 10)
plt.title("Real-Time Loudness (RMS)")
plt.xlabel("Frame")
plt.ylabel("Loudness")

# History buffer
rms_history = [0.0] * 10

# ===== Update Function =====
def update(frame):
    data = stream.read(CHUNK, exception_on_overflow=False)
    samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

    # Optional filtering
    filtered = apply_bandpass(samples)

    # RMS loudness
    rms = np.sqrt(np.mean(filtered**2))
    rms_history.append(rms)
    rms_history.pop(0)

    bar.set_data(range(len(rms_history)), rms_history)
    return bar,

# Animate
ani = animation.FuncAnimation(fig, update, interval=50, blit=True)
plt.show()

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()



# import pyaudio

# p = pyaudio.PyAudio()

# print("Available audio input devices:\n")
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     if info["maxInputChannels"] > 0:
#         print(f"Index {i}: {info['name']}")

# p.terminate()
