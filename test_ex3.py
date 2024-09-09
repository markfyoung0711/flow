from ex3 import do


tlist = [1, 2, 3]
tlist = [tlist, tlist, tlist]


def test_do():
    df = do(tlist, columns=["A", "B", "C"])
    assert df["A"].loc[0] == 1
    print(df)
