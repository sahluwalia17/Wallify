Members:
<br/>Albert Zhong: zhong116@purdue.edu
<br/>Sahil Ahluwalia: sahluwal@purdue.edu
<br/>Puja Maheshwari: maheshwp@purdue.edu

Project Name: Wallify
<br/>Firebase: Database to store username/password
<br/>Flask: Handle backend and establish localhost
<br/>HTML/CSS: Handles frontend

Description
<br/>Wallify is a webapp that will compile a user’s top songs and merge it into a wallpaper. Once assembled, users will be able to download the wallpaper that is arranged in order of ranking or have the option to fully customize the wallpaper and place album covers in the spots they desire. The last feature is an auto-update feature where the program will automatically run every set amount of time specified by the user (every day, every week, every month, etc). This auto-update will run the program and see if there have been any changes to the user's top tracks. If there is a single change, the user is notified through their email and given a copy of the new wallpaper and a link to Wallify if they choose to customize their wallpaper again.

There are two sources of authentication to this:
<br/>- Spotify authentication: This is for the user to authorize Wallify for the user-top-read scope so that we can send an API GET request and be able to parse the response body for the track information
<br/>- Wallify authentication: This is for the user to provide Wallify with an email/password combination. The intent of this is so that Wallify can notify users through their email of any changes to their top tracks. This information will be stored in Firebase.
