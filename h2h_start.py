import BreadLib as bl
import os

presets = bl.registry.get_all()
choosed_preset = presets[0]

def get_output_dir():
    from pathlib import Path
    SCRIPT_DIR = Path(__file__).resolve().parent
    OUTPUT_DIR = SCRIPT_DIR / "Output"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR

# def draw_menu():
#     import tkinter as tk
#     from tkinter import ttk

#     root = tk.Tk()
#     root.title("Human To Human")
#     root.geometry("400x400")

#     panel_frame = tk.Frame(root, bg="#1e1e1e")
#     panel_frame.pack(anchor=tk.NW, padx=20, pady=20)



if __name__ == "__main__":
    print("[Human to Human Script]")

    OUTPUT_DIR = get_output_dir()

    for i, pr in enumerate(presets):    # enumerate is important. Returns tuple
        bl.msg_info(f"{i} - {pr.name}")
    bl.msg_info("Please enter prefered profile:")
    profile_index = (int)(input())
    profile = presets[profile_index]
    try:
        while True:
            try:
                path = input("Please provide path to file to process: ").strip()
                if not os.path.exists(path):
                    raise ValueError(f"File not found at: {path}")
                elif path == "exit":
                    break
                
                res = bl.get_data_vertical(path,cols=profile.columns, sRow=profile.startRow, maxEmpty=profile.maxEmptyRows)
                
                res = bl.data_clear_empty(res)
                pip = bl.daily_count(res, refCol=profile.referenceColumn, matCol=profile.materialColumn, countCol=profile.countColumn)

                week_order = profile.week_order

                sorted_pip = {}
                for day in week_order:
                    for key, value in pip.items():
                        if key[0] == day:
                            sorted_pip[key] = value
                
                summary = bl.sum_count(sorted_pip)
                bl.build_table(OUTPUT_DIR, sorted_pip, 2, summary)

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

