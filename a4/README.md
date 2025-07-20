# CS158A Assignment 4 Re: Leader Election

## Files Included
- `myleprocess.py`: the process to be part of the election ring
- `config.txt`: the config file, which includes IP addresses and port numbers
- `log1.txt`, `log2.txt`, `log3.txt`: log files from the three processes in your local demo
- `README.md`: instructions and execution examples/test cases

## Run the Program

### Step 1. Under three folders:
Includes `config.txt` and `myleprocess.py` under separate folders.

### Step 2. Run the program
Run `myleprocess.py` in separate terminals.

## Execution Example & Output
Terminal 1:

<img width="435" height="112" alt="Screenshot 2025-07-20 at 4 18 27 PM" src="https://github.com/user-attachments/assets/7f41ac35-e4e4-44b4-8cce-c55b5d35f1e0" />

Terminal 2:

<img width="435" height="112" alt="Screenshot 2025-07-20 at 4 19 14 PM" src="https://github.com/user-attachments/assets/7b64a7d7-d853-4b70-9182-aa7a13b8d809" />

Terminal 3:

<img width="435" height="112" alt="Screenshot 2025-07-20 at 4 19 55 PM" src="https://github.com/user-attachments/assets/2f8b878a-c668-482c-8fd8-8c835808d58b" />

- At the end, the leader with the largest uuid is decided.
- Under the three folders, `log.txt` will be created with received and sent messages.

