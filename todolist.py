from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def show_all(sess):
    rows = sess.query(Table).order_by(Table.deadline).all()
    for row in rows:
        print(f"{row.id}. {row.task}. {row.deadline.strftime('%d %b')}")
    return rows


def menu():
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    today = datetime.today()
    print("1) Today's tasks",
          "2) Week's tasks",
          "3) All tasks",
          "4) Missed tasks",
          "5) Add task",
          "6) Delete task",
          "0) Exit",
          sep='\n')
    choice = int(input())
    if choice == 1:
        print(f"\nToday {today.strftime('%d %b')}:")
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if not rows:
            print("Nothing to do!")
        else:
            for row in rows:
                print(f"{row.id}. {row.task}")
        print()

    elif choice == 2:
        date_list = [today + timedelta(days=x) for x in range(7)]
        for i in date_list:
            print(f"\n{i.date().strftime('%A %d %b')}:")
            rows = session.query(Table).filter(Table.deadline ==
                                               i.date().strftime('%Y-%m-%d')).all()
            if not rows:
                print("Nothing to do!")
            else:
                for row in rows:
                    print(f"{row.id}. {row.task}")
        print()

    elif choice == 3:
        print("\nAll tasks:")
        if not show_all(session):
            print("Nothing to do!")
        print()

    elif choice == 4:
        rows = session.query(Table).filter(Table.deadline < today.date()).\
            order_by(Table.deadline).all()
        print("\nMissed tasks:")
        if not rows:
            print("Nothing is missed!")
        else:
            for row in rows:
                print(f"{row.id}. {row.task}. {row.deadline.strftime('%d %b')}")
        print()

    elif choice == 5:
        task_name = input("\nEnter task\n")
        deadline_date = input("Enter deadline\n")
        new_row = Table(task=task_name,
                        deadline=datetime.strptime(deadline_date, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")

    elif choice == 6:
        print("\nChoose the number of the task you want to delete:")
        rows = show_all(session)
        if not rows:
            print("Nothing to delete")
        else:
            task_num = int(input())
            rows = session.query(Table).filter(Table.id == task_num).all()
            session.delete(rows[0])
            session.commit()
            print("The task has been deleted!")
        print()

    elif choice == 0:
        print("\nBye!")
        exit()

    else:
        print("The operation cannot be performed.\n")


def main():
    while True:
        menu()


if __name__ == "__main__":
    main()
