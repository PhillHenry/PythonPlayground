import re
import pandas as pd


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
    tables = set([])
    for line in lines:
        schema, obj = line.split(",")
        table = drop_last_underscore(obj)
        if not table:
            table = obj.strip()
        tables.update(table)
        warehouse = df[df["View"].str.lower() == "Commissioner_Hierarchies".lower()]
        if table.strip() == "SUS+ Faster Emergency Care Data Set (ECDS) (Daily)":
            print(warehouse)
        if len(warehouse) != 1:
            print(f"Could not match {table}")
            print(warehouse)


