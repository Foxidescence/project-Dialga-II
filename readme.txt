Staff Shift Management System

A command-line interface application to manage staff shifts and a work roster.
The app allows an administrator to schedule shifts and view reports, while staff members can 
log their time in and out.

Features
-(Admin) Schedule a staff member shifts for the week
-(Staff) View combined roster of all staff
-(Staff) Time in/out at the start/end of the shifts
-(Admin) View shift report for the week

Commands
-flask init - initializes the system; must be run before any other command to have sample
            users to work with.
-flask create-shift - schedules a shift for a staff member; an admin user must be selected
            for this to work.
-flask log-time - logs the actual time a staff member entered and left their shift
-flask view-roster - shows the combined roster for the week, or all the shifts scheduled for the week
-flask view-shift-reports - shows the shifts that a staff member has for the week; an admin
            user must be selected for this to work