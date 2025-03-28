# non-relational_db for equipment
## Структура базы данных

База будет содержать 2 коллекции:

1. `equipment` - оборудование предприятия
2. `employees` - ремонтные работники

### Коллекция `equipment`

Каждый документ представляет единицу оборудования и содержит:

- `_id` - уникальный идентификатор (ObjectId)
- `name` - название оборудования
- `category` - категория (например, "электроника", "механика")
- `purchase_date` - дата поступления
- `status` - текущий статус ("на складе", "в работе", "в ремонте", "изъято")
- `assigned_employee` - ID работника, если оборудование в ремонте (может быть null)

### Коллекция `employees`

Каждый документ представляет работника и содержит:

- `_id` - уникальный идентификатор (ObjectId)
- `full_name` - ФИО работника
- `hire_date` - дата приема на работу
- `position` - должность
- `assigned_equipment` - массив ID оборудования, назначенного на ремонт
