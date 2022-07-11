FROM python:3.8

# set a directory for the app
WORKDIR /home/tareeq/Documents/Hood_Sealer_Container

# copy all the files to the container
COPY . .

# install dependencies

RUN apt-get update && apt-get install -y python3-opencv \
      libhdf5-dev \
      libgl1-mesa-glx \
      openmpi-bin \
      wget \
      python3-tk && \
    rm -rf /var/lib/apt/lists/*


RUN pip install keyboard 
RUN pip install opencv-python
RUN pip install --no-cache-dir -r requirements.txt 

# tell the port number the container should expose
EXPOSE 5000

ENV QT_X11_NO_MITSHM=1

# run the command
CMD ["python", "./main.py"]
