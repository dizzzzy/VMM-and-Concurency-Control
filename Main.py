from Scheduler import SchedulerThread


def main():
    """
    Main Scheduler thread that spawns the process thread.
    Only 1 ProcessThread at a time.

    """
    main_scheduler_thread = SchedulerThread()
    main_scheduler_thread.start()


if __name__ == '__main__':
    main()
