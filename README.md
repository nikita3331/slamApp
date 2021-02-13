# slamApp
 Main purpose of this project is to create self driving car. By creating the map of it's surroundings, car should be able to direct itself to proper position set by user. Project can be divided into three parts:

- User app:
  - By connecting to web socket user should see current map of room. Later on this map should be saved for out of a box usage. 
  - After pressing specific position on map, car should direct itself to chosen point.
  - User interface will be done in react-native. Map will be generated either as svg or fetched from server as image.
- Server:
  - Main ingredient of project. Data arrived from IMU and distance sensor will be transformed here to position of car and it's surroundings.
  - It will listen on two ports, one will be for connection to mobile app and the other one for connection to car sensors.
  - Position of car will be calculated from data sent by IMU. 
  - Initial position of the car should be known, so that later aproximations will be more aqurate.
  - Positions of objects near car will be calculated from distance points. If from one position object has one dimensions, and from the other, other position, then they should be aproximated by taking the average. Points will lie on the same plane, if they are close enough to each other.
- Car driver:
  - Car should be connected to web socket and send it's data constantly. 
  - Besides socket connection, car should turn the servo in 360$\degree$ and send the info about distances.
  - IMU info should be sent to server with current distance from point and angle.
  - User should be able to drive the car by pressing buttons in the app.
  
