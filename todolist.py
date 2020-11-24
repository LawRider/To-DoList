from datetime import datetime, timedelta, date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import sessionmaker
import sys

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=date.today())

    def __repr__(self):
        return self.task


class ToDoApp:
    menu = "\n1) Today's tasks\n" \
           "2) Week's tasks\n" \
           "3) All tasks\n" \
           "4) Missed tasks\n" \
           "5) Add task\n" \
           "6) Delete task\n" \
           "0) Exit"

    def __init__(self):
        self.create_database()
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        self.start()

    @staticmethod
    def create_database():
        # if exists, it does nothing
        Base.metadata.create_all(engine)

    def start(self):
        while True:
            print(self.menu)
            choice = input()
            if choice == '1':
                self.print_todays_tasks()
            elif choice == '2':
                self.print_weeks_tasks()
            elif choice == '3':
                self.print_all_tasks()
            elif choice == '4':
                self.print_missed_tasks()
            elif choice == '5':
                self.add_task()
            elif choice == '6':
                self.delete_task()
            else:
                print('\nBye!')
                sys.exit()

    def show_all(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        for row in rows:
            print(f"{row.id}. {row.task}. {row.deadline.strftime('%d %b')}")
        return rows

    def print_todays_tasks(self):
        print(f"\nToday {datetime.strftime(datetime.today(), '%d %b')}:")
        rows = self.session.query(Table).filter(Table.deadline == date.today()).all()
        if not rows:
            print("Nothing to do!")
        else:
            for row in rows:
                print(f"{row.id}. {row.task}")

    def print_weeks_tasks(self):
        today = datetime.today()
        date_list = [today + timedelta(days=x) for x in range(7)]
        for i in date_list:
            print(f"\n{i.date().strftime('%A %d %b')}:")
            rows = self.session.query(Table).filter(Table.deadline ==
                                                    i.date().strftime('%Y-%m-%d')).all()
            if not rows:
                print("Nothing to do!")
            else:
                for row in rows:
                    print(f"{row.id}. {row.task}")

    def print_all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print('All tasks:')
        if rows:
            for i, task in enumerate(rows, start=1):
                date_frt = datetime.strftime(task.deadline, '%e %b').strip()
                print(f"{i}. {task}. {date_frt}")
        else:
            print('Nothing to do!')

    def print_missed_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline < date.today()). \
            order_by(Table.deadline).all()
        print("\nMissed tasks:")
        if not rows:
            print("Nothing is missed!")
        else:
            for row in rows:
                print(f"{row.id}. {row.task}. {row.deadline.strftime('%d %b')}")

    def add_task(self):
        task_name = input("\nEnter task\n")
        deadline_date = input("Enter deadline\n")
        new_row = Table(task=task_name,
                        deadline=datetime.strptime(deadline_date, '%Y-%m-%d').date())
        self.session.add(new_row)
        self.session.commit()
        print("The task has been added!")

    def delete_task(self):
        print("\nChoose the number of the task you want to delete:")
        rows = self.show_all()
        if not rows:
            print('Nothing to delete')
        else:
            to_delete = int(input())
            row_to_delete = rows[to_delete - 1]
            if row_to_delete:
                self.session.delete(row_to_delete)
                self.session.commit()
                print('The task has been deleted!')


if __name__ == "__main__":
    app = ToDoApp()
