from flask import Flask, render_template, request, redirect, url_for
import pymongo
print(pymongo.__version__)
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

# Подключение к MongoDB
from pymongo.server_api import ServerApi


client = MongoClient('mongodb://localhost:27017/')
db = client['equipment_management']
equipment = db['equipment']
employees = db['employees']


@app.route('/')
def index():
    # Получаем все оборудование с информацией о работниках
    equipment_list = list(equipment.aggregate([
        {
            '$lookup': {
                'from': 'employees',
                'localField': 'assigned_employee',
                'foreignField': '_id',
                'as': 'employee_info'
            }
        },
        {'$unwind': {'path': '$employee_info', 'preserveNullAndEmptyArrays': True}}
    ]))

    # Получаем всех работников
    employees_list = list(employees.find())

    return render_template('index.html',
                           equipment=equipment_list,
                           employees=employees_list,
                           statuses=['на складе', 'в работе', 'в ремонте', 'изъято'])


@app.route('/add_employee', methods=['POST'])
def add_employee():
    # Добавление нового работника
    employees.insert_one({
        'full_name': request.form['full_name'],
        'position': request.form['position'],
        'hire_date': datetime.now(),
        'assigned_equipment': []
    })
    return redirect(url_for('index'))


@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    # Добавление нового оборудования
    equipment.insert_one({
        'name': request.form['name'],
        'category': request.form['category'],
        'purchase_date': datetime.now(),
        'status': 'на складе',
        'assigned_employee': None
    })
    return redirect(url_for('index'))


@app.route('/update_status', methods=['POST'])
def update_status():
    # Обновление статуса оборудования
    equip_id = ObjectId(request.form['equip_id'])
    new_status = request.form['status']

    update_data = {'status': new_status}

    # Если статус "в ремонте", назначаем работника
    if new_status == 'в ремонте' and 'employee_id' in request.form:
        employee_id = ObjectId(request.form['employee_id'])
        update_data['assigned_employee'] = employee_id

        # Добавляем оборудование в список работника
        employees.update_one(
            {'_id': employee_id},
            {'$addToSet': {'assigned_equipment': equip_id}}
        )
    elif new_status != 'в ремонте':
        # Если статус изменился с "в ремонте", убираем назначение
        equipment.update_one(
            {'_id': equip_id},
            {'$set': {'assigned_employee': None}}
        )

    equipment.update_one(
        {'_id': equip_id},
        {'$set': update_data}
    )

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)