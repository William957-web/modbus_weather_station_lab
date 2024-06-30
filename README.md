## Hello World
This is a beginner ICS Security lab dealing with modbus protocol

## Setup
1. package installation:  
```py
sudo pip3 install -r requirements.txt
```

2. victim machine setup:  

The modbus server part:  
```py
sudo python3 station.py
```

Web UI:  
```py
sudo python3 app.py
```
It's EZ~  

## Exploit
**recon.py** is used to check registers' values.  
**set_register.py** is used to set a specific register value.  


*Have fun with weather station~*  
*Try to make it snowy through modbus protocol :>*  
*Also, you can stop this service !*
