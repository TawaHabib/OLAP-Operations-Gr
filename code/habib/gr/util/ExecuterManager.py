import threading
import time
from threading import Thread, Event
import win32com.client
import matplotlib as plt

from models.GestureModels import Gesture
from util.DataBaseUtility import get_sql_executor
from util.DashboardUtility import launch_app_as_thread
from cube_model.Cube import get_sales_fact_instance
from cube_model.Cube import FactInstance
from cube_model.Cube import IDimension
from util.DashboardUtility import get_gestore_graphic
from util.IKillable import Killable


class MediaPipeGesturesCommand(object):
    def Closed_Fist(self):
        pass

    def Open_Palm(self):
        pass

    def Pointing_Up(self):
        pass

    def Thumb_Down(self):
        pass

    def Thumb_Up(self):
        pass

    def Victory(self):
        pass

    def ILoveYou(self):
        pass

    def kill(self):
        pass


class ExecuteManager(Thread, Killable):

    def __init__(self, x=1, min_confidence=0.7):
        super().__init__()
        self.event = Event()
        self.last_execution: list[str] = []
        self.current_execution: list[str] = []
        self.life: bool = True
        self.command_manager = None
        self.last_time_execution = time.time_ns()
        self.x = x
        self.min_confidence = min_confidence

    def run(self) -> None:
        super().run()
        self.command_manager = CommandManager()
        while self.get_life():
            self.event.wait()
            self.event.clear()
            #######TABELLA VERITA FUNZIONAMENTO IF:
            #A=> RISULTATO DELL INTERROGAZIONE COMANDO ATTUALE UGUALE AL COMANDO PRECEDENTE
            #B=> RISULTATO dell'interrogazione è passato x secondi dall'esecuxione dell'ultimo comando
            ##A |   B   |   OUT
            ##0 |   0   |   F
            ##0 |   1   |   F
            ##1 |   0   |   V
            ##1 |   1   |   F
            ##QUINDI OUT=A && (!B)
            if (sorted(self.current_execution) == sorted(self.last_execution) and
                    (not (((time.time_ns()-self.last_time_execution)/1000000000) > self.x))):
                #print((time.time_ns()-self.last_time_execution)/1000000000)
                continue

            for command in self.current_execution:
                print('execution command: '+command)
                self.execute_command(command)

            self.last_execution.clear()
            self.last_execution.extend(self.current_execution)
            self.last_time_execution=time.time_ns()
        self.command_manager.kill()

    def kill(self):
        self.life = False
        self.command_manager.kill()
        self.event.set()

    def execute_command(self, command: str):
        try:
            method = getattr(self.command_manager.get_commands_class(), command)
            method()
            self.last_time_execution = time.time_ns()
        except Exception as e:
            print('FAIL TO EXECUTE_COMMAND'+command)
            print(e)

    def update_gestures(self, gestures: list[Gesture]):
        current = []
        last = []
        current.extend(self.current_execution)
        last.extend(self.last_execution)

        self.last_execution.clear()
        self.last_execution.extend(self.current_execution)
        self.current_execution.clear()

        for g in gestures:
            if g.gesture_id != 'None' and g.score > 0.5:
                #print(g.score)
                self.current_execution.append(g.gesture_id)

        if self.current_execution.__len__() == 0:
            #self.last_time_execution = time.time_ns()
            self.current_execution.clear()
            self.last_execution.clear()
            self.last_execution.extend(last)
            self.current_execution.extend(current)
        else:
            self.event.set()

    def get_life(self) -> bool:
        return self.life


class CommandManager(Killable):
    def __init__(self):
        self.command = TwoPassDWhCommand()

    def get_commands_class(self) -> object:
        return self.command

    def kill(self):
        self.command.kill()


