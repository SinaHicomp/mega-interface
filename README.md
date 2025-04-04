# mega-interface

> Install megacmd

1. Install the package in accordance with your operating system from the below link

[megacmd site](https://mega.io/cmd)

`Linux`  
For example for `Ubuntu 22.04`
```bash
wget https://mega.nz/linux/repo/xUbuntu_22.04/amd64/megacmd-xUbuntu_22.04_amd64.deb && sudo apt install "$PWD/megacmd-xUbuntu_22.04_amd64.deb"
```

`Windows`  
After installing the program, you should place the following path in the Path section in Environment.
```plaintext
C:\Users\<username>\AppData\Local\MEGAcmd
```

2. git clone

```bash
git clone https://github.com/SinaHicomp/mega_interface.git
```

3. Add to sys (Optional)

Add the path of `mega_interface` directory to sys with the below code:
```python
import sys
sys.path.append(r'<Path of the "mega_interface" folder>')
```
then you can use only `mega` replace of relative directory address on import

## Usage
> Initialize the interface and login
```python
from mega import MegaCmdInterface
# Replace with your MEGA account credentials
email = 'EMAIL'  
password = 'PASSWORD'

# Initialize the interface and login
mega_interface = MegaCmdInterface(email, password)
```
If you did not do part 3, use relative addresses when importing. Like below:
```python
from mega_interface.mega import MegaCmdInterface
```
> Upload a file
```python
# Upload a file
mega_interface.upload_file('local_path', 'MEGA_path')
```
> Download a file
```python
# Download a file
mega_interface.download_file('MEGA_path', 'local_path')
```
> Remove a file
```python
# Remove a file
mega_interface.remove_file('MEGA_path')
```
> List files in the MEGA directory
```python
# List files in the MEGA directory
files = mega_interface.list_files('MEGA_path')
```
> Create folder
```python
# Create folder
mega_interface.create_folder("MEGA_path")
```
> Logout
```python
# Logout
mega_interface.logout()
```