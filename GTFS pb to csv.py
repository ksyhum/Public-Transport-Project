#pip install gtfs_kit
#pip install protobuf3-to-dict==0.1.5
#pip install --upgrade gtfs-realtime-bindings

import os
import pandas as pd
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

# Base directory path
base_directory_path = r"D:\Humam\KTH\Github\Public Transport\extracted_files\2024-01-16\16\sl\TripUpdates\2024\01\16" #change to your path


# Loop through hours 00 to 23
for hour in range(00, 24):
    # Format the hour to ensure it is two digits
    formatted_hour = f"{hour:02d}"

    # Update the directory path for the current hour
    directory_path = os.path.join(base_directory_path, formatted_hour)

    # Initialize an empty DataFrame for the current hour's real-time data
    all_realtimedata = pd.DataFrame()

    # Loop over all files in the current directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.pb'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'rb') as f:
                feed = gtfs_realtime_pb2.FeedMessage()
                feed.ParseFromString(f.read())

                # Convert protobuf to dictionary and normalize
                realtime_dict = protobuf_to_dict(feed)
                realtimedata = pd.json_normalize(realtime_dict['entity'])

                # Ensure 'trip_update.stop_time_update' exists before processing
                if 'trip_update.stop_time_update' in realtimedata.columns:
                    dfstoptime = realtimedata['trip_update.stop_time_update'].explode().apply(pd.Series)
                    realtimedata = pd.concat([realtimedata, dfstoptime], axis=1)
                    realtimedata = realtimedata.drop(['trip_update.stop_time_update'], axis=1)

                # Normalize 'arrival' and 'departure' if they exist
                if 'arrival' in realtimedata.columns:
                    dfarrival = pd.json_normalize(realtimedata['arrival'].dropna())
                    dfarrival = dfarrival.rename(columns={"delay": "arrival_delay", "time": "arrival_time", "uncertainty": "arrival_uncertainty"})
                    realtimedata = realtimedata.drop(['arrival'], axis=1)
                else:
                    dfarrival = pd.DataFrame()

                if 'departure' in realtimedata.columns:
                    dfdeparture = pd.json_normalize(realtimedata['departure'].dropna())
                    dfdeparture = dfdeparture.rename(columns={"delay": "departure_delay", "time": "departure_time", "uncertainty": "departure_uncertainty"})
                    realtimedata = realtimedata.drop(['departure'], axis=1)
                else:
                    dfdeparture = pd.DataFrame()

                # Concatenate processed data
                realtimedata.reset_index(drop=True, inplace=True)
                dfarrival.reset_index(drop=True, inplace=True)
                dfdeparture.reset_index(drop=True, inplace=True)
                realtimedata = pd.concat([realtimedata, dfarrival, dfdeparture], axis=1, ignore_index=False)

                # Accumulate the data
                all_realtimedata = pd.concat([all_realtimedata, realtimedata], ignore_index=True)

    # Reset the index of the final DataFrame
    all_realtimedata.reset_index(drop=True, inplace=True)

    # Save the final dataframe with a unique name for the current hour
    output_file_name = f"RT_17_2024_{formatted_hour}.csv" #set your date here
    all_realtimedata.to_csv(output_file_name, index=False)

    # Optional: Print out a message to indicate completion for the current hour
    print(f"Data for hour {formatted_hour} processed and saved to {output_file_name}")