# MapsToAtakFormatter

## How to use
1. Create a new map in [Google My Maps](https://www.google.com/mymaps)
2. Rename the layers to: "0 - ...", "1 - ...", ... .
3. Add markers
   <br>![image](https://github.com/user-attachments/assets/484ff17c-26b8-4fbb-87f5-e842498de551)
   ![image](https://github.com/user-attachments/assets/22201508-0a14-496f-8044-073ccedc3329)
5. Create a ```.env``` file and add the link from Googe My Maps as ```URL="YOUR_GOOGLE_MY_MAPS_LINK"```
6. Run the Docker build command ```docker build -t formatter .```
7. Run the Docker run command ```docker run --rm -v $(pwd):/src/output formatter```
8. Copy the .kmz files from ```òutput``` directory into your device ```atak/overlays``` directory
9. Import the files inside the ```Atak```
![1748284025637](https://github.com/user-attachments/assets/d4c8ab8c-c6f5-46ac-99aa-7fb14965f75d)
Select ```Local SD``` and import the files inside of ```atak/overlays``` directory
![1748284025635](https://github.com/user-attachments/assets/d131316b-58c4-4394-afab-c082377e863f)
10. Enjoy!
![1748284025639](https://github.com/user-attachments/assets/467f21fe-193c-4003-97ce-a3f95d594a07)
