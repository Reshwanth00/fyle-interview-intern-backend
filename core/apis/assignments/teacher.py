from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment , AssignmentStateEnum , GradeEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments that are submitted or graded"""
    # Fetch assignments by teacher ID and filter by state
    teachers_assignments = Assignment.filter(
        Assignment.teacher_id == p.teacher_id,
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()
    
    # Serialize the assignments
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    
    # Return the response
    return APIResponse.respond(data=teachers_assignments_dump)
@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    
    if grade_assignment_payload.grade not in GradeEnum.__members__.values():
        return APIResponse.respond_error('ValidationError', 400)
    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    if assignment is None:
        return APIResponse.respond_error('FyleError', 404)
    if assignment.teacher_id != p.teacher_id:
        return APIResponse.respond_error('FyleError',400)
    if assignment.state != AssignmentStateEnum.SUBMITTED:
        return APIResponse.respond_error('FyleError', 400)
    
    # Proceed with grading the assignment
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
