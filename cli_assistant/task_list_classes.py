from datetime import datetime
import pickle


class ResponsiblePerson:
    """Клас для створення відповідальної особи"""

    def __init__(self, name):
        self.name = name.title()

    def __str__(self):
        return self.name


class Task:
    """Клас для створення завдання"""

    def __init__(self, text: str, person: ResponsiblePerson, deadline):
        self.text = text.capitalize()
        self.person = person

        d, m, y = deadline.split("/")
        self.deadline = datetime(
            year=int(y), month=int(m), day=int(d), hour=23, minute=59, second=59
        )

        self.status = "in process"

    def is_in_time(self):
        """функція перевіряє статус виконання на момент визову"""

        today = datetime.now()
        if self.status != "done":
            if today > self.deadline:
                self.status = "FAIL"
            else:
                self.status = "in process"

    def see_task(self):
        """Виводимо всю актуальну інформацію по завданню в консоль"""

        self.is_in_time()
        return f"\nResponsible Person: {self.person.name}      Deadline: {self.deadline.date()}\nTask: {self.text}\nStatus: {self.status}\n==============\n"


class TaskList:
    """Клас для створення списку завдань"""

    cnt = 0

    def __init__(self):
        self.task_lst = {}
        self.read_fr_file()

    def add_task(self, task: Task):
        """Додаємо нове завдання"""

        self.task_lst[self.cnt + 1] = task
        self.cnt += 1
        self.save_to_file()

    def remove_task(self, ID):
        """Видаляємо завдання по ID"""

        if int(ID) in self.task_lst:
            self.task_lst.pop(int(ID))
            self.save_to_file()

    def show_all_tasks(self):
        """Виводимо перелік всіх завдань"""

        result = " "
        if len(self.task_lst) > 0:
            for k, v in self.task_lst.items():
                result += f"=== ID: {k} === {v.see_task()}\n"
            return result
        else:
            return f"\nTask book is empty.\n"

    def change_deadline(self, ID, new_deadline):
        """Змінюємо термін виконання завдання по ID"""

        d, m, y = new_deadline.split("/")
        new_deadline = datetime(year=int(y), month=int(m), day=int(d))

        if int(ID) in self.task_lst:
            self.task_lst[int(ID)].deadline = new_deadline
            self.save_to_file()

    def search_task(self, text_to_search):
        """Шукаємо завдання по тексту"""

        for task in self.task_lst.values():
            if text_to_search.strip().lower() in task.text.lower():
                print(task.see_task())

    def search_respons_person(self, responsible_person: str):
        """Шукаємо всі завдання, за які відповідає/відповідала особа"""

        result = "\n"
        for id, task in self.task_lst.items():
            if responsible_person.title() == task.person.name:
                result += f"ID: {int(id)}\n{task.see_task()})"
        return result

    def set_done(self, id):
        """Змінюємо статус виконання на DONE"""

        if int(id) in self.task_lst:
            self.task_lst[int(id)].status = "done"
            self.save_to_file()
            return f"\nStatus task ID: {int(id)} changed!\n"
        else:
            return f"\nThe task with ID: {int(id)} isn't exist!\n"

    def save_to_file(self):
        """Зберігаємо книгу у pickle-файл"""

        with open("tasks.bin", "wb") as fh:
            pickle.dump(self.task_lst, fh)

    def read_fr_file(self):
        """зчитуємо книгу з pickle-файла"""

        try:
            with open("tasks.bin", "rb") as fh:
                self.task_lst = pickle.load(fh)
                if self.task_lst:
                    self.cnt = max(self.task_lst.keys())
        except FileNotFoundError:
            self.task_lst = {}
            self.cnt = 0


tasklist = TaskList()
