# UAVPayload Simulation Test Script

This Python script simulates the UAVPayloadTAQ by sending **video** or **log data** to a host over the network. It is designed for testing the Ground Control Station (GCS) subsystem in isolation.  

## Features

- Stream MP4 video over UDP.  
- Send log data over TCP, with optional delay between each log line.  
- Supports verification of backend log persistence and UI display.
