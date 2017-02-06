from flask import Blueprint, request, jsonify, json
create_api = Blueprint('create_api', __name__)

from models import *
from web_app import db

@create_api.route('/user', methods = ["POST"])
def new_user():
    data = request.json
    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return 'ERROR USERNAME ALREADY EXISTS'
    user = User(username=username, password=password,
                first_name = first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    return  "User %s added to database" (username)

@create_api.route('/faculty', methods = ["POST"])
def new_faculty():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    allowed_work_units = data['allowed_word_units']

    faculty = Faculty(first_name=first_name, last_name=last_name,
                        allowed_word_units=allowed_word_units)
    db.session.add(faculty)
    db.session.commit()
    return  "Faculty %s %s added to database" (first_name, last_name)

@create_api.route('/course', methods = ["POST"])
def new_course():
    data = request.json
    number = data['number']
    major = data['major']
    lecture_workload_units = data['lecture_workload_units']
    lecture_hours = data['lecture_hours']
    lab_workload_units = data['lab_workload_units']
    lab_hours = data['lab_hours']

    course = Courses(data=data, number=number, major=major,
                    lecture_workload_units=lecture_workload_units,
                    lecture_hours=lecture_hours,
                    lab_workload_units=lab_workload_units, lab_hours=lab_hours)
    db.session.add(course)
    db.session.commit()
    return  "Course %s %d added to database" % (major, number)

@create_api.route('/term', methods = ["POST"])
def new_term():
    data = request.json
    name = data['name']

    term = Terms(name=name)
    db.session.add(term)
    db.session.commit()
    return "Term %s added to the database" % (name)

@create_api.route('/room', methods = ["POST"])
def new_room():
    data = request.json
    type = data['type']
    capacity = data['capacity']

    room = Rooms(type=type, capacity=capacity)
    return "%s room with capacity %d added to database" % (type, capacity)

@create_api.route('/section', methods = ["POST"])
def new_section():
    data = request.json
    course_id = data['course_id']
    term_id = data['term_id']
    faculty_id = data['faculty_id']
    room_id = data['room_id']
    number = data['number']
    section_type = data['section_type']
    time_start = data['time_start']
    time_end = data['time_end']
    days = data['days']

    course = Courses.query.filter_by(id=course_id).first()
    if course is None:
        return "ERROR COURSE NOT FOUND"
    term = Terms.query.filter_by(id=term_id).first()
    if term in None:
        return "ERROR TERM NOT FOUND"
    faculty = Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        return "ERROR FACULTY NOT FOUND"
    room = ROOMS.query.faculty_by(id=room_id).first()
    if room is None:
        return "ERROR ROOM NOT FOUND"

    section = Sections(course=course, term=term, faculty=faculty,
                        room=room, number=number, section_type=section_type,
                        time_start=time_start, time_end=time_end, days=days)
    db.session.add(section)
    db.session.commit()
    return "Section %d of course %s %d added to database" % (number, course.name, course.number)

@create_api.route('/equipment', methods = ['POST'])
def new_equipment():
    data = request.json
    name = data['name']

    room = Room(name=name)
    db.session.add(room)
    db.session.commit()
    return "Room %s added to database" % (room)

@create_api.route('/roomEquipment', methods = ['POST'])
def new_room_equipment():
    data = request.json
    room_id = data['room_id']
    equipment_id = data['equipment_id']

    room = Rooms.query.filter_by(id=room_id).first()
    if room is None:
        return "ERROR ROOM NOT FOUND"
    equipment = Equipment.query.filter_by(id=equipment_id).first()
    if equipment is None:
        return "ERROR EQUIPMENT NOT FOUND" 

    roomEquipment = RoomEquipment(room=room, equipment=equipment)
    db.session.add(roomEquipment)
    db.session.commit()
    return "%s added to room %s" % (equipment.name, room.type)

@create_api.route('/scheduleFinal', methods = ['POST'])
def new_schedule_final():
    data = request.json
    term_id = data['term_id']
    course_id = data['course_id']
    number_sections = data['number_sections']
    total_enrollment = data['total_enrollment']
    waitlist = data['waitlist']

    term = Terms.query.filter_by(id=term_id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"
    course = Courses.query.filter_by(id=course_id).first()
    if course is None:
        return "ERROR COURSE NOT FOUND"

    sf = ScheduleFinal(term=term, course=course, number_sections=number_sections,
                        total_enrollment=total_enrollment, waitlist=waitlist)
    db.session.add(sf)
    db.session.commit()
    return "ScheduleFinal for term %s and course %s %d added to database" % (term.name, course.major, course.number)

@create_api.route('/scheduleInitial', methods = ['POST'])
def new_schedule_inital():
    data = request.json
    term = data['term']
    section = data['section']

    scheduleInitial = ScheduleInitial(term=term, section=section)
    db.session.add(scheduleInitial)
    db.session.commit()
    return "ScheduleInitial: term %s, section %s" % (term, section)

@create_api.route('publishedSchedule', methods = ['POST'])
def new_published_schedule():
    data = request.json
    term = data['term']

    publishedSchedule = PublishedSchedule(term=term)
    db.session.add(publishedSchedule)
    db.session.commit()
    return "PublishedSchedule: term %s" % (term)

@create_api.route('/facultyPreferences', methods = ['POST'])
def new_faculty_preferences():
    data = request.json()
    faculty_id = data['faculty_id']
    term_id = data['term_id']
    day = data['day']
    time_start = data['time_start']
    time_end = data['time_end']
    preference = data['preference']

    faculty = Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        return "ERROR FACULTY NOT FOUND"
    term = Terms.query.filter_by(id=term.id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"

    fp = FacultyPreferences(faculty=faculty, term=term, day=day,
                            time_start=time_start, time_end=time_end,
                            preference=preference)
    db.session.add(fp)
    db.session.commit()
    return "FacultyPreference added to database"

@create_api.route('/facultyConstraint', methods = ['POST'])
def new_faculty_constraint():
    data = request.json()
    faculty_id = data['faculty_id']
    term_id = data['term_id']
    course_id = data['course_id']
    constraint = data['constraint']

    faculty = Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        return "ERROR FACULTY NOT FOUND"
    term = Terms.query.filter_by(id=term.id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"
    course = Courses.query.filter_by(id=course_id).first()
    if course is None:
        return "ERROR COURSE NOT FOUND"

    fc = facultyConstraint(faculty=faculty, term=term,
                            course=course, constraint=constraint)
    db.session.add(fc)
    db.session.commit()
    return "FacultyConstraint added to db"

@create_api.route('/comment', methods = ['POST'])
def new_comment():
    data = request.json()
    term_id = data['term_id']
    username = data['username']
    comment = data['comment']
    time = data['time']

    term = Terms.query.filter_by(id=term.id).first()
    if term is None:
        return "ERROR TERM NOT FOUND"

    comment = Comment(term=term, username=username,
                        comment=comment, time=time)
    db.session.add(comment)
    db.session.commit()
    return "Comment added to database"

@create_api.route('/notification', methods = ['POST'])
def new_notification():
    data = request.json
    faculty_id = data['faculty_id']
    message = data['message']
    unread = data['unread']
    time = data['time']

    faculty = Faculty.query.filter_by(id=faculty_id).first()
    if faculty is None:
        return "ERROR FACULTY NOT FOUND"

    n = notification(faculty=faculty, message=message,
                        unread=unread, time=time)
    db.session.add(n)
    db.session.commit()
    return "Notification added to database"

