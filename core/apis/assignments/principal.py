from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentSubmitSchema, TeacherSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'])
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    assignments = Assignment.get_submitted_and_graded()
    assignment_schema = AssignmentSchema(many=True)
    result = assignment_schema.dump(assignments)
    return APIResponse.respond(data=result)


@principal_assignments_resources.route('/teachers', methods=['GET'])
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of teachers"""
    teachers = Teacher.get_all_teachers()
    teacher_schema = TeacherSchema(many=True)
    result = teacher_schema.dump(teachers)
    return APIResponse.respond(data=result)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or Re-grade an assignment"""
    assignment_data = AssignmentGradeSchema().load(incoming_payload)
    assignment_id = getattr(assignment_data, 'id', None)
    grade = incoming_payload.get('grade', None)
    if not assignment_id or not grade:
        return APIResponse.respond(data={'error': 'Invalid data provided'}), 400
    assignment = Assignment.get_by_id(assignment_id)
    if not assignment:
        return APIResponse.respond(data={'error': 'Assignment not found'}), 404
    if assignment.state == AssignmentStateEnum.DRAFT:
        return APIResponse.respond(data={'error': 'Draft assignments cannot be graded'}), 400
    assignment.grade = grade
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()
    assignment_schema = AssignmentSchema()
    result = assignment_schema.dump(assignment)
    return APIResponse.respond(data=result)
