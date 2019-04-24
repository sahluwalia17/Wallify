Members:
<br/>Albert Zhong: zhong116@purdue.edu
<br/>Sahil Ahluwalia: sahluwal@purdue.edu
<br/>Puja Maheshwari: maheshwp@purdue.edu

Project Name: Wallify
<br/>Firebase: Database to store username/password
<br/>Flask: Handle backend and establish localhost
<br/>Heroku: Deploys website
<br/>HTML/CSS: Handles frontend

Description
<br/>Wallify is a webapp that will compile a user’s top songs and merge it into a wallpaper. Once assembled, users will be able to download the wallpaper that is arranged in order of ranking or have the option to fully customize the wallpaper and place album covers in the spots they desire. Users will be able to choose different time frames to pull top tracks from. The time frames would be from a couple weeks back, a couple months back, and a couple years back.

There are two sources of authentication to this:
<br/>- Spotify authentication: This is for the user to authorize Wallify for the user-top-read scope so that we can send an API GET request and be able to parse the response body for the track information
<br/>- Wallify authentication: This is for the user to provide Wallify with an email/password combination. Authentication will be conducted by the database. People will have the option to sign in as a guest. Unless signed in as a guest, users information will be stored in Firebase.
