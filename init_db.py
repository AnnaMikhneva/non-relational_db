
from app import app, equipment, employees
from datetime import datetime
from bson.objectid import ObjectId

def init_test_data():
    # Очистка коллекций
    equipment.delete_many({})
    employees.delete_many({})

    # Добавление тестовых работников
    employee1 = employees.insert_one({
        'full_name': 'Иванов Иван Иванович',
        'position': 'Старший механик',
        'hire_date': datetime(2020, 5, 15),
        'assigned_equipment': []
    }).inserted_id

    employee2 = employees.insert_one({
        'full_name': 'Петров Петр Петрович',
        'position': 'Электроник',
        'hire_date': datetime(2021, 3, 10),
        'assigned_equipment': []
    }).inserted_id

    employee3 = employees.insert_one({
        'full_name': 'Сидорова Анна Михайловна',
        'hire_date': datetime(2022, 1, 20),
        'position': 'Техник',
        'assigned_equipment': []
    }).inserted_id

    # Добавление тестового оборудования
    equipment.insert_many([
        {
            'name': 'Токарный станок X-200',
            'category': 'механика',
            'purchase_date': datetime(2019, 10, 5),
            'status': 'в работе',
            'assigned_employee': None
        },
        {
            'name': 'Осциллограф DS-1054',
            'category': 'электроника',
            'purchase_date': datetime(2020, 2, 15),
            'status': 'в ремонте',
            'assigned_employee': employee1
        },
        {
            'name': 'Компрессор AIR-300',
            'category': 'пневматика',
            'purchase_date': datetime(2021, 5, 20),
            'status': 'на складе',
            'assigned_employee': None
        },
        {
            'name': 'Паяльная станция PS-90',
            'category': 'электроника',
            'purchase_date': datetime(2021, 7, 12),
            'status': 'в ремонте',
            'assigned_employee': employee2
        },
        {
            'name': 'Гидравлический пресс HP-50',
            'category': 'гидравлика',
            'purchase_date': datetime(2022, 1, 8),
            'status': 'в работе',
            'assigned_employee': None
        },
        {
            'name': 'Мультиметр UT-61',
            'category': 'электроника',
            'purchase_date': datetime(2022, 3, 10),
            'status': 'изъято',
            'assigned_employee': None
        },
        {
            'name': 'Фрезерный станок F-100',
            'category': 'механика',
            'purchase_date': datetime(2022, 4, 5),
            'status': 'на складе',
            'assigned_employee': None
        }
    ])

    print("Тестовые данные успешно добавлены!")

if __name__ == '__main__':
    with app.app_context():
        init_test_data()