# Test

Update - 

Install opencv before compiling.

brew tap homebrew/science

brew install opencv

cat ~/.bash_profile | grep PYTHONPATH   (Make sure to add PYTHONPATH)

ln -s /usr/local/Cellar/opencv/2.4.13.2/lib/python2.7/site-packages/cv.py cv.py

ln -s /usr/local/Cellar/opencv/2.4.13.2/lib/python2.7/site-packages/cv2.so cv2.so

pip install numpy

pip install matplotlib

If need be, export the PYTHONPATH from terminal.

To build, do the following - 

mkdir build

cd build

cmake ..

make && make install

Now, navigate to csps.app in build/src/dist/ and open it.
