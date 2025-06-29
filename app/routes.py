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

        location_detail = None # This will store country or ship name

        # Validation for start_date and entry_type
        if not start_date_str or not entry_type:
            flash('Start date and a valid entry type are required.', 'error')
            return redirect(url_for('index'))

        if entry_type == 'work_land':
            location_detail = request.form.get('country')
            if not location_detail:
                flash('Country is required for "Work Land" entries.', 'error')
                return redirect(url_for('index'))
        elif entry_type == 'work_ship':
            location_detail = request.form.get('ship_name')
            if not location_detail:
                flash('Ship Name is required for "Work Ship" entries.', 'error')
                return redirect(url_for('index'))
        elif entry_type not in ['vacation', 'travel']:
            flash('Invalid entry type selected.', 'error')
            return redirect(url_for('index'))

        try:
            parsed_start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            parsed_end_date = parsed_start_date # Default end_date to start_date
            if end_date_str:
                parsed_end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            if parsed_end_date < parsed_start_date:
                flash('End date cannot be before start date. Setting end date to start date.', 'warning') # Or 'error' and redirect
                parsed_end_date = parsed_start_date # Correcting it, or could be an error

        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('index'))

        # Create a single entry for the period
        new_entry = TimeEntry(
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            entry_type=entry_type,
            location=location_detail # This now holds country or ship_name, or None
        )
        db.session.add(new_entry)

        try:
            db.session.commit()
            flash('Entries added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving entries: {str(e)}', 'error')

        return redirect(url_for('index'))

    # For GET request, fetch entries and calculate summaries
    entries = TimeEntry.query.order_by(TimeEntry.start_date.desc()).all()

    total_work_land_days = 0
    total_work_ship_days = 0
    total_vacation_days = 0
    total_travel_days = 0
    work_land_days_by_country = {} # Specific for work_land entries

    for entry in entries:
        # Calculate duration of the entry
        duration = (entry.end_date - entry.start_date).days + 1

        if entry.entry_type == 'work_land':
            total_work_land_days += duration
            if entry.location: # Location stores country
                work_land_days_by_country[entry.location] = work_land_days_by_country.get(entry.location, 0) + duration
        elif entry.entry_type == 'work_ship':
            total_work_ship_days += duration
            # Ship work days are not added to work_land_days_by_country
        elif entry.entry_type == 'vacation':
            total_vacation_days += duration
        elif entry.entry_type == 'travel':
            total_travel_days += duration

    summaries = {
        'total_work_land_days': total_work_land_days,
        'total_work_ship_days': total_work_ship_days,
        'total_vacation_days': total_vacation_days,
        'total_travel_days': total_travel_days,
        'work_land_days_by_country': work_land_days_by_country
    }

    return render_template('index.html', entries=entries, summaries=summaries)


@current_app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    entry_to_edit = TimeEntry.query.get_or_404(entry_id)

    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        entry_type = request.form.get('entry_type')
        location_detail = None

        if not start_date_str or not entry_type:
            flash('Start date and a valid entry type are required.', 'error')
            # Re-render edit form with error, passing entry back
            return render_template('edit_entry.html', entry=entry_to_edit)

        if entry_type == 'work_land':
            location_detail = request.form.get('country')
            if not location_detail:
                flash('Country is required for "Work Land" entries.', 'error')
                return render_template('edit_entry.html', entry=entry_to_edit)
        elif entry_type == 'work_ship':
            location_detail = request.form.get('ship_name')
            if not location_detail:
                flash('Ship Name is required for "Work Ship" entries.', 'error')
                return render_template('edit_entry.html', entry=entry_to_edit)
        elif entry_type not in ['vacation', 'travel']:
            flash('Invalid entry type selected.', 'error')
            return render_template('edit_entry.html', entry=entry_to_edit)

        try:
            parsed_start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            parsed_end_date = parsed_start_date
            if end_date_str:
                parsed_end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            if parsed_end_date < parsed_start_date:
                flash('End date cannot be before start date. Correcting to single day.', 'warning')
                parsed_end_date = parsed_start_date

        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return render_template('edit_entry.html', entry=entry_to_edit)

        # Update entry fields
        entry_to_edit.start_date = parsed_start_date
        entry_to_edit.end_date = parsed_end_date
        entry_to_edit.entry_type = entry_type
        entry_to_edit.location = location_detail

        try:
            db.session.commit()
            flash('Entry updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating entry: {str(e)}', 'error')
            return render_template('edit_entry.html', entry=entry_to_edit)

    # GET request:
    return render_template('edit_entry.html', entry=entry_to_edit)


@current_app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry_to_delete = TimeEntry.query.get_or_404(entry_id)
    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        flash('Entry deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting entry: {str(e)}', 'error')
    return redirect(url_for('index'))
