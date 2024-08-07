from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentSubmitSchema, TeacherSchema

principal_assignments_resources = Blueprint('principal', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'])
@decorators.authenticate_principal
def list_assignments(p):
    assignments = Assignment.get_submitted_and_graded()
    assignment_schema = AssignmentSchema(many=True)
    result = assignment_schema.dump(assignments)
    return jsonify({'data': result})


@principal_assignments_resources.route('/teachers', methods=['GET'])
@decorators.authenticate_principal
def list_teachers(p):
    teachers = Teacher.get_all_teachers()
    teacher_schema = TeacherSchema(many=True)
    result = teacher_schema.dump(teachers)

    # Return the result as JSON response
    return jsonify({'data': result})

