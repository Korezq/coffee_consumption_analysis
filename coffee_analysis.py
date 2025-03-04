
# Global Coffee Consumption Trends Analysis
# Analyzing worldwide coffee habits using worldwide_coffee_habits.csv

# Step 1: Import Required Libraries
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Upload Dataset
# Upload the worldwide_coffee_habits.csv file in Colab
df = pd.read_csv('worldwide_coffee_habits.csv')

# Quick data inspection
print("Dataset Preview:")
print(df.head())
print("\nDataset Info:")
print(df.info())

# Step 3: Create SQLite Database
conn = sqlite3.connect(':memory:')
df.to_sql('coffee_habits', conn, index=False, if_exists='replace')

# Step 4: Define SQL Queries for Analysis

# Query 1: Average consumption and price by year
query1 = """
SELECT Year,
       AVG("Coffee Consumption (kg per capita per year)") as AvgConsumption,
       AVG("Average Coffee Price (USD per kg)") as AvgPrice
FROM coffee_habits
WHERE Year >= 2015  -- Focus on recent years for relevance (adjust as needed)
GROUP BY Year
ORDER BY Year
"""
trends_by_year = pd.read_sql_query(query1, conn)

# Query 2: Top 5 countries by coffee consumption in 2023
query2 = """
SELECT Country,
       "Coffee Consumption (kg per capita per year)" as Consumption,
       "Population (millions)" as Population
FROM coffee_habits
WHERE Year = 2023
ORDER BY Consumption DESC
LIMIT 5
"""
top_countries_2023 = pd.read_sql_query(query2, conn)

# Query 3: Coffee type preference by year
query3 = """
SELECT Year,
       "Type of Coffee Consumed" as CoffeeType,
       COUNT(*) as Count,
       AVG("Coffee Consumption (kg per capita per year)") as AvgConsumption
FROM coffee_habits
WHERE Year >= 2015
GROUP BY Year, "Type of Coffee Consumed"
ORDER BY Year, CoffeeType
"""
coffee_type_trends = pd.read_sql_query(query3, conn)


query4 = """
SELECT "Average Coffee Price (USD per kg)",
       AVG("Coffee Consumption (kg per capita per year)") as AvgConsumption
FROM coffee_habits
GROUP BY "Average Coffee Price (USD per kg)"
ORDER BY "Average Coffee Price (USD per kg)"
"""
price_demand = pd.read_sql_query(query4, conn)

query5 = """
SELECT Year,
       "Type of Coffee Consumed" as CoffeeType,
       AVG("Coffee Consumption (kg per capita per year)") as AvgConsumption
FROM coffee_habits
GROUP BY Year, "Type of Coffee Consumed"
ORDER BY Year, CoffeeType
"""
coffee_type_trends = pd.read_sql_query(query5, conn)

query6 = """
SELECT "Population (millions)",
       AVG("Coffee Consumption (kg per capita per year)") as AvgConsumption
FROM coffee_habits
GROUP BY "Population (millions)"
ORDER BY "Population (millions)"
"""
population_vs_consumption = pd.read_sql_query(query6, conn)



# Step 5: Visualizations

# Visualization 1: Consumption and Price Trends Over Time
plt.figure(figsize=(12, 6))
plt.plot(trends_by_year['Year'], trends_by_year['AvgConsumption'], label='Avg Consumption (kg/capita)', marker='o')
plt.plot(trends_by_year['Year'], trends_by_year['AvgPrice'], label='Avg Price (USD/kg)', marker='o')
plt.title('Global Coffee Consumption and Price Trends (2015-2023)')
plt.xlabel('Year')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()

# Visualization 2: Top 5 Countries by Coffee Consumption in 2023
plt.figure(figsize=(10, 6))
sns.barplot(data=top_countries_2023, x='Country', y='Consumption')
plt.title('Top 5 Countries by Coffee Consumption Per Capita (2023)')
plt.xlabel('Country')
plt.ylabel('Consumption (kg per capita)')
plt.xticks(rotation=45)
plt.show()

# Visualization 3: Coffee Type Preferences Over Time
plt.figure(figsize=(12, 6))
sns.barplot(data=coffee_type_trends, x='Year', y='AvgConsumption', hue='CoffeeType')
plt.title('Coffee Type Preferences by Year (2015-2023)')
plt.xlabel('Year')
plt.ylabel('Average Consumption (kg per capita)')
plt.legend(title='Coffee Type')
plt.show()

plt.figure(figsize=(10, 6))
plt.hexbin(price_demand['Average Coffee Price (USD per kg)'], price_demand['AvgConsumption'], gridsize=30, cmap='Blues', mincnt=1)
plt.colorbar(label='Count')
plt.title('Price Elasticity of Coffee Demand')
plt.xlabel('Average Coffee Price (USD/kg)')
plt.ylabel('Avg Consumption (kg per capita)')
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(data=coffee_type_trends, x='Year', y='AvgConsumption', hue='CoffeeType', marker='o')
plt.title('Coffee Type Trends Over Time')
plt.xlabel('Year')
plt.ylabel('Avg Consumption (kg per capita)')
plt.legend(title='Coffee Type')
plt.grid()
plt.show()

plt.figure(figsize=(10, 6))
plt.hexbin(population_vs_consumption['Population (millions)'], population_vs_consumption['AvgConsumption'], gridsize=30, cmap='Greens', mincnt=1)
plt.colorbar(label='Count')
plt.title('Population vs. Coffee Consumption')
plt.xlabel('Population (millions)')
plt.ylabel('Avg Consumption (kg per capita)')
plt.show()

# Step 6: Analysis and Thoughts
print("\nAnalysis Thoughts:")
print("1. Trends Over Time: Observing the plot, we can see if consumption increases as price changes. A stable or rising consumption with increasing prices might suggest strong demand.")
print("2. Top Countries: The top 5 countries in 2023 show which nations have the highest per capita consumption. Cross-referencing with population could reveal total volume leaders.")
print("3. Coffee Type Preferences: The distribution of coffee types over years indicates shifts in global preferences—e.g., a rise in Latte might reflect trendy café culture.")

# Step 7: Export Results
trends_by_year.to_csv('trends_by_year.csv', index=False)
top_countries_2023.to_csv('top_countries_2023.csv', index=False)
coffee_type_trends.to_csv('coffee_type_trends.csv', index=False)

# Download results, remove # to enable downloads
#files.download('trends_by_year.csv')
#files.download('top_countries_2023.csv')
#files.download('coffee_type_trends.csv')

# Close the database connection
conn.close()