import re
import pandas as pd

VIEW = "View"


def read_warehouse() -> pd.DataFrame:
    df = pd.read_csv("/home/henryp/Documents/Answer/Warehouse.csv", header=0)
    return df

def drop_last_underscore(x: str) -> str:
    match = re.match(r'^(.*)_[^_]*$', x)
    matched = None
    if match:
        matched = match.group(1).strip()
    else:
        print(f"Don't know how to parse '{x.strip()}'")
    return matched

if __name__ == "__main__":
    with open("/home/henryp/Documents/Answer/29946/schema_object.csv", "r") as f:
        lines = f.readlines()
    print(len(lines))
    df = read_warehouse()
    tables = []
    for line in lines:
        schema, obj = line.split(",")
        table = drop_last_underscore(obj)
        if not table:
            table = obj.strip()
        tables.append(table.lower())
        warehouse = df[df[VIEW].str.lower() == table.lower()]
        num_match = len(warehouse)
        if num_match != 1:
            print(f"Table '{table}' ({obj.strip()}) matches {num_match} rows in warehouse")
            if num_match > 1:
                print(warehouse[VIEW])
    assert len(tables) == len(lines)
    tables = set(tables)
    matching = df[df[VIEW].str.lower().isin(tables)]
    print(len(matching))
    print(f"len(matching = {len(matching)}, set of names = {len(tables)}")
    assert(len(matching) == set(tables))


