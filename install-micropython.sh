#bin/sh

#set the correct COM port, check COM port in Device Manager under Ports (Silicon Labs CP210x USB to UART bridge)
./tools-and-binaries/esptool-v4.8.1-win64/esptool-win64/esptool.exe --chip esp32 --port COM11 write_flash -z 0x1000 ./tools-and-binaries/ESP32_GENERIC-20240602-v1.23.0.bin

