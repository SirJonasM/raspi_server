= Further Notes
Here are some minor details that are important to run the benchmark correctly.
- .env files: Create .env files in the directory like this:
```env
DEVICE_NAME=<Device name>
```
this how the server and client get the name to write to in the CSV-Files.
- The controller script uses an shell script to make sure everything is installed. If not it tries to install everything and then runs the benchmark. Should there be an error in the installation process it wont run the benchmark.

