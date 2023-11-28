import threading
import time
import tkinter as tk
from threading import Thread

import matplotlib as plt
import matplotlib.axis
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

from util.PlottingUtil import *
from cube_model.Cube import FactInstance
from util.IKillable import Killable
from util.Util import Util


class ImageGrid(tk.Frame):
    def __init__(self, master, image_label_data, last_command: str = 'None'):
        super().__init__(master)
        self.master = master
        self.image_label_data = image_label_data
        riga = 0
        max_column = 0
        self.last_command=last_command
        for text in image_label_data:
            riga += 1
            font = 30
            column = 0

            for c in text.split(';'):
                text_label1 = tk.Label(self, text=c, font=("Arial", int(font)))
                text_label1.grid(row=riga, column=column)
                if max_column < column:
                    max_column = column
                column += 1
                font = font/1.5
            #text_label2 = tk.Label(self, text=l[1], font=("Arial", 15))
            #text_label2.grid(row=riga, column=1 )

        text_label1 = tk.Label(self, text='Comando', font=("Arial", int(20)))
        text_label1.grid(row=riga+1, column=0)

        self.text_label1 = tk.Label(self, text=last_command, font=("Arial", int(30/1.5)))
        self.text_label1.grid(row=riga+1, column=max_column)
        self.riga = riga+1
        self.max_column = max_column
        self.pack(side='left', fill=tk.BOTH, expand=False, padx=10, pady=10)

    def update_command(self, command):
        if command != self.last_command:
            self.text_label1.config(text=command)
            self.last_command = command


class MatplotlibFrame(tk.Frame):
    def __init__(self, master, axis: matplotlib.axis.Axis,ppi_x=100,  ppi_y=100):
        super().__init__(master)
        self.ppi_x = ppi_x
        self.ppi_y = ppi_y
        self.canvas1 = FigureCanvasTkAgg(axis.get_figure(), master=self)
        self.pack(side="left", fill="both", expand=True)
        self.canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

    def update_axis(self, axis:  matplotlib.axis.Axis):
        self.canvas1.figure = axis.get_figure()
        self.canvas1.figure.set_size_inches(np.array([self.winfo_width()/(self.ppi_x+1),
                                                      self.winfo_height()/(self.ppi_y+1)]))
        self.canvas1.draw()


class MasterFrame(tk.Frame):
    def __init__(self, master, axis: matplotlib.axis.Axis, image_label_data,ppi_x=100,  ppi_y=100):
        super().__init__(master)
        self.axis = axis
        self.frame_axis = MatplotlibFrame(self, axis, ppi_x, ppi_y)
        self.frame_emoji = ImageGrid(self, image_label_data)
        self.frame_emoji.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=10, pady=10)

    def update_axis(self, axis: matplotlib.axis.Axis):
        self.frame_axis.update_axis(axis)


class GestoreGraficoMid:
    def __init__(self, fact_instance: FactInstance, emojis_list: list[str],
                 lock_file=threading.Lock(), killable_listeners: list[Killable] = None):
        self.lock_changes = threading.Lock()
        self.fact_instance: FactInstance = fact_instance
        self.actual_frame = 0
        self.emojis = emojis_list
        self.changes = False
        self.lock_file = lock_file
        self.killable_listeners = killable_listeners
        self.last_command = 'None'

    def next(self):
        if self.actual_frame < len(self.fact_instance.dimensions)-1:
            self.actual_frame += 1
            self.lock_changes.acquire()
            print(self.fact_instance.dimensions[self.actual_frame].get_actual_level_name())
            self.changes = True
            self.lock_changes.release()

    def previous(self):
        if self.actual_frame > 0:
            self.actual_frame -= 1
            self.lock_changes.acquire()
            self.changes = True
            self.lock_changes.release()

    def declare_data_is_change(self):
        self.lock_changes.acquire()
        self.changes = True
        self.lock_changes.release()

    def update_last_command(self,command):
        if self.last_command != command:
            self.last_command = command
            self.lock_changes.acquire()
            self.changes = True
            self.lock_changes.release()


