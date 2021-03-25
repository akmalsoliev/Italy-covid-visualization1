import re
import wikipedia as wp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Wikipedia scrapper

wiki_page = 'Climate_of_Italy'
html = wp.page(wiki_page).html().replace(u'\u2212', '-')


def dataframe_cleaning(table_number=int):
    global html
    df = pd.read_html(html, encoding='utf-8')[table_number]
    df.drop(np.arange(5, len(df.index)), inplace=True)
    df.columns = df.columns.droplevel()
    replace = '[Â°C(Â°F)]*'
    df['Month'] = df['Month'].str.replace(replace, '', regex=True)

    find = '\((.*?)\)'
    for i, column in enumerate(df.columns):
        if i > 0:
            df[column] = (df[column]
                          .str.findall(find)
                          .map(lambda x: np.round((float(x[0]) - 32) * (5 / 9), 2)))
    return df


test = dataframe_cleaning(1)

# Importing DATA
covid_data = pd.read_csv('Daily_Covis19_Italian_Data_Province_Incremental.csv')

# Grouping
covid_positive = covid_data.groupby('Date').agg({'Total Positive': np.sum})

# Creating plot
fig, ax = plt.subplots(figsize=[8, 4.5])

# Plotting
ax.plot(covid_positive)

# Labeling
plt.title('COVID-19 Italy \nNumber of new cases by from Feb 2019')
plt.xlabel('Months')
plt.ylabel('Number of new cases')

# Setting x-tick labels.
locations = np.arange(0, 393, 30)
plt.xticks(locations, np.linspace(0, len(locations), len(locations), dtype=int))

plt.show()