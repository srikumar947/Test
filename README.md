# Test

Installed packages -

Python 2.7.13 (Binary)
Pip 9.0.1 (Installs automatically when Python 2.7.13 is installed using a binary)
PySerial 3.3 (Download python wheel of PySerial and then pip install <package>)
Pillow 4.1.1 (pip install pillow)
PyInstaller-3.3.dev0; Future 0.16.0; Pypiwin32-219 (pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip)
Imutils 0.4.3 (pip install imutils)
Opencv-python 3.2.0.7; Numpy-1.13.0 (pip install opencv-python)
Matplotlib 2.0.2; cycler-0.10.0 functools32-3.2.3.post2 pyparsing-2.2.0 python-dateutil-2.6.0 pytz-2017.2 six-1.10.0 (pip install matplotlib)
CMake 3.9.0 (Binary)
MinGW (Binary)
Make 3.8.1 (Binary)


Changes to be made in API - 

Add BT-H3 as an acceptable device in _device_types (threespace_api.py Line 3506 under class TSBTSensor)


Changes to be made in csps.py - 

Change the COM_PORT to the corresponding value in your computer.


CMake Windows - 

set PATH=%PATH%;C:\MinGW\bin;C:\Program Files (x86)\GnuWin32\bin;
cmake -G "Unix Makefiles" ..
make && make install
