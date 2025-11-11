from sqlalchemy import create_engine, Column, Integer, String, Date, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['RemindersRepositoryORM']

Base = declarative_base()

class Reminder(Base):
    __tablename__ = 'reminders'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    date = Column(Date)

    def __repr__(self):
        return f"<Reminder(id= {id}, name={self.name}, address={self.address}, date={self.date})>"
    
class RemindersRepositoryORM:
    def __init__(self, database_path):
        engine = create_engine(f'sqlite:///{database_path}')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_by_id(self, reminder_id):
        return self.session.query(Reminder).filter_by(id=reminder_id).first()
    
    def get_all(self):
        return self.session.scalars(select(Reminder)).all()

    def add_reminder(self, reminder_data):
        new_reminder = Reminder( 
            name=reminder_data["name"],
            address=reminder_data["address"],
            date=reminder_data["date"]
        )
        self.session.add(new_reminder)
        self.session.commit()

    def delete(self, reminder_id):
        reminder_to_delete = self.get_by_id(reminder_id)
        if reminder_to_delete:
            self.session.delete(reminder_to_delete)
            self.session.commit()