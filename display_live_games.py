import json
import time
import os
while True:
    with open("output.json", "r") as f:
        data = json.load(f)
    #data = dict(sorted(data.items(), key=lambda x: int(x[1]['Diff']), reverse=True))
    # Define the column headings
    print("{:<5} {:<30} {:<10} {:<20} {:<10} {:<10} {:<20} {:<10}".format('ID', 'League', 'Status', 'Team1', 'Score1', 'Score2', 'Team2', 'Diff'))

    # Loop through the data and print each row as a formatted string
    for key, value in data.items():
        print("{:<5} {:<30} {:<10} {:<20} {:<10} {:<10} {:<20} {:<10}".format(key, value['League'], value['status'], value['Team1'], value['Score1'], value['Score2'], value['Team2'], value['Diff']))
    time.sleep(5)
    os.system("clear")