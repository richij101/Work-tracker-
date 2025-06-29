from . import db
from sqlalchemy import Date # Ensure Date type is imported

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(Date, nullable=False) # Storing individual dates
    entry_type = db.Column(db.String(50), nullable=False)  # "work", "vacation", "travel"
    location = db.Column(db.String(100), nullable=True) # Nullable because only for 'work'

    def __repr__(self):
        return f'<TimeEntry {self.entry_date} - {self.entry_type} - {self.location or ""}>'
