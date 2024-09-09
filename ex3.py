import pandas as pd


def do(data, columns):
    df = pd.DataFrame(data, columns=columns)
    return df


if __name__ == "__main__":
    df = do()
    print(df)
