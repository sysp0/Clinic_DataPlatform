import pandas as pd
import pandera as pa


def validate(model, query, engine):
    df = pd.read_sql(query, engine)
    try:
        return model.validate(df, lazy=True)
    except pa.errors.SchemaErrors as err:
        bad_idx = [i for i in err.failure_cases["index"].unique() if i in df.index and pd.notna(i)]
        return df.drop(bad_idx) if bad_idx else df
