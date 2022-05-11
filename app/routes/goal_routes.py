from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.goal import Goal
from .helpers import validate_goal, validate_task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    new_goal = Goal.from_json(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_json()}), 201


@goals_bp.route("", methods=["GET"])
def read_goals():
    Goals = Goal.query.all()

    goals_response = [goal.to_json() for goal in Goals]
        
    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return jsonify({"goal": goal.to_json()}), 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.update_goal(request_body)

    db.session.commit()

    return jsonify({"goal": goal.to_json()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details":f'Goal {goal_id} "{goal.title}" successfully deleted'} ), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    task_list = []
    for task_id in request_body["task_ids"]:
        task = validate_task(task_id)
        task_list.append(task)
    # task_list = link_tasks_to_goal(request_body)
    goal.tasks = task_list

    db.session.commit()
    return jsonify({"id": 1, "task_ids": [1, 2, 3]})


