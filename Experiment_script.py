import subprocess

# Define the number of times to run the script
num_runs = 50

# Loop to run the script multiple times
for i in range(num_runs):
    # Run the gamemanager.py script
    result = subprocess.run(["python3", "GameManager_3.py"])
    # Check the return code to see if the script ran successfully
    if result.returncode == 0:
        print(f"Run {i+1}/{num_runs} completed successfully.")
    else:
        print(f"Run {i+1}/{num_runs} failed with return code {result.returncode}.")
