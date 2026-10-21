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



#               Find the Most Expensive Apps, Filter out the Junk, and Calculate a (ballpark) Sales Revenue Estimate
# onvert the price column to numeric data. Then investigate the top 20 most expensive apps in the dataset.
#
# Remove all apps that cost more than $250 from the df_apps_clean DataFrame.
#
# Add a column called 'Revenue_Estimate' to the DataFrame. This column should hold the price of the app times the number of installs.
# What are the top 10 highest grossing paid apps according to this estimate? Out of the top 10 highest grossing paid apps, how many are games?

print("\n\n\n\n")
df_apps_clean.Price = df_apps_clean.Price.astype(str).str.replace('$', '')
df_apps_clean.Price = pd.to_numeric(df_apps_clean.Price)
print(df_apps_clean.sort_values(by='Price', ascending=False).head(20))

df_apps_clean = df_apps_clean[df_apps_clean['Price'] < 250]
print(df_apps_clean.sort_values(by='Price', ascending=False).head(20))


df_apps_clean['Revenue_Estimate'] = df_apps_clean.Installs.mul(df_apps_clean.Price)
print(df_apps_clean.sort_values('Revenue_Estimate', ascending=False)[:10])


#               Plotly Bar Charts & Scatter Plots: The Most Competitive & Popular App Categories
print(f"\n\nThere are {df_apps_clean['Category'].nunique()} unique Categories in the PlayStore\n\n")
top10_category = df_apps_clean['Category'].value_counts()[:10]
print("\n\nThese are the TOP 10 categories of the PlayStore App", top10_category)


# Visualizing Data with Plotly based on their Category
bar = px.bar(x=top10_category.index,  # index = category name
             y=top10_category.values)

# UnComment the line below and run the app.py if u want a window to pup up with the chart
# bar.show()


# Most popular Category is the one with the most downloads right ?
category_installs = df_apps_clean.groupby('Category').agg({'Installs': pd.Series.sum})
category_installs.sort_values('Installs', ascending=True, inplace=True)

# Visualizing Data with Plotly based on their Downloads
h_bar = px.bar(x=category_installs.Installs,
               y=category_installs.index,
               orientation='h',
               title='Category Popularity')

h_bar.update_layout(xaxis_title='Number of Downloads', yaxis_title='Category')

# UnComment the line below and run the app.py if u want a window to pup up with the chart
# h_bar.show()


# Create a DataFrame that has the number of apps in one column and the number of installs in another:
df_by_category = df_apps_clean.groupby('Category').agg({'App': pd.Series.count})
df_by_category = pd.merge(df_by_category, category_installs, on='Category', how="inner")
print(f'The dimensions of the DataFrame are: {df_by_category.shape}')
df_by_category.sort_values('Installs', ascending=False)


scatter = px.scatter(df_by_category, # data
                    x='App', # column name
                    y='Installs',
                    title='Category Concentration',
                    size='App',
                    hover_name=df_by_category.index,
                    color='Installs')

scatter.update_layout(xaxis_title="Number of Apps (Lower=More Concentrated)",
                      yaxis_title="Installs",
                      yaxis=dict(type='log'))

# UnComment the line below and run the app.py if u want a window to pup up with the chart
# scatter.show()


#               Extracting Nested Column Data using .stack()
# How many different types of genres are there? Can an app belong to more than one genre?
# Number of Genres?
print(len(df_apps_clean.Genres.unique()))
# Problem: Have multiple categories seperated by ;
print(df_apps_clean['Genres'].value_counts(ascending=True)[:5])

# Split the strings on the semi-colon and then .stack them.
stack = df_apps_clean.Genres.str.split(';', expand=True).stack()
print(f'We now have a single column with shape: {stack.shape}')
num_genres = stack.value_counts()
print(f'Number of genres: {num_genres}')

genres_bar= px.bar(num_genres,
                            x=num_genres.index,
                            y=num_genres.values,
                            title='Top Genres',
                            hover_name=num_genres.index,
                            color=num_genres.values,
                            color_continuous_scale='Agsunset')

genres_bar.update_layout(xaxis_title='Genres',yaxis_title='Number of Apps')

# UnComment the line below and run the app.py if u want a window to pup up with the chart
# genres_bar.show()



#               Grouped Bar Charts and Box Plots with Plotly
print(df_apps_clean.Type.value_counts())
# The majority of apps are free on the Google Play Store
df_free_vs_paid = df_apps_clean.groupby(["Category", "Type"], as_index=False).agg({'App': pd.Series.count})
print(df_free_vs_paid.head())
print(df_free_vs_paid.info())


paid_free_bar = px.bar(df_free_vs_paid,
                       x='Category',
                       y='App',
                       title='Free vs Paid Apps by Category',
                       color='Type',
                       barmode='group')

paid_free_bar.update_layout(xaxis_title='Category',
                    yaxis_title='Number of Apps',
                    xaxis={'categoryorder':'total descending'},
                    yaxis=dict(type='log'))

# UnComment the line below and run the app.py if u want a window to pup up with the chart
# paid_free_bar.show()




# How much should you charge? What are other apps charging in that category?
# How much revenue could you make?
# And how many downloads are you potentially giving up because your app is paid?
# A box plot that shows the number of Installs for free versus paid apps.

# Box Plots for the Number of Installs
box = px.box(df_apps_clean,
             y='Installs',
             x='Type',
             color='Type',
             notched=True,
             points='all',
             title='How Many Downloads are Paid Apps Giving Up?')

box.update_layout(yaxis=dict(type='log'))
# box.show()

#               Plotly Box Plots: Revenue by App Category
df_paid_apps = df_apps_clean[df_apps_clean['Type'] == 'Paid']
box = px.box(df_paid_apps,
             x='Category',
             y='Revenue_Estimate',
             title='How Much Can Paid Apps Earn?')

box.update_layout(xaxis_title='Category',
                  yaxis_title='Paid App Ballpark Revenue',
                  xaxis={'categoryorder': 'min ascending'},
                  yaxis=dict(type='log'))

box.show()

#               How Much Can You Charge? Examine Paid App Pricing Strategies by Category
df_paid_apps.Price.median()

price_per_category_box = px.box(df_paid_apps,
             x='Category',
             y="Price",
             title='Price per Category')

price_per_category_box.update_layout(xaxis_title='Category',
                  yaxis_title='Paid App Price',
                  xaxis={'categoryorder':'max descending'},
                  yaxis=dict(type='log'))


price_per_category_box.show()
