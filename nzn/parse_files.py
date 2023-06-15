from typing import List

import pandas as pd

from database.models import Node


def read_pension_funds() -> List[dict]:
    df = pd.read_excel("OWNAHA data 2021.xlsx", sheet_name=0).rename(
        columns={
            "ID": "id",
            "Sponsor/Entity": "name",
            "Country": "country",
        }
    )
    df["websites"] = df.apply(
        lambda row: {
            "homepage": row["Company_Website"],
            "integrated annual report": row["Integrated AR_website"],
            "sustainability report": row["SR_Website"],
        },
        axis=1,
    ).apply(lambda d: {k: d[k] for k in d.keys() if pd.notna(d[k])})

    df = df[["id", "name", "country", "websites"]]
    df = df.to_dict(orient="records")
    data = [Node(x).to_arango_document() for x in df]
    return data
