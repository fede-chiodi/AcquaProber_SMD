from multiprocessing import Process, Manager
from modules.sensors.collect_data import collect_data
from GUI.gui_process import run_gui
from modules.plotter.plotter import plotter_worker
from modules.feeder.feeder import feeder_worker

if __name__ == "__main__":
    with Manager() as manager:
        shared_dict = manager.dict()
        shared_dict["status"] = True
        shared_dict["mode"] = 0

        data_process = Process(target=collect_data, args=(shared_dict, ))
        gui_process = Process(target=run_gui, args=(shared_dict, ))
        plotter_process = Process(target=plotter_worker, args=(shared_dict, ))
        feeder_process = Process(target=feeder_worker, args=(shared_dict, ))

        data_process.start()
        gui_process.start()
        plotter_process.start()
        feeder_process.start()

        data_process.join()
        gui_process.join()
        plotter_process.join()
        feeder_process.join()
