import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file with specified encoding
file_path = r'C:\Users\DavidMothibi\OneDrive - Childline Gauteng\Desktop\Airbnb Data\Listings.csv'
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Convert 'host_since' to datetime
df['host_since'] = pd.to_datetime(df['host_since'], errors='coerce')

# Filter for Paris listings and keep only specified columns
paris_listings = df[df['city'] == 'Paris'][['host_since', 'neighbourhood', 'city', 'accommodates', 'price']]

# Check for missing values
missing_values = paris_listings.isnull().sum()

# Calculate basic profiling metrics
qa_metrics = paris_listings.describe()

print("Missing Values:")
print(missing_values)
print("\nQA Metrics:")
print(qa_metrics)

# Create a table grouped by 'neighbourhood' and calculate mean price
paris_listings_neighbourhood = paris_listings.groupby('neighbourhood')['price'].mean().sort_values().reset_index()

# Find the most expensive neighbourhood
most_expensive_neighbourhood = paris_listings_neighbourhood.iloc[-1]['neighbourhood']

# Filter for the most expensive neighbourhood
most_expensive_neighbourhood_listings = paris_listings[paris_listings['neighbourhood'] == most_expensive_neighbourhood]

# Group by 'accommodates' and calculate the mean price
paris_listings_accommodations = most_expensive_neighbourhood_listings.groupby('accommodates')['price'].mean().sort_values().reset_index()

# Extract year from 'host_since'
paris_listings['host_since_year'] = paris_listings['host_since'].dt.year

# Group by year and calculate the average price and count of new hosts
paris_listings_over_time = paris_listings.groupby('host_since_year').agg({'price': 'mean', 'host_since': 'count'}).rename(columns={'host_since': 'new_hosts'}).reset_index()

# Plot the average price by neighbourhood
plt.figure(figsize=(10, 6))
plt.barh(paris_listings_neighbourhood['neighbourhood'], paris_listings_neighbourhood['price'], color='skyblue')
plt.xlabel('Average Price')
plt.ylabel('Neighbourhood')
plt.title('Average Price by Neighbourhood in Paris')
plt.show()

# Plot the average price by accommodates in the most expensive neighbourhood
plt.figure(figsize=(10, 6))
plt.barh(paris_listings_accommodations['accommodates'], paris_listings_accommodations['price'], color='lightgreen')
plt.xlabel('Average Price')
plt.ylabel('Accommodates')
plt.title(f'Average Price by Accommodates in {most_expensive_neighbourhood}')
plt.show()

# Create two line charts: one showing the count of new hosts over time, and one showing average price
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot count of new hosts over time
ax1.plot(paris_listings_over_time['host_since_year'], paris_listings_over_time['new_hosts'], color='blue', label='New Hosts')
ax1.set_xlabel('Year')
ax1.set_ylabel('Count of New Hosts', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis for the average price
ax2 = ax1.twinx()
ax2.plot(paris_listings_over_time['host_since_year'], paris_listings_over_time['price'], color='red', label='Average Price')
ax2.set_ylabel('Average Price', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Add titles and labels
plt.title('Count of New Hosts and Average Price Over Time')
fig.tight_layout()
plt.show()

# Display the neighbourhood with the highest average price
print(f"The neighbourhood in Paris with the highest average AirBnB listing price is {most_expensive_neighbourhood}")
