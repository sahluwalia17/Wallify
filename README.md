Live at: wallifyy.herokuapp.com


Members:
<br/>Albert Zhong: zhong116@purdue.edu
<br/>Puja Maheshwari: maheshwp@purdue.edu
<br/>Sahil Ahluwalia: sahluwal@purdue.edu

Project Name: Wallify
<br/>Wallify is a webapp that will compile a user’s top songs and merge it into a wallpaper. Once assembled, users will be able to download the wallpaper that is arranged in order of ranking or have the option to fully customize the wallpaper and place album covers in the spots they desire. Users will be able to choose different time frames to pull top tracks from. The time frames would be 4 weeks, 6 months, and 2 years.

Features: 
<br/>- Spotify authentication: This is for the user to authorize Wallify for the user-top-read scope so that we can send an API GET request and be able to parse the response body for the track information
<br/>- Wallify authentication: This is for the user to provide Wallify with an email/password combination. Authentication will be conducted by the database. People will have the option to sign in as a guest. Unless signed in as a guest, users information will be stored in Firebase.
<br/>- Flask API backend: We have utilized Python module Flask to create our own backend API to handle the specific app routes that are provided by our flow execution.
<br/>- Download: Final page features a download button that will allow the user to download their customized wallpaper. This is done using a list in Javascript and using a AJAX POST request to communicate between the client and our backend. Through this request, we are able to receive the manipulated list and able to configure the wallpaper .jpg in the way the user wanted.
<br/>- Drag & Drop: Ability to customize the picture by dragging and dropping images onto others. Doing this will swap the positions of the two pictures. This was implemented through Javascript's parent/child function calls and DragEvent/DropEvent Protocols.
