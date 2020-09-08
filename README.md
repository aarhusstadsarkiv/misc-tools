# misc-tools
Miscellaneous tools for handling various data related tasks at Aarhus City Archives.

### Compiler notes
Use `pyinstaller` as follows:

- Install to and compile in your virtual environment via `poetry`. 
- On Windows, remember to use the windowed option with `-w`.
    * When debugging on Windows, leave out the windowed option and run the resulting `.exe` file in `PowerShell`.
- To compile to one file, use the `-F` option.
- If using a spec file, remember to a) commit it to source control, and b) tell `pyinstaller` to use it during run with `pyinstaller [options] specfile.spec` instead of the script path. For more information: https://pyinstaller.readthedocs.io/en/stable/spec-files.html
- In summary: 
    ```
    poetry add pyinstaller
    poetry run pyinstaller -F -w path_to_script.py
    ``` 
    OR
    ```
    poetry add pyinstaller
    poetry run pyinstaller specfile.spec
    ``` 