class TwoPassDWhCommand(Killable, MediaPipeGesturesCommand):
    def __init__(self):
        self.command = ''
        self.pax = 0
        self.data_base_executor = get_sql_executor()
        self.file_lock = threading.Lock()
        self.fact_instance = get_sales_fact_instance()
        self.data_base_executor.execute_and_save(self.fact_instance.get_dimensions_levels_as_str())
        self.gestore_grafica = get_gestore_graphic(self.file_lock, fact_instance=self.fact_instance,
                                                   killable_listeners=[self.data_base_executor])
        self.graphic_thread: threading.Thread = launch_app_as_thread(self.gestore_grafica)

    def Open_Palm(self):
        self.command = ''
        self.pax = 0
        self.gestore_grafica.update_last_command(self.command)

    def Thumb_Down(self):
        self.gestore_grafica.previous()
        self.gestore_grafica.update_last_command(self.command)

    def Thumb_Up(self):
        self.gestore_grafica.next()
        self.gestore_grafica.update_last_command(self.command)

    def Closed_Fist(self):
        self.__actions('Closed_Fist')
        self.gestore_grafica.update_last_command(self.command)

    def Pointing_Up(self):
        self.__actions('Pointing_Up')
        self.gestore_grafica.update_last_command(self.command)

    def Victory(self):
        self.__actions('Victory')
        self.gestore_grafica.update_last_command(self.command)

    def ILoveYou(self):
        self.__actions('ILoveYou')
        self.gestore_grafica.update_last_command(self.command)

    def kill(self):
        self.graphic_thread.join(0)
        self.data_base_executor.kill()
        self.pax = -1

    def __actions(self, caller_name_as_str: str):
        match self.pax:
            case 0:
                #print(caller_name_as_str+'\taccepted')
                self.command = str(caller_name_as_str)
                self.pax += 1
            case 1:
                self.command = self.command+'_'+str(caller_name_as_str)
                self.__execute_cmd(self.command)
                self.pax = 0
                self.command = ''
            case -1:
                pass

    def __execute_cmd(self, command):
        try:
            print('try to execute\t'+command)
            method = getattr(self, command)
            method()
        except Exception as e:
            #print('FAIL TO EXECUTE_COMMAND:\t' + self.command+'\n\t'+str(e))
            pass

    #ROLL UP  SU TEMPO
    def Pointing_Up_ILoveYou(self):
        self.roll_up_operation('tempo')

    #ROLL UP SU PRODOTTO
    def Pointing_Up_Victory(self):
        self.roll_up_operation('prodotto')

    #ROLL UP SU FILIALE
    def Pointing_Up_Closed_Fist(self):
        self.roll_up_operation('filiale')

    # DRILL-DOWN SU TEMPO
    def Closed_Fist_ILoveYou(self):
        self.drill_down_operation('TEMPO')

    # DRILL-DOWN SU PRODOTTO
    def Closed_Fist_Victory(self):
        self.drill_down_operation('prodotto')

    # DRILL-DOWN SU FILIALE
    def Closed_Fist_Closed_Fist(self):
        self.drill_down_operation('FILIALE')

    def roll_up_operation(self, dimension: str):
        if not self.fact_instance.roll_up(dimension.upper()):
            return
        self.file_lock.acquire()
        self.data_base_executor.execute_and_save(self.fact_instance.get_dimensions_levels_as_str())
        print(self.fact_instance.get_dimensions_levels_as_str())
        self.file_lock.release()
        self.gestore_grafica.declare_data_is_change()

    def drill_down_operation(self, dimension: str):
        if not self.fact_instance.drill_down(dimension.upper()):
            return
        self.file_lock.acquire()
        self.data_base_executor.execute_and_save(self.fact_instance.get_dimensions_levels_as_str())
        self.file_lock.release()
        print(self.fact_instance.get_dimensions_levels_as_str())
        self.gestore_grafica.declare_data_is_change()


class PrintCommands(Killable, MediaPipeGesturesCommand):

    def __init__(self):
        pass

    def Closed_Fist(self):
        print('\n'+'Closed_Fist executed'+'\n')

    def Open_Palm(self):
        print('\n'+'Open_Palm executed'+'\n')

    def Pointing_Up(self):
        print('\n'+'Pointing_Up executed'+'\n')

    def Thumb_Down(self):
        print('\n'+'Thumb_Down executed'+'\n')

    def Thumb_Up(self):
        print('\n'+'Thumb_Up executed'+'\n')

    def Victory(self):
        print('\n'+'Victory executed'+'\n')

    def ILoveYou(self):
        print('\n'+'ILoveYou executed'+'\n')

    def kill(self):
        print('killed')
