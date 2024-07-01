import re
import pandas as pd

DATABASE = "Database"

SCHEMA = "Schema"

VIEW = "View"

MBs = "UsedSpaceMB"
SCHEMA = "Schema in NCDR"

# nhp_PSD = pd.read_excel(filename, sheet_name="NHSE_PSDM_0046", header=0)
# nhp_BB = pd.read_excel(filename, sheet_name="NHSE_BB_5008", header=0)
# nhp_neuro = pd.read_excel(filename, sheet_name="NHSE_Sandbox_Spec_Neurology", header=0)
# nhp_strat = pd.read_excel(filename, sheet_name="NHSE_Sandbox_StrategyUnit", header=0)
# dbs = [nhp_BB, nhp_neuro, nhp_neuro, nhp_strat]

def total_nhp() -> dict:
    filename = "/home/henryp/Downloads/JW_2024_06_27 - Table Sizes.xlsx"
    dbs = {}
    for tab in ["NHSE_PSDM_0046", "NHSE_BB_5008", "NHSE_Sandbox_Spec_Neurology", "NHSE_Sandbox_StrategyUnit"]:
        df = pd.read_excel(filename, sheet_name=tab, header=0)
        dbs[tab] = df
    raw = 0
    for df in dbs.values():
        raw = raw + df[MBs].sum()
    print(f"Total in NHP = {raw} MBs")
    return dbs


def actual_disk_used(nhp: pd.DataFrame, dbs: dict):
    total = 0
    for name, df in dbs.items():
        merged = pd.merge(nhp, df, left_on=VIEW, right_on="TableName", how='outer', indicator=True)
        both = merged[merged['_merge'] == 'both']
        used = both[MBs].sum()
        total = total + used
    print(f"\nTotal disk space used = {total / 1024} GB")


def non_matching(nhp: pd.DataFrame, dbs: dict):
    dfs = list(dbs.values())
    all = dfs[0]
    for df in dfs[1:]:
        all = pd.concat([all, df])
    merged = pd.merge(nhp, all, left_on=VIEW, right_on="TableName", how='outer', indicator=True)
    unknown = merged[merged['_merge'] == 'left_only']
    print(f"Number of unknown {len(unknown)}")
    print(unknown[[SCHEMA, VIEW]].to_string(index=False))


if __name__ == "__main__":
    # dfe = pd.read_excel("/home/henryp/Downloads/PhODs_UDAL Mart Requirements v9_1.xlsx", sheet_name="Phase 1 migration-Pharm+", header=0)
    nhp = pd.read_excel("/home/henryp/Downloads/21434 - NHPSU - Requirements - 20240529.xlsx",
                        sheet_name="E) DM-Data to copy from NCDR",
                        header=4)
    nhp = nhp.rename({"NCDR Dataset Schema": SCHEMA,
                "NCDR Table/View Name": VIEW,
                "NCDR Sandbox": DATABASE
                }, axis=1)
    actual_disk_used(nhp, total_nhp())
    non_matching(nhp, total_nhp())
    print("\nDatabases:")
    for db in nhp[1:][DATABASE].drop_duplicates():
        print(db)


