import re
import pandas as pd

VIEW = "View"
SCHEMA = "Schema"


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


class Mismatch:
    def __init__(self, num_matches: int, message: str):
        self.message = message
        self.num_matches = num_matches
    def __repr__(self):
        return f"""{self.num_matches} mismatches. 
{self.message}"""


def try_match(obj: str, mismathes: dict, df: pd.DataFrame, schema: str) -> str:
    table = drop_last_underscore(obj)
    if not table:
        table = obj.strip()

    warehouse = df[(df[VIEW].str.lower() == table.lower()) & (df[SCHEMA].str.lower() == schema.lower())]
    num_match = len(warehouse)
    if num_match != 1 and len(warehouse.groupby([SCHEMA, VIEW]).size().reset_index(name='count')) != 1:
        if num_match > 1:
            others = warehouse[[SCHEMA, VIEW]]
        else:
            others = ""
        msg = f"""Table '{table}' in {schema} ({obj.strip()}) matches {num_match} rows in warehouse
{others}"""
        mismathes[table] = Mismatch(num_match, msg)

    return table.lower()


if __name__ == "__main__":
    with open("/home/henryp/Documents/Answer/29946/schema_object.csv", "r") as f:
        lines = f.readlines()
    print(len(lines))
    df = read_warehouse()
    tables = []
    mismathes = {}
    for line in lines:
        schema, obj = line.split(",")
        tables.append(try_match(obj, mismathes, df, schema))
    assert len(tables) == len(lines)
    tables = set(tables)
    matching = df[df[VIEW].str.lower().isin(tables)]
    print(len(matching))
    print(f"len(matching = {len(matching)}, set of names = {len(tables)}")
    print("\nAmbiguous")
    for table, mismatch in mismathes.items():
        if mismatch.num_matches > 1:
            print(f"{table}: {mismatch}")
    print("\nUnmapped")
    count = 0
    for table, mismatch in mismathes.items():
        if mismatch.num_matches == 0:
            print(f"{table}: {mismatch}")
            count += 1
    print(f"{count} not mapped")
    assert(len(matching) == set(tables))


