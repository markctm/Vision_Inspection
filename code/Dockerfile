
FROM jumidlej/raspios-buster:python3.7opencv4.1.2

USER root
RUN apt-get update --allow-releaseinfo-change
RUN apt-get upgrade -y
RUN apt-get install -y libraspberrypi-bin
RUN apt-get install  libopenjp2-7

RUN apt-get install -y qt5-default
RUN apt-get install -y python3-pyqt5.qtquick python3-pyside2.qtquick python3-pyside2.qtquickwidgets qml-module-qtquick-controls2 qml-module-qtquick2
RUN apt-get install -y tesseract-ocr

WORKDIR /home/pi/Desktop/Vision_Inspection/code/

#WORKDIR /appsrc
COPY ./ /home/pi/Desktop/Vision_Inspection/code/

ADD requirements.txt ./requirements.txt
RUN  python3 -m pip install  --upgrade pip
RUN  python3 -m pip install  -r requirements.txt 

WORKDIR /appsrc
#COPY ./ /appsrc/
# RUN ls /appsrc

#RUN chmod +x /appsrc/gui.py
#RUN chmod +x /appsrc/app.sh

#ENV START_UP = "/appsrc/app.sh"

RUN chmod +x /home/pi/Desktop/Vision_Inspection/code/gui.py
RUN chmod +x /home/pi/Desktop/Vision_Inspection/code/app.sh

ENV START_UP = "/home/pi/Desktop/Vision_Inspection/code/app.sh"