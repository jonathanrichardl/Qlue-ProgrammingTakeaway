import eel
from multiprocessing import Queue, Process
from sensor_reader import acquire_data

light_switch = Queue(1)

@eel.expose
def turn_lights_on():
    """
    Signal the photosensor input voltage random generator to produce high numbers (to simulate a bright room)
    """
    light_switch.put(True)
    return

@eel.expose
def turn_lights_off():
    """
    Signal the photosensor input voltage random generator to produce low numbers (to simulate that a dark room)
    """
    light_switch.put(False)
    return


def main():
    sensor_data = Queue()
    eel.init("gui")
    microcontroller = Process(target=acquire_data, args = (sensor_data, light_switch ))
    microcontroller.start()
    eel.start("index.html", block = False)
    while 1:
        try:
            photosensor, temperature, humidity  = list(map(str,sensor_data.get().split(",")))
            eel.dataUpdate(photosensor, temperature, humidity)
            eel.sleep(1)
        except KeyboardInterrupt:
            break
    microcontroller.join()
    

    


if __name__ == '__main__':
    main()