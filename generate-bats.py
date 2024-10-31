port = input("Enter comport number in the format [COMx], where x stands for the number of the com port: ")

with open("doorbell/write-to-ESP.bat","w") as file:
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp main.py :\n")
	file.write("echo 'Success!'")

with open("wristband/write-to-ESP.bat","w") as file:
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp main.py :")
	file.write("echo 'Success!'")

with open("install-micropython.bat","w") as file:
	file.write("./tools-and-binaries/esptool-v4.8.1-win64/esptool-win64/esptool.exe --port " + port + " erase_flash\n")
	file.write("./tools-and-binaries/esptool-v4.8.1-win64/esptool-win64/esptool.exe --chip esp32 --port " + port + " write_flash -z 0x1000 ./tools-and-binaries/ESP32_GENERIC-20240602-v1.23.0.bin")
	file.write("echo 'Success!'")

print(".bat files generated successfully!")