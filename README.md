# Dumb Doorbell

The ELEC-C9801 Design Thinking and Electronic prototyping final project for Team#18

## Installing/uploading code

### Generating the .bat scripts for easier installation
Run "python generate-bast.py" and follow the instructions.
This is done, as otherwise if a single team member would edit a bat script to change the com port, if they pushed their changes, the com port would change for everyone else aswell, which is not wanted.

### Flashing the ESP32

Use the install-micropython.bat file to flash micropython onto the ESP32, if you don't have micropython on the controller yet.
Make sure to edit the .bat file to point to the correct COM port (check in your device manager under "Ports (COM & LPT)")

### Uploading python code to the ESP32

Use the write-to-ESP.bat files in the directories of the respective devices (main doorbell and wristband) to upload the code to the ESP32.
Make sure to edit the .bat file to point to the correct COM port (check in your device manager under "Ports (COM & LPT)")

### Encryption

- Create 2 16-byte strings to store the encryption keys.
- Put them in a file called "keys.txt" in the doorbell folder and switch into it
- Copy the "keys.txt" file to the ESP using: ```python ../tools-and-binaries/pyboard.py --device [serial-port-here] -f cp keys.txt :```
- Make another copy of the keys.txt file into the wristband folder
- Use the same command to copy the keys over to the ESP: ```python ../tools-and-binaries/pyboard.py --device [serial-port-here] -f cp keys.txt :```
