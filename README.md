# Programming Test 
## Instructions
### Requirements
##### 1. Python 3 Standard Modules (random, multiprocessing)
##### 2. Web Browser that supports HTML5 and JS. 
EIther Edge, Chrome, Opera, Firefox, or Safari. 
##### 3. Additional Modules
To get the additional modules, you can run the following command in CLI
```
pip install -r requirements.txt
```
It will automatically install the additional packages.  

### Instructions
After you managed to install all the dependencies, just navigate into the project folder on your OS and run
#### Windows
```
py main.py 
```
#### Linux/Mac OS
```
python3 main.py
```

## Workflow
### Microcontroller Mock (sensor_reader.py)
The file sensor_reader.py is a module that concurrently (using multiprocessing based concurrency) measure temperature, humidity, luminosity, by randomly generates input voltage from 0-255 for humidity, temperature and luminosity and process it into real values while also listens for incoming signal to switch light on and off (this will affect the luminosity random number generator). The acquire_data() function inside this file is meant to be called as a separate process, and will periodically sends the measured data.  
#### Example usage:
```
from sensor_reader import acquire_data
from multiprocessing import Queue, Process
queue = Queue(1)
light_switch = Queue(1)
light = True #initially the light is on
process = Process(target = acquire_data, args = (queue, light_switch)) # the function is called as a separate process
process.start()
while 1:
    print(queue.get())  
    light = not light #change the light state
    light_switch.put(light) #signal the microcontroller to change the light state
    
```
#### Example output:
```
527.45, 32.82, 13.73
135.03, 32.82, 13.33
527.45, 32.82, 13.33
135.03, 32.82, 14.12
531.67, 32.82, 12.94
105.49, 34.12, 13.73
```
The data generated is comma delimited with the following order: Luminosity in Lux, Temperature in Celcius, and Humidity in Percent. 

### Main File (main.py)
The main file connects with the microcontroller mock and updates the GUI whenever a message is received from the microcontroller thread. It uses the eel package to connect and call javascript function that controls the HTML based GUI.  

