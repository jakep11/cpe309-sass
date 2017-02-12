from flask import Blueprint, request, jsonify, json
from sqlalchemy import and_
import sys


# blueprint url prefix = "/filter"
filters_api = Blueprint('filters_api', __name__)

from models import *

# grab filtered courses
@filters_api.route('/courses', methods = ["GET"])
def filtered_courses():
   courses = Courses.query.all()
   return jsonify([i.serialize for i in courses])

# grab filtered sections
@filters_api.route('/sections', methods = ["POST"])
def filtered_sections():
   data = request.json
   ids = data['ids']
   instructors = data['instructors']
   startTimes = data['time_start']
   endTimes = data['time_end']

   filters = []

   if ids:
      filters.append(Sections.course_id.in_(ids))
   if instructors:
      filters.append(Sections.faculty_id.in_(instructors))
   if startTimes:
      filters.append(Sections.time_start.in_(startTimes))
   if endTimes:
      filters.append(Sections.time_end.in_(endTimes))

   #sections = None

   if not filters:
      sections = Sections.query.all()
   else:
      sections = Sections.query.filter(and_(*filters)).all()

   print(len(filters))
   sys.stdout.flush()

   return jsonify([i.serialize for i in sections])