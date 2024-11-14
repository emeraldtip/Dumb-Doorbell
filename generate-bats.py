port = input("Enter comport number in the format [COMx], where x stands for the number of the com port: ")

with open("doorbell/write-to-ESP.bat","w") as file:
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp main.py :\n")
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f mkdir templates\n")
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp templates/index.html :templates/index.html\n")
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f mkdir static\n")
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp static/index.css :static/index.css\n")

with open("doorbell/copy-libraries-to-ESP.bat","w") as file:
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp microdot.py :\n")
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp utemplater.py :\n")
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f mkdir utemplate :\n")
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp utemplate/compiled.py :utemplate/compiled.py\n")
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp utemplate/recompile.py :utemplate/recompile.py\n")
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp utemplate/source.py :utemplate/source.py\n")

with open("wristband/write-to-ESP.bat","w") as file:
	file.write("python ../tools-and-binaries/pyboard.py --device " + port + " -f cp main.py :")
	file.write("echo 'Success!'")

with open("install-micropython.bat","w") as file:
	file.write("./tools-and-binaries/esptool-v4.8.1-win64/esptool-win64/esptool.exe --port " + port + " erase_flash\n")
	file.write("./tools-and-binaries/esptool-v4.8.1-win64/esptool-win64/esptool.exe --chip esp32 --port " + port + " write_flash -z 0x1000 ./tools-and-binaries/ESP32_GENERIC-20240602-v1.23.0.bin")

print(".bat files generated successfully!")