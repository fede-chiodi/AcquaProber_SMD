from multiprocessing import Process, Manager
from .modules.sensors.collect_data import collect_data
from .GUI.gui_process import run_gui

if __name__ == "__main__":
    with Manager() as manager:
        shared_dict = manager.dict()

        data_process = Process(target=collect_data, args=(shared_dict, ))
        gui_process = Process(target=run_gui, args=(shared_dict, ))

        data_process.start()
        gui_process.start()

        data_process.join()
        gui_process.join()
