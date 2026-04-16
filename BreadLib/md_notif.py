info_pref = "[BreadLib Info]"
warn_pref = "[BreadLib Warn]"
error_pref = "[BreadLib Error]"

def msg_info(text):
    print(f"\033[32m{info_pref} {str(text)}\033[0m")

def msg_warning(text):
    print(f"\033[33m{warn_pref} {str(text)}\033[0m")

def msg_error(text):
    print(f"\033[31m{error_pref} {str(text)}\033[0m")