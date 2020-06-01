# imgsrcs-2D
## Image-Sources Method for 2D flat box-shaped room case and obtaining acoustic parameters
###### Project for MiNPwA

Algorithm:
1. Set the room parameters:
   - length, width of the box-shaped room
   - source position (omni), its SPL efficiency, air damping factor,
   - order of the Image-Sources method
   - assign reverb absorbing coefficients
2. Create and reflect mirror rooms, create their walls, image sources, assign alphas for each wall
3. Get the Room Impulse Response from all sources and plot Echogram
4. Calculate Schroeder Integral for next calculations
5. Obtain objective room-acoustics parameters: **EDT, T20, T30, T60, C50, D80**
6. Present the results on room maps

*Reference:*
*[1] Mehta, Bhadradiya - Measurement of Room Impulse Response Using Image Source Method*
*[2] Hak, Wenmaekers, van Luxemburg - Measuring Room Impulse Responses: Impact of the Decay Range on Derived Room Acoustic Parameters*
*[3] Lehmann, Johansson - Diffuse reverberation model for efficient image-source simulation of room impulse responses*