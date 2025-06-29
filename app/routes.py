from flask import render_template, request, redirect, url_for, flash, current_app
from . import db
from .models import TimeEntry
from datetime import datetime, timedelta

@current_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        entry_type = request.form.get('entry_type')
        location = request.form.get('location', None) # Optional, get '' if not present

        # Basic Validation
        if not start_date_str or not entry_type:
            flash('Start date and entry type are required.', 'error')
            return redirect(url_for('index'))

        if entry_type == 'work' and not location:
            flash('Location is required for "Work" entries.', 'error')
            return redirect(url_for('index'))

        if entry_type != 'work': # Ensure location is null if not a work entry
            location = None

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            # If end_date is not provided or empty, use start_date
            end_date = start_date
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            if end_date < start_date:
                flash('End date cannot be before start date.', 'error')
                return redirect(url_for('index'))

        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('index'))

        # Create entries for the date range
        current_date = start_date
        while current_date <= end_date:
            new_entry = TimeEntry(
                entry_date=current_date,
                entry_type=entry_type,
                location=location if entry_type == 'work' else None
            )
            db.session.add(new_entry)
            current_date += timedelta(days=1)

        try:
            db.session.commit()
            flash('Entries added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving entries: {str(e)}', 'error')

        return redirect(url_for('index'))

    # For GET request, fetch entries and calculate summaries
    entries = TimeEntry.query.order_by(TimeEntry.entry_date.desc()).all()

    total_worked_days = 0
    total_vacation_days = 0
    total_travel_days = 0
    work_days_by_location = {}

    for entry in entries:
        if entry.entry_type == 'work':
            total_worked_days += 1
            if entry.location: # Should always be true for work, but good practice
                work_days_by_location[entry.location] = work_days_by_location.get(entry.location, 0) + 1
        elif entry.entry_type == 'vacation':
            total_vacation_days += 1
        elif entry.entry_type == 'travel':
            total_travel_days += 1

    summaries = {
        'total_worked_days': total_worked_days,
        'total_vacation_days': total_vacation_days,
        'total_travel_days': total_travel_days,
        'work_days_by_location': work_days_by_location
    }

    return render_template('index.html', entries=entries, summaries=summaries)
