import time

import pandas as pd

def wait_until_file_is_ready(path):
    last_size = -1
    while True:
        current_size = path.stat().st_size
        if current_size == last_size:
            break
        last_size = current_size
        time.sleep(0.5)


def append_data_to_excel_file(data, path):
    df = pd.read_excel(path) if path.exists() else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(path, index=False)

