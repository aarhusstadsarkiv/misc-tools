# misc-tools
Miscellaneous tools for handling various data related tasks at Aarhus City Archives.

### Compiler notes
Use `pyinstaller` as follows:

- Compile in your virtual environment via `poetry`. 
- On Windows, remember to use the "windowed" option with `-w`.
- To compile to one file, use the `-F` option.
- In summary: 
    ```
    poetry run pyinstaller -F -w path_to_script.py
    ``` 
