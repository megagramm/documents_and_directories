def main():
    rprint('help - покажет доступные команды')
    while True:
        user_comand = input('Введите команду: ')
        if user_comand == 'p':
            get_man_by_document(input('Укажите номер документа: '))
        elif user_comand == 's':
            get_shelf_by_number(input('Укажите номер документа: '))
        elif user_comand == 'l':
            get_all_documents()
        elif user_comand == 'a':
            add_document(input('Тип документа: '), input('Укажите номер документа: '), input('Укажите Имя: '),
                         input('Укажите название полки: '))
        elif user_comand == 'd':
            delete_document(input('Укажите номер документа: '))
        elif user_comand == 'm':
            move_document(input('Укажите номер документа: '), input('Укажите название полки: '))
        elif user_comand == 'id':
            is_this_a_document(input('Укажите номер документа: '))
        elif user_comand == 'as':
            add_shelf(input('Укажите название полки: '))
        elif user_comand == 'ls':
            list_shelfs()
        elif user_comand == 'ds':
            delete_shelf(input('Укажите полку: '))
        elif user_comand == 'is':
            rprint(is_this_a_shelf(input('Укажите полку: ')))
        elif user_comand == 'help':
            print(help_string)
        elif user_comand == 'q':
            rprint('До новых встречь!')
            break
        else:
            rprint("Команда не распознана")
            rprint('Попробуйте help для вывода справки')


def rprint(string):
    """Формирует вывод текста на экран по правому краю"""
    print(f'{string:>60}')


def rprint_error(string):
    """Формирует вывод текста на экран по правому краю"""
    print(f"{'!!!Ошибка!!!':>60}\n{string:>60}")


documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
      ]
directories = {
        '1': ['2207 876234', '11-2', '5455 028765'],
        '2': ['10006'],
        '3': []
      }
help_string = """
p – people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит;
s – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится;
l– list – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин";
a – add – команда, которая добавит новый документ в каталог и в перечень полок,
    спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться. 
    Корректно обработайте ситуацию, когда пользователь будет пытаться добавить 
    документ на несуществующую полку.
d – delete – команда, которая спросит номер документа и удалит полностью документ из 
    каталога и его номер из перечня полок. Предусмотрите сценарий, когда пользователь 
    вводит несуществующий документ;
m – move – команда, которая спросит номер документа и целевую полку и переместит его 
    с текущей полки на целевую. Корректно обработайте кейсы, когда пользователь пытается 
    переместить несуществующий документ или переместить документ на несуществующую полку;
as – add shelf – команда, которая спросит номер новой полки и добавит ее в перечень. 
    Предусмотрите случай, когда пользователь добавляет полку, которая уже существует.;
is - is this a shelf - проверяет, является ли указанное название полкой;
ls - list directories - Показывает перечень полок и указывает пустые;
"""


def get_man_by_document(document):
    """получаем данные о человеке по документу"""
    for doc in documents:
        if doc['number'] == document:
            rprint("Владелец документа: "+doc['name'])
            return True
    rprint_error("Человек с таким документом не найден")
    return False


def get_shelf_by_number(document):
    """Показывает на какой полке лежит этот документ"""
    if not is_this_a_document(document):
        rprint_error("Документ не существует:")
        return False
    shelf = get_shelf_by_document(document)
    if shelf:
        rprint("Документ " + document + " располагается на полке " + shelf)
        return True
    return False


def get_all_documents():
    """Показывает перечень всех докуметов"""
    rprint('Перечень всех документов')
    for element in documents:
        print(f'\t\t{element["type"]} "{element["number"]}" "{element["name"]}"')
    print()


def add_document(document_type, number, name, shelf):
    """Создает документ"""

    document_types = ['passport', 'invoice', 'insurance']
    # проверяет доступен ли такой тип
    if document_type not in document_types:
        rprint_error("Недоступный тип документов")
        print()
        rprint("Доступные типы документов:")
        print(*document_types, sep='\n')
        print()
        return

    # проверить, существует ли документ
    if is_this_a_document(number):
        rprint_error("Такой документ существует")
        shelf_of_existings_document = get_shelf_by_document(number)
        rprint("Расположен на полке "+shelf_of_existings_document)
        return False

    #  проверка существует ли полка
    if not is_this_a_shelf(shelf):
        rprint_error("Полки не существует")
        return
    documents.append({"type": document_type, "number": number, "name": name})
    directories[shelf].append(number)
    rprint("Документ создан и помещен на полку")


def is_this_a_document(document):
    """Проверяет существует ли такой документ"""
    for doc in documents:
        if doc['number'] == document:
            return True
    return False


def delete_document(document):
    """Удаляет документ из базы и с полки"""

    if not is_this_a_document(document):
        rprint_error("Документа не существует")
        return
    # удаляем документ с полки
    shelf = get_shelf_by_document(document)
    if shelf:
        delete_document_from_shelf(document, shelf)

    for doc in documents:
        if doc['number'] == document:
            documents.remove(doc)
            rprint('Документ удалён')
            return


def delete_document_from_shelf(document, shelf):
    """Удаляет документ с полки"""
    if not is_this_a_shelf(shelf):
        rprint_error("Полка не существует")
        return

    if not is_this_a_document(document):
        rprint_error("Документа не существует")
        return

    if document in directories[shelf]:
        directories[shelf].remove(document)
        rprint('Документ удалён с полки')
        return
    else:
        rprint_error('На указаной полке нет этого документа')


def move_document(document, shelf):
    """перечещает документ на полку"""

    if not is_this_a_shelf(shelf):
        rprint_error("Полка назначения не существует")
        return False

    if not is_this_a_document(document):
        rprint_error("Документа не существует")
        return False

    shelf_source = get_shelf_by_document(document)
    if not shelf_source:
        rprint_error("Документ не привязан ни одной полке")
        return
    else:
        # проверяем не совпадает ли источник и цель назначения
        if shelf_source == shelf:
            rprint_error("Документ уже лежит на этой полке")
            return
        else:
            # создаем документ в указанной полке, удаляем документ в текущей полке
            directories[shelf_source].remove(document)
            directories[shelf].append(document)
            rprint('Документ перемещён')
            return


def get_shelf_by_document(document):
    """возвращает название полки или False"""
    for shelf, items in directories.items():
        if document in items:
            return shelf


def is_this_a_shelf(shelf):
    """Проверяет существует ли полка"""
    return shelf in directories


def add_shelf(shelf):
    """Добавляет полку"""
    if not is_this_a_shelf(shelf):
        directories[shelf] = []
        rprint('Полка добавлена')
        return
    else:
        rprint_error('Уже существует')


def delete_shelf(shelf):
    """Удаляет полку"""
    if is_this_a_shelf(shelf):
        if len(directories[shelf]) == 0:
            directories.pop(shelf)
            rprint('Полка удалена')
            return
        else:
            rprint_error('Полка не пустая.')
            rprint('Сначала перенесите все')
            rprint('документы или удалите')
            return
    else:
        rprint_error('Полки не существует')


def list_shelfs():
    """Показывает перечень полок и указать пустые"""
    rprint('Перечень полок')
    for key, values in directories.items():
        if len(values) == 0:
            empty_shelf = 'Пустая'
        else:
            empty_shelf = '      '
        print(f'Полка: {empty_shelf} {key} документы: {values}')
    print()


main()
