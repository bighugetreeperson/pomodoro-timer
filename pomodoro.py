from tkinter import *
from tkinter import ttk
from math import floor
from plyer import notification

CONST_POMODORO_TIME = 1500
CONST_BREAK_TIME = 300
CONST_POMODORO_COUNT = 3


def convert_time_to_string(time):
    pomodoro_minutes = floor(time / 60)
    pomodoro_seconds = time % 60
    pomodoro = f"{pomodoro_minutes}:{pomodoro_seconds:02d}"
    return pomodoro


class Timer:
    _timer_started = False
    _timer_id = None
    _pomodoro_count = 1
    _is_in_break = False
    _pomodoro_time_raw = CONST_POMODORO_TIME

    def start_timer(self):
        if not self._timer_started:
            self._timer_started = True
            pomodoro_header.set(f"Pomodoro {self._pomodoro_count}, active")
            self.decrement_pomodoro()

    def stop_timer(self):
        root.after_cancel(self._timer_id)
        print("Timer stopped")
        self._timer_started = False
        pomodoro_time.set("Not Yet Started")
        pomodoro_header.set("Not Yet Started")
        self._pomodoro_time_raw = CONST_POMODORO_TIME

    def pause_timer(self):
        root.after_cancel(self._timer_id)
        self._timer_started = False
        pomodoro_time.set("Paused")

    def decrement_pomodoro(self):
        if self._pomodoro_time_raw > 1:
            self._pomodoro_time_raw -= 1
            pomodoro_time.set(convert_time_to_string(self._pomodoro_time_raw))
            self._timer_id = root.after(1000, self.decrement_pomodoro)
        elif self._pomodoro_count > CONST_POMODORO_COUNT:
            # The last pomodoro has completed, so we're ending it
            root.after_cancel(self._timer_id)
            pomodoro_time.set("Pomodoro Over!")
            self._timer_started = False
            self._pomodoro_time_raw = CONST_POMODORO_TIME
            notification.notify(title="Pomodoro Timer", message=f"Time for a long break!")
        else:
            # We should have logic switching between pause/pomodoro and resetting the clock here.
            if self._is_in_break:
                # Going to next pomodoro
                self._is_in_break = False
                self._pomodoro_time_raw = CONST_POMODORO_TIME
                self._pomodoro_count += 1
                pomodoro_time.set(convert_time_to_string(self._pomodoro_time_raw))
                self._timer_id = root.after(1000, self.decrement_pomodoro)
                notification.notify(title="Pomodoro Timer", message=f"Pomodoro #{self._pomodoro_count}, break has ended!")
            else:
                # Going to next break
                self._is_in_break = True
                self._pomodoro_time_raw = CONST_BREAK_TIME
                pomodoro_time.set(convert_time_to_string(self._pomodoro_time_raw))
                self._timer_id = root.after(1000, self.decrement_pomodoro)
                notification.notify(title="Pomodoro Timer", message=f"Pomodoro #{self._pomodoro_count}, break has started!")


root = Tk()
root.title("Pomodoro Timer")

pomodoro_time = StringVar()
pomodoro_header = StringVar()

pomodoro_time.set("Not Yet Started")
pomodoro_header.set("Not Yet Started")

pomodoro_timer = Timer()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, textvariable=pomodoro_header).grid(column=0, row=0, columnspan=3)

ttk.Label(mainframe, textvariable=pomodoro_time, font=("Arial", 25)).grid(column=0, row=1, columnspan=3)

button_start = ttk.Button(mainframe, text="Start", command=pomodoro_timer.start_timer).grid(column=0, row=2)
button_pause = ttk.Button(mainframe, text="Pause", command=pomodoro_timer.pause_timer).grid(column=1, row=2)
button_stop = ttk.Button(mainframe, text="Reset", command=pomodoro_timer.stop_timer).grid(column=2, row=2)


root.mainloop()
