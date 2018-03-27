# Sonication
This project aims to turn a visual path on an image into a coherent sound.

# How does it work ?
The creation process is divided into 3 steps :
visual path ---|into|---> interpolated path ---|into|---> data ---|into|---> sound.

## First step
A visual path is a sequence of fixation points, written as follow :

```
# visual_path.dat
x1 y1
x2 y2
...
xn yn
```
One can simply interpolate it using the bash function "spline" : 
```
spline -n 500 -d 2 -A visual_path.dat >> splined.dat
```
Then, the interpolated path must be transformed to keep the important points around the fixation points. It can be done using the python function "empty_spline". One can use it this way :
```
./empty_spline.py visual_path.dat
```
Now we can go to next step.

## Second step
Data are created using 2 files : splined.dat and your_image.jpg. Run "create_data_1.py" :
```
./create_data_1.py your_image.jpg
```
