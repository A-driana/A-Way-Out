from rocketry import Rocketry
from rocketry.args import Session, Task
from app.mail import send_mail
from app.model import User, TodoDB, Notification
from app.db import SessionLocal
import datetime as _date

schedule = Rocketry(execution="async")


@schedule.task('every 90 seconds')
async def send_notification() -> None:
    db = SessionLocal()
    due_todos = db.query(TodoDB).filter(TodoDB.reminder <= _date.datetime.utcnow(), TodoDB.sent_alert == False).all()
    if due_todos:
        for todo in due_todos:
            msg = f'This is to reminder you that {todo.title} ({todo.id}) has not yet been completed'
            user = db.query(User).filter(User.id == todo.user_id).first()
            user_email = user.email
            send_mail(msg, user_email)
            todo.sent_alert = True
            new_alert = Notification(
                message=msg,
                user_id=todo.user_id
            )
            new_alert.todo = todo
            db.add(new_alert)
            db.commit()
            db.refresh(new_alert)


@schedule.task(execution='thread')
def read_task(task: Task(send_notification)):
    print(task)


@schedule.task(execution='thread')
def read_logs(session: Session()):
    task = session['send_notification']

    run_logs = task.logger.filter_by(action='run').all()
    success_logs = task.logger.filter_by(action='success').all()
    fail_logs = task.logger.filter_by(action='fail').all()


if __name__ == "__main__":
    schedule.run()
