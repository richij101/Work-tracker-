from . import db
from sqlalchemy import Date # Ensure Date type is imported

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(Date, nullable=False)
    end_date = db.Column(Date, nullable=False)
    entry_type = db.Column(db.String(50), nullable=False)  # "work_land", "work_ship", "vacation", "travel"
    location = db.Column(db.String(100), nullable=True) # Country for work_land, Ship Name for work_ship

    def __repr__(self):
        if self.start_date == self.end_date:
            date_repr = self.start_date.strftime('%Y-%m-%d')
        else:
            date_repr = f"{self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}"
        return f'<TimeEntry {date_repr} - {self.entry_type} - {self.location or "N/A"}>'
