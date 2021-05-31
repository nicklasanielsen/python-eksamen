import matplotlib.pyplot as plt


def plotter(dataframe, column):
    columns = dataframe.columns
    df_sorted = dataframe

    for col in columns:
        if col == column:
            df_sorted = dataframe.sort_values(by=[col])

    plt.figure(figsize=[20, 10])
    plt.xticks(rotation=45, horizontalalignment="right")
    plt.ylabel("Amount of crimes", fontsize=10)
    plt.xlabel("Town", fontsize=10)
    plt.title(column.upper(), fontsize=20)

    try:
        plt.bar(df_sorted.index, df_sorted.loc[:, column.lower()])
    except:
        return

    plt.show
