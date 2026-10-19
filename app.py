import pandas as pd
import plotly.express as px

pd.options.display.float_format = '{:,.2f}'.format

df_apps = pd.read_csv('apps.csv')
# To Find the shape of the DataFrame and display the first few rows, you can use the following code:
print("Shape of df_apps:", df_apps.shape)

# Display a sample of 5 random rows from the DataFrame:
print("Sample of df_apps:")
print(df_apps.sample(5))

# Displaying the column names of the DataFrame can be done using the following code:
for column in df_apps.columns:
    print(df_apps[column].name)



#               Drop Unused Columns
# Remove the columns called Last_Updated and Android_Version from the DataFrame. We will not use these columns.
df_apps = df_apps.drop(columns=["Last_Updated", "Android_Ver"])
print(df_apps.head())




#               Find and Remove NaN values in Ratings
# How may rows have a NaN value (not-a-number) in the Ratings column?
count_nan_ratings = df_apps['Rating'].isna().sum()
print("NaN values in Ratings column:",count_nan_ratings)

# DataFrame called `df_apps_clean` that does not include these rows.
df_apps_clean = df_apps.dropna(subset=['Rating'])
print("Shape of df_apps_clean:", df_apps_clean.shape)

# Check for duplicates using the .duplicated()
# How many entries can you find for the "Instagram" app? remove any duplicates from `df_apps_clean`
print("Duplicates in df_apps_clean:", df_apps_clean.duplicated().sum())
df_apps_clean = df_apps_clean.drop_duplicates(subset=['App', 'Type', 'Price'])
print("Shape of df_apps_clean after dropping duplicates:", df_apps_clean.shape)



#               Find Highest Rated Apps
# Identify which apps are the highest rated. What problem might you encounter if you rely exclusively on ratings alone to determine the quality of an app?
highest_rated_apps = df_apps_clean.sort_values(by='Rating', ascending=False)
print("Highest Rated Apps:\n", highest_rated_apps.head(5))


#               Find 5 Largest Apps in terms of Size (MBs)
# What's the size in megabytes (MB) of the largest Android apps in the Google Play Store. Based on the data, do you think there could be limit in place or can developers make apps as large as they please?
largest_apps = df_apps_clean.sort_values(by='Size_MBs', ascending=False)
print("5 Largest Apps by Size:\n", largest_apps.head(5))



#           Find 5 Apps with Most Reviews
# Which apps have the highest number of reviews? Are there any paid apps among the top 50?
most_reviewed_apps = df_apps_clean.sort_values(by='Reviews', ascending=False).head(50)
print("5 Apps with Most Reviews:\n", most_reviewed_apps.head(5))
# Paid apps among the top 50
found = False
for type in most_reviewed_apps['Type']:
    if type == 'Paid':
        print("There are paid apps in the most reviewed apps list.")
        found = True
        break
if not found:
    print("There are no paid apps in the most reviewed apps list.")


#               Plotly Pie and Donut Charts - Visualise Categorical Data: Content Ratings
ratings = df_apps_clean['Content_Rating'].value_counts()
fig = px.pie(labels=ratings.index,values=ratings.values,title="Content Rating",names=ratings.index,)
fig.update_traces(textposition='outside', textinfo='percent+label')
# fig.show()



#               Numeric Type Conversion: Examine the Number of Installs
# How many apps had over 1 billion (that's right - BILLION) installations? How many apps just had a single install?
# Check the datatype of the Installs column.
# Count the number of apps at each level of installations.
# Convert the number of installations (the Installs column) to a numeric data type. Hint: this is a 2-step process. You'll have make sure you remove non-numeric characters first.

df_apps_clean.Installs.describe()
df_apps_clean.info()
print(df_apps_clean[['App', 'Installs']].groupby('Installs').count())
df_apps_clean.Installs = df_apps_clean.Installs.astype(str).str.replace(',', "")
df_apps_clean.Installs = pd.to_numeric(df_apps_clean.Installs)
print(df_apps_clean[['App', 'Installs']].groupby('Installs').count())