def update_gui(master_frame: MasterFrame, gestore: GestoreGraficoMid, root, axis):
    gestore.lock_changes.acquire()
    if gestore.changes:
        gestore.lock_file.acquire()
        try:
            axis = get_histo_2d_axes(gestore.fact_instance.dimensions[gestore.actual_frame].get_actual_level_name().upper(),
                                     gestore.fact_instance.get_aggregate_data_name_as_str(),
                                     delimiter=';')
        except Exception as e:
            gestore.fact_instance.dimensions[gestore.actual_frame].dimension_down()
            axis = get_histo_2d_axes(
                gestore.fact_instance.dimensions[gestore.actual_frame].get_actual_level_name().upper(),
                gestore.fact_instance.get_aggregate_data_name_as_str(),
                delimiter=';')
            print(e)
        gestore.lock_file.release()
        master_frame.update_axis(axis)
        master_frame.frame_emoji.update_command(gestore.last_command)
        gestore.changes = False
    gestore.lock_changes.release()


def launch_graphic_app(gestore: GestoreGraficoMid):
    root = tk.Tk()
    root.state('zoomed')
    root.title('tesi'.upper())
    time.sleep(1)
    try:
        path = Util.get_properties_from_file('../../../utilities/config.property', 'utf-8',
                                             'DEFAULT', 'logo_path')
        load = Image.open(path)
        render = ImageTk.PhotoImage(load)
        root.iconphoto(True, render)
    except Exception as e:
        print(e)
        pass

    # Get screen resolution in pixels
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get physical screen size in millimeters
    screen_width_mm = root.winfo_screenmmwidth()
    screen_height_mm = root.winfo_screenmmheight()

    # Convert millimeters to inches
    mm_per_inch = 25.4  # 1 inch = 25.4 mm
    screen_width_inches = screen_width_mm / mm_per_inch
    screen_height_inches = screen_height_mm / mm_per_inch

    # Calculate pixels per inch (PPI)
    ppi_x = screen_width / screen_width_inches
    ppi_y = screen_height / screen_height_inches
    gestore.lock_file.acquire()
    try:
        axis = get_histo_2d_axes(gestore.fact_instance.dimensions[gestore.actual_frame].get_actual_level_name().upper(),
                                 gestore.fact_instance.get_aggregate_data_name_as_str(),
                                 delimiter=';')
    except Exception as e:
        print(e)

    gestore.lock_file.release()
    master_frame = MasterFrame(master=root, image_label_data=gestore.emojis, axis=axis, ppi_x=ppi_x, ppi_y=ppi_y)
    master_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def update_periodically():
        update_gui(master_frame, gestore, root, axis)
        root.after(50, update_periodically)  # Schedule the task to run again after 50 milliseconds

    def on_closing():
        if gestore is not None:
            try:
                for i in gestore.killable_listeners:
                    try:
                        i.kill()
                    except Exception as e:
                        pass
            except Exception as e1:
                pass
        tk.Tk.quit(root)
        plt.close('all')
        root.destroy()
        #exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Schedule the first execution of the task
    root.after(1, update_periodically)
    root.mainloop()


def get_gestore_graphic(file_lock: threading.Lock, fact_instance: FactInstance, killable_listeners: list[Killable],
                        emojis_list: list[str] = None) -> GestoreGraficoMid:
    if emojis_list is None:
        emojis_list = [';;COMANDI GRAFICA',
                       '👍;=;AVANTI',
                       '👎;=;INDIETRO',
                       ';;SVUOTA MEMORIA',
                       '🤚;=;ELIMINA_AZIONE',
                       ';;COMANDI_OLAP',
                       '☝️;=;C-ROLL_UP',
                       '✊;=;C-DRILL_DOWN',
                       ';;DIMENSIONI',
                       '🤟;=;D_TEMPO',
                       '✌️;=;D_PRODOTTO',
                       '✊;=;D_NEGOZIO',
                       'REGOLA;;C+D']
    gestore = GestoreGraficoMid(fact_instance=fact_instance, emojis_list=emojis_list, lock_file=file_lock,
                                killable_listeners=killable_listeners)
    return gestore


def launch_app_as_thread(gestore: GestoreGraficoMid) -> Thread:
    t1 = Thread(target=launch_graphic_app, args=[gestore])
    t1.start()
    return t1

