import pandas as pd
import re
from .md_notif import *


# Логика
def get_size(df, settings):
    start = settings["sRow"]
    checkCol = df.iloc[start:, 2]
    
    emptyStreak = 0
    dataIndex = 0

    for i, cell in enumerate(checkCol.values):
        if pd.isna(cell):
            emptyStreak += 1
            if emptyStreak >= settings["maxEmpty"]:
                break
        else:
            emptyStreak = 0
            dataIndex = i + 1
            
    if dataIndex == 0:
        msg_warning("No data found")
    
    return start + dataIndex

def get_sheets(path):
    file = pd.ExcelFile(path)
    if not file:
       msg_error("No file found")
    sheets = file.sheet_names
    
    if not sheets:
        msg_warning("No sheets found")

    return sheets

# Исполнитель
def get_data_vertical(path, cols, sRow=0, maxEmpty=5):
    settings = {
        "cols":cols,
        "sRow":sRow,
        "maxEmpty":maxEmpty
    }
    if cols < 1:
        msg_error("Columns must be > 0!")
        return None

    sheets = get_sheets(path)    

    # msg_info(sheets)

    data = []   # массив данных для каждого дня
    for sheet in sheets:
        df = pd.read_excel(
                path, 
                sheet_name=sheet,
                header=sRow
            )
        attributes = df.columns[:cols].tolist()
        msg_info(f"Found attributes: {attributes}")

        endIndex = get_size(df=df, settings=settings)

        if endIndex > 0:
            final_df = df.iloc[:endIndex, :cols]
            msg_info(f"Sheet '{sheet}': grabbed {endIndex} rows")
            for i, row in final_df.iterrows():
                if i >= endIndex:
                    break
                task = dict(zip(attributes,row[:cols].tolist()))
                task["day"] = sheet
                data.append(task)
            
    return data

def data_clear_empty(data):
    cleaned = [] # Создаем временную корзину

    for task in data:
        counter = 0
        for key, value in task.items():
            if key != "day":
                if pd.isna(value):
                    counter += 1
        
        if counter < 2:
            cleaned.append(task)

    return cleaned

def parse_float(raw):
    if pd.isna(raw):
        return 0.0, ""
    
    text = str(raw).strip()         
    text = text.replace(",",".")    # , -> .

    match = re.match(r"^(\d+(?:\.\d+)?)\s*(.*)$", text)  # RegEx for check two groups
    # 1 - float
    # 2 - unit 

    if match:   # if we have our groups
        try:
            amount = float(match.group(1))  # parse amount
            unit = match.group(2).strip()  # just copy 2 group
            return amount, unit 
        except ValueError:
            pass

    return 0.0, text

def daily_count(data, refCol, matCol, countCol):
    if not data:
        msg_warning("No data provided!")
        return {}
    
    # Create needy dictionary
    task_distinct = {}

    # main thing
    for task in data:
        # get all values from task. Like "LV" "Material" and other
        values = list(task.values())
        try:
            lv = values[refCol]     # get all from previously defined column 
            material = values[matCol]   # same 
            count_raw = values[countCol] # same
            day = task.get("day")
        except IndexError:  
            continue

        if pd.isna(lv):
            continue

        # parse data to put in future
        count, unit = parse_float(count_raw)

        # clear raw data
        lv_clean = str(lv).strip()          # extract clean LV to proceed further
        mat_clean = str(material).strip()   # same way
        day_clean = str(day).strip()

        # create complete expr
        unique_key = (day_clean, lv_clean, mat_clean)

        # check expr
        # check whole thing in dictionary . If new - create
        if unique_key not in task_distinct:     
            task_distinct[unique_key] = {
                "Count": count,
                "Unit": unit
            }
        else:                                   
            # if not new - add
            task_distinct[unique_key]["Count"] += count
    sorted_distinct = dict(sorted(task_distinct.items(), key=lambda x: x[0][1]))
    # x = (  (day, lv, mat),  {'Count': 10, 'Unit': 'm'}  )
    #        ^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^^^^
    #           KEY (0)             VAL (1)
    # thats why we use 0, and [1] is our argument (here is LV)
    return sorted_distinct

# Стоит ли добавлять только одну функцию?
def sum_count(data):
    # Что получаю от дата?
    # Полный список, уже отсортированый
    # Главный ключ это Day, LV, Mat, хвост
    # tasks = [(lv, mat) for (day, lv, mat) in data.keys()]
    tasks_summary = {}
    for (day, lv,mat), task_data in data.items():
        if (lv,mat) not in tasks_summary:
            tasks_summary[(lv,mat)] = {
                "Count":task_data["Count"],
                "Unit":task_data["Unit"]
            } 
        else:
            tasks_summary[(lv, mat)]["Count"] += task_data["Count"]
    
    # Сортируем items и превращаем их обратно в словарь
    # x[0][0] — это LV (первый элемент кортежа-ключа)
    sorted_dict = dict(sorted(tasks_summary.items(), key=lambda x: x[0][0]))

    return sorted_dict