from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentSubmitSchema

principal_assignments_resources = Blueprint('principal', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'])
@decorators.authenticate_principal
def list_assignments(p):
    assignments = Assignment.get_submitted_and_graded()
    assignment_schema = AssignmentSchema(many=True)
    result = assignment_schema.dump(assignments)
    return jsonify({'data': result})

