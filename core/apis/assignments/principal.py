from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema

principle_assignments_resources = Blueprint('principle_assignments_resources', __name__)

@principle_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """List all submitted and graded assignments"""
    assignments = Assignment.filter(
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()

    principle_assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=principle_assignments_dump)

@principle_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """List all the teachers"""
    teachers = Assignment.get_all_teachers()
    principal_teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=principal_teachers_dump)


@principle_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    assignment_data = AssignmentGradeSchema().load(incoming_payload)


    # Fetch assignment by ID
    assignment = Assignment.get_by_id(assignment_data.id)

    if assignment is None:
        return APIResponse.respond_error('Assignment not found', 400)

    # Check if the assignment is in a state that cannot be graded
    if assignment.state == AssignmentStateEnum.DRAFT:
        return APIResponse.respond_error('Assignment in draft state cannot be graded', 400)

    if assignment.state not in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]:
        return APIResponse.respond_error('Only submitted or graded assignments can be graded', 400)

    # Grade the assignment
    assignment.grade = assignment_data.grade
    assignment.state = AssignmentStateEnum.GRADED
    
    # Commit the transaction
    db.session.commit()

    # Serialize the graded assignment
    graded_assignment_dump = AssignmentSchema().dump(assignment)
    
    # Return the response
    return APIResponse.respond(data=graded_assignment_dump)

