from Scheduler import SchedulerThread

"""
Main Scheduler thread that spawns the process thread.
Only 1 ProcessThread at a time.

"""
main_scheduler_thread = SchedulerThread()
main_scheduler_thread.start()

