# matrbot

To execute this robot:

- log in in the robot (raspberry pi), read the lcd display to know the ip.

- run the following command:
```
sudo python3 asyncmain.py -H a2sq3y7mdrjtom.iot.us-east-1.amazonaws.com -e eb942de4 -r 8a0f4d2f -P 8883 -F ./robot/rootCA.pem -C ./robot/hugocerts/hugobot.certificate.pem -K ./robot/hugocerts/hugobot.private-key.txt --use-tls --tls-version=tlsv1.2
```
