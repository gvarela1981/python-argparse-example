# python-argparse-example
Parsing parameters example using python's built in argparse

# Features of the Argparse Library

1. **Define Command-line Arguments**  
   Create both positional and optional arguments for your command-line script.
   **Example:**
	```python
    import argparse
    
    parser = argparse.ArgumentParser(description="Demo argparse")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("--count", type=int, help="Number of iterations")
    args = parser.parse_args()
    ```
   **Command Execution:**
	```python
    python script.py --unknown

    ```
   **Output:**
	```python
    usage: script.py [-h] [--verbose] [--count COUNT]
    script.py: error: unrecognized arguments: --unknown

    ```

2. **Automatic Help Messages**  
   Automatically generate help `--help` and `-h` messages for users to understand the script's usage.

   **Example:**
	```python
	python script.py --help
	```
	**Output:**

	```python
	usage: script.py [-h] [--verbose] filename
3. **Type Validation**  
   Ensures the correct data type for arguments (e.g., ```int```, ```float```, ```str```).

	**Example:**

	```python
	parser.add_argument("--count", type=int, help="Number of iterations")
	```

4. **Assign default values to arguments if they are not provided.**  
   Ensures the correct data type for arguments (e.g., ```int```, ```float```, ```str```).

	**Example:**

	```python
	parser.add_argument("--mode", default="normal", help="Set the mode")

5. **Short and Long Options.**  
   Supports both short (e.g., ```-v```) and long (e.g., ```--verbose```) options.

	**Example:**

	```python
	parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

	```

6. **Action Parameters**  
   Specify what happens when an argument is encountered:
   - ```store``` (default): Stores the argument value. 
   - ```store_true``` / ```store_false```: Sets a boolean flag.
   - ```append```: Adds multiple values to a list.
   - ```count```: Counts occurrences of a flag.

	**Example:**

	```python
	parser.add_argument("--debug", action="store_true", help="Enable debugging")

	```

7. **Positional Arguments**  
   Require specific arguments in order:
   
	**Example:**

	```python
	parser.add_argument("input_file", help="Input file path")

	```


8. **Choices**  
   Restrict argument values to a predefined set.
   
	**Example:**

	```python
	import argparse

    parser = argparse.ArgumentParser(description="Demo argparse with choices")
    parser.add_argument(
        "--level",
        choices=["low", "medium", "high"],
        required=True,
        help="Set the difficulty level (low, medium, high)",
    )
    args = parser.parse_args()
    
    print(f"Selected level: {args.level}")
    ```

    **How It Works**
    
    **Command with Valid Input**

	```python
	python script.py --level medium

    ```
    
    **Output**

	```python
	Selected level: medium

    ```

    **Command with Invalid Input**

	```python
	python script.py --level extreme

    ```
    
    **Output**

	```python
	usage: script.py [-h] --level {low,medium,high}
    script.py: error: argument --level: invalid choice: 'extreme' (choose from 'low', 'medium', 'high')

    ```

	```

9. **Subcommands**  
   Create subcommands for complex CLI tools.
   
	**Example:**

	```python
	subparsers = parser.add_subparsers(dest="command")

    subparser_a = subparsers.add_parser("run", help="Run the program")
    subparser_a.add_argument("--fast", action="store_true", help="Run fast")
    
    subparser_b = subparsers.add_parser("test", help="Test the program")

	```

10. **Error Handling**  
   Provides clear error messages when invalid arguments are passed.
   
	**Example:**

	```python
	python script.py --unknown

	```
   
	**Output:**

	```python
	error: unrecognized arguments: --unknown

	```