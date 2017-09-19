# BokehAppDemo
An app to play with the hyper-parameters and save it to a file

## Clone the repository  
``` 
git clone https://github.com/holmgroup/BokehAppDemo.git
``` 
Do your work and then add them to git server as:
``` 
git add -A
git commit "Commit message"
git push
``` 

In terminal:

navigate to the parent folder to Flask_parameter_update and then run:

``` 
bokeh serve --show Flask_parameter_update
``` 

On saving the params, they are appended to a textfile output.txt in Flask_parameter_update/output.txt
## Packages required:
Bokeh
Numpy
Scikit-image (> 0.12)

#Port Forwarding:
To run this on hippolyta, clone the repository into hippolyta and run it as before
Note the local port number on the terminal, and port forward it to your machine as:
``` 
ssh -N -L $LOCALPORT:localhost:$REMOTEPORT $REMOTEHOST
``` 
