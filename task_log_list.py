import datetime


class TaskLog():
    def __init__(self, id, start_time, ticket_number=0, comment="EndOfDay"):
        self.id = id
        self._start_time = start_time
        self.logged_time = 0
        self._ticket_number = ticket_number
        self.activity_id = 5
        self._comment = comment

    def __lt__(self, other):
        return self.ticket_number < other.ticket_number
    # def __le__(self, other):
    #     return self.ticket_number <= other.ticket_number
    def __eq__(self, other):
        return self.ticket_number == other.ticket_number and self.comment == other.comment
    # def __ne__(self, other):
    #     return self.ticket_number != other.ticket_number
    # def __gt__(self, other):
    #     return self.ticket_number > other.ticket_number
    # def __ge__(self, other):
    #     return self.ticket_number >= other.ticket_number

    #=== Properties ===
    @property
    def start_time(self):
        return self._start_time

    # @start_time.setter

    @property
    def ticket_number(self):
        return self._ticket_number

    # @ticket_number.setter

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        if self._ticket_number:
            self._comment = comment

    #=== Functions ===    
    def show(self, message_callback=print):
        message_callback("{} : {} {} {} {}".format(self.id,
            self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            self.logged_time, self.ticket_number, self.comment
            ))

    def is_end_of_day(self):
        return self._ticket_number == 0

    def submit_log(self):
        # submit task log to the ticket
        pass

    def merge(self, other_task):
        if not self == other_task:
            return False

        self.logged_time += other_task.logged_time
        return True


class TaskLogList():
    def __init__(self):
        self.tasks = []
        self.tasks_sorted = []

    def append_new(self, start_time, ticket_number, comment):
        if self.is_day_closed():
            print("The day is already closed")
            return False

        if self.tasks and self.tasks[-1].start_time > start_time:
            print("Please specify valid start_time: {} > {}".format(
                self.tasks[-1].start_time.strftime("%Y-%m-%d %H:%M:%S"),
                start_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            return False

        self.tasks.append(TaskLog(len(self.tasks), start_time, ticket_number, comment))
        return True

    def insert_new(self, start_time, ticket_number, comment):
        if self.is_day_closed():
            print("The day is already closed")
            return False

        self.tasks.append(TaskLog(len(self.tasks), start_time, ticket_number, comment))
        self.tasks = sorted(self.tasks, key=lambda task: task.start_time)
        return True

    def remove_task(self, task_id):
        if self.is_day_closed():
            print("The day is already closed")
            return False

        if task_id < len(self.tasks):
            del self.tasks[task_id]
        else:
            print("task_id out of range")

    def close_day(self, time):
        if not self.is_day_closed():
            self.tasks.append(TaskLog(len(self.tasks), time))
            self.calculate_logged_time()
            self.sort()
            return True
        else:
            return False

    def is_day_closed(self):
        if not len(self.tasks):
            return False

        for task in self.tasks:
            if task.is_end_of_day():
                return True

        return False

    def show_tasks(self):
        for task in self.tasks:
            task.show()
        print("")
    
    def show_tasks_sorted(self):
        for tasks_sorted in self.tasks_sorted:
            tasks_sorted.show()
        print("")
    
    def calculate_logged_time(self):
        for n in range(len(self.tasks) - 1):
            self.tasks[n].logged_time = self.tasks[n+1].start_time - self.tasks[n].start_time

    def sort(self):
        self.tasks_sorted = sorted(self.tasks)
        
        n = 0
        while n < len(self.tasks_sorted) - 1:
            n = n + 1

            while n < len(self.tasks_sorted) - 1:
                if self.tasks_sorted[n] == self.tasks_sorted[n+1]:
                    self.tasks_sorted[n].merge(self.tasks_sorted[n+1])
                    del self.tasks_sorted[n+1]
                else:
                    break

        n = -1
        while n < len(self.tasks_sorted) - 1:
            n = n + 1
            if self.tasks_sorted[n].ticket_number <= 0:
                    del self.tasks_sorted[n]
                    n -= 1
    
    def clear(self):
        self.tasks.clear()
        self.tasks_sorted.clear()

    def get_tasks_sorted(self):
        return self.tasks_sorted
