from multiprocessing import Process, Queue
from time import sleep
from random import randint

SAMPLING = 255
VOLTAGE = 3.3
MAX_LUX = 1076

def read_photosensor(data_queue : Queue, light_switch : Queue):
    """
    Read the photoresistor data ranging from 0-1076 LUX, actively listens for any light switch process
    """
    multiplier = VOLTAGE/SAMPLING
    a = 125
    b = 128
    while 1:
        if light_switch.empty():
            input_voltage  = randint(a,b) * multiplier
            brightness = (input_voltage / 3.3) * MAX_LUX
            data_queue.put(brightness)
            sleep(1)
        else:
            if not light_switch.get():
                a = 25
                b = 33
                continue
            a = 125
            b = 128


def read_temperature(data_queue : Queue):
    """
    Read the temperature data in celcius from analog data randomly generated
    """
    multiplier = VOLTAGE/SAMPLING
    while 1:
        input_voltage = randint(64,65) * multiplier
        temperature = (input_voltage - 0.5) * 100
        data_queue.put(temperature)
        sleep(1)

def read_humidity(data_queue : Queue):
    """
    Read the humidity data in percent from analog data randomly generated
    """
    multiplier = VOLTAGE/SAMPLING
    while 1:
        input_voltage = randint(33,37) * multiplier
        humidity = (input_voltage/3.3) * 100
        data_queue.put(humidity)
        sleep(1)

def acquire_data(sensor_data : Queue, light_signal : Queue):
    """
    Generates threads for each measurements and send the data through queue into the caller process.
    """
    photosensor_result = Queue(1)
    temperature_result = Queue(1)
    humidity_result = Queue(1)
    photosensor_thread = Process(target=read_photosensor, args=(photosensor_result, light_signal)) 
    temperature_thread = Process(target=read_temperature, args=(temperature_result,)) 
    humidity_thread = Process(target = read_humidity, args=(humidity_result,)) 
    photosensor_thread.start()
    temperature_thread.start()
    humidity_thread.start()
    while 1:
        try:
            sensor_data.put("%0.2f, %0.2f, %0.2f" %(photosensor_result.get(), temperature_result.get(), humidity_result.get()))
        except KeyboardInterrupt:
            break
    photosensor_thread.join()
    temperature_thread.join()
    humidity_thread.join()

    
    
if __name__ == '__main__':
    """
    in case if this script is being run for testing purposes
    """
    queue = Queue(1)
    light_switch = Queue(1)
    light = True #initially the light is on
    process = Process(target = acquire_data, args = (queue, light_switch)) # the function is called as a separate process
    process.start()
    while 1:
        print(queue.get()) 
        light = not light #change the light state
        light_switch.put(light) #signal the microcontroller to change the light state