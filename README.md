# misc-tools
Miscellaneous tools for handling various data related tasks at Aarhus City Archives.

### Compiler notes
Use `pyinstaller` as follows:

- Install to and compile in your virtual environment via `poetry`. 
- On Windows, remember to use the windowed option with `-w`.
    * When debugging on Windows, leave out the windowed option and run the resulting `.exe` file in `PowerShell`.
- To compile to one file, use the `-F` option.
- In summary: 
    ```
    poetry add pyinstaller
    poetry run pyinstaller -F -w path_to_script.py
    ``` 
