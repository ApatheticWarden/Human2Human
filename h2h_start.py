import BreadLib as bl
import os
if __name__ == "__main__":
    print("[Human to Human Script]")
    try:
        while True:
            try:
                path = input("Please provide path to file to process: ").strip()
                if not os.path.exists(path):
                    raise ValueError(f"File not found at: {path}")
                elif path == "exit":
                    break
                
                res = bl.get_data_vertical(path,cols=6, sRow=6, maxEmpty=10)
                
                res = bl.data_clear_empty(res)
                pip = bl.daily_count(res, refCol=5, matCol=3, countCol=4)

                week_order = ['Poniedzialek', 'Wtorek', 'Sroda', 'Czwartek', 'Piatek', 'Sobota']

                sorted_pip = {}
                for day in week_order:
                    for key, value in pip.items():
                        if key[0] == day:
                            sorted_pip[key] = value
                
                summary = bl.sum_count(sorted_pip)
                bl.output_daily_tables('C:\\Users\\Gleb\\Desktop\\proc', sorted_pip, 4, summary)

                # for (day, lv, material), value in pip.items():
                #     print(f"{day}\t| {lv} \t| {value['Count']} {value.get('Unit', '')} \t| {material}")
            except ValueError as v:
                bl.msg_warning(v)
                continue
            except Exception as e:
                bl.msg_error(e)
                break
    except Exception as e:
        bl.msg_error(e)

