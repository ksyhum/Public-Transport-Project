import pandas as pd
import os

# Define the base path where your CSV files are located
base_path = r'D:\Humam\KTH\Github\Public Transport\csv'
final_stop_path = os.path.join(base_path, 'final_stop_update.csv')  # Adjust path as necessary

# Read stops_akhir CSV
final_stop_df = pd.read_csv(final_stop_path)


# Columns to be dropped, now correctly formatted
columns_to_drop = [
    'id', 'trip_update.trip.start_time', 'trip_update.trip.start_date',
    'trip_update.trip.schedule_relationship', 'trip_update.trip.direction_id',
    'trip_update.vehicle.id', 'trip_update.timestamp', 'schedule_relationship',
    'arrival_uncertainty', 'departure_uncertainty', 'stop_name', 'stop_lat', 'stop_lon', 'location_type', 'parent_station', 'platform_code'
]

# Initialize an empty DataFrame for the results
filtered_df = pd.DataFrame()

# Process the CSV files in the folder
for filename in os.listdir(base_path):
    if filename.endswith('.csv') and filename != 'final_stop_update.csv':
        file_path = os.path.join(base_path, filename)

        # Adjust chunksize based on your system's memory
        chunksize = 100000

        for chunk in pd.read_csv(file_path, chunksize=chunksize, low_memory=False):
            # Drop specified columns
            chunk.drop(columns=columns_to_drop, errors='ignore', inplace=True)

            # Rename columns
            chunk.rename(columns={
                'trip_update.trip.trip_id': 'trip_id',
                'trip_update.trip.route_id': 'route_id'
            }, inplace=True)

            # Filter based on stop_id existing in stops_akhir_df
            chunk = chunk[chunk['stop_id'].isin(final_stop_df['stop_id'])]

            # Concatenate filtered chunk to the final DataFrame
            filtered_df = pd.concat([filtered_df, chunk])


# Drop duplicates based on trip_id and stop_id, if needed
filtered_df = filtered_df.drop_duplicates(subset=['trip_id', 'stop_id'])
filtered_df['trip_id'] = filtered_df['trip_id'].apply(lambda x: '{:.0f}'.format(x) if pd.notnull(x) else x)
filtered_df['route_id'] = filtered_df['route_id'].apply(lambda x: '{:.0f}'.format(x) if pd.notnull(x) else x)
filtered_df['stop_sequence'] = filtered_df['stop_sequence'].apply(lambda x: '{:.0f}'.format(x))
filtered_df['arrival_delay'] = filtered_df['arrival_delay'].apply(lambda x: '{:.0f}'.format(x))
filtered_df['departure_delay'] = filtered_df['departure_delay'].apply(lambda x: '{:.0f}'.format(x))
filtered_df['arrival_time'] = pd.to_datetime(filtered_df['arrival_time'], unit='s', utc=True)  # Mengubah menjadi waktu
filtered_df['departure_time'] = pd.to_datetime(filtered_df['departure_time'], unit='s', utc=True)  # Mengubah menjadi waktu

# Save the final, processed DataFrame to CSV
output_path = os.path.join(base_path, 'final_data_processed_16.csv')  # Adjust output filename as necessary
filtered_df.to_csv(output_path, index=False)

print("Processed Data Preview:", filtered_df.head())
print(filtered_df.astype)

