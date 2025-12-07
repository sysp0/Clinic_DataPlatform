import jdatetime
import pandas as pd
import pandera as pa


def validate(model, query, engine):
    df = pd.read_sql(query, engine)
    try:
        return model.validate(df, lazy=True)
    except pa.errors.SchemaErrors as err:
        bad_idx = [i for i in err.failure_cases["index"].unique() if i in df.index and pd.notna(i)]
        return df.drop(bad_idx) if bad_idx else df

def shamsi_to_miladi(shamsi_date_str):
    """
    تبدیل تاریخ شمسی (string) به میلادی (datetime)
    فرمت‌های پشتیبانی شده: '1402/09/15' یا '1402-09-15'
    """
    if pd.isna(shamsi_date_str) or shamsi_date_str == '':
        return pd.NaT
    
    try:
        shamsi_date_str = str(shamsi_date_str).strip()
        shamsi_date_str = shamsi_date_str.replace('/', '-')
        parts = shamsi_date_str.split('-')
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        jalali_date = jdatetime.date(year, month, day)
        gregorian_date = jalali_date.togregorian()
        return gregorian_date.strftime("%Y-%m-%d")
    
    except Exception as e:
        print(f"Error converting {shamsi_date_str}: {e}")
        return pd.NaT