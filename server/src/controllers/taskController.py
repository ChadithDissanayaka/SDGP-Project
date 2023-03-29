import json
import os
from datetime import datetime

from bson.objectid import ObjectId
from flask import Blueprint, request

from config import db
from src.models.taskModel import Task
from src.controllers.userController import find_all

taskCtrl = Blueprint('task', __name__)


@taskCtrl.route('/create', methods=['POST'])
def create_task():
    form = request.form
    data = json.loads(form['data'])

    if 'attachment' in request.files:
        file = request.files['attachment']

        filename = file.filename
        file.save(os.path.join(os.environ['UPLOAD_FOLDER'], filename))
    else:
        filename = None
    task = Task(data["userId"], data["taskName"], data["desc"],
                data["submissionDate"], filename)

    result = db.tasks.insert_one(task.__dict__)

    return json.dumps({'taskId': result.inserted_id}, default=str)



