# Milestone Project 3
## A Gaming Review Website

This is my third milestone project. I decided to create a gaming review website where users can add reviews based on existing games in the database, users are also allowed to suggest games which an admin can review and then add to the database for further reviews.

This project includes interactivity, database management, pagination and ease of use. It is easy to navigate, easy to understand and has been testet by several people before publishing.

The project is deployed to heroku under:
## [Best-Reviews](https://best-reviews.herokuapp.com/)

## Table of Contents

1. **[UX](#UX)**

    * **[Wireframes](#wireframes)**
        * **[Home](#home)**
        * **[Browse](#browse)**
        * **[Top Games](#top-games)**
        * **[User Page](#user-page)**
        * **[Login](#login)**
        * **[Sign Up](#sign-up)**
    * **[User Stories](#user-stories)**

2. **[Features](#features)**

   * **[Existing Features](#existing-features)**
   * **[Future Features](#future-features)**

3. **[Technologies Used](#technologies-used)**

   * **[Languages](#languages)**
   * **[Libraries](#libraries)**
   * **[Tools](#tools)**
   * **[Hosting](#hosting)**
   
4. **[Testing](#testing)**

5. **[Deployment](#deployment)**

6. **[Credits](#credits)**


## Wireframes for the project

### Home
##### Desktop Version
<p align="center">
  <img alt="login" src="/app/wireframes/home.png">
</p>

##### Mobile Version
<p>
  <img alt="login" src="/app/wireframes/home_mobile.png">
</p>

### Browse
##### Desktop Version
<p align="center">
  <img alt="login" src="/app/wireframes/browse.png">
</p>

##### Mobile Version
<p>
  <img alt="login" src="/app/wireframes/browse_mobile.png">
</p>

### Top Games
##### Desktop Version
<p align="center">
  <img alt="login" src="/app/wireframes/top_games.png">
</p>

##### Mobile Version
<p>
  <img alt="login" src="/app/wireframes/top_games_mobile.png">
</p>

### User Page
##### Desktop Version
<p align="center">
  <img alt="login" src="/app/wireframes/user_page.png">
</p>

##### Mobile Version
<p>
  <img alt="login" src="/app/wireframes/user_page_mobile.png">
</p>

### Login
##### Desktop Version
<p align="center">
  <img alt="login" src="/app/wireframes/login.png">
</p>

##### Mobile Version
<p>
  <img alt="login" src="/app/wireframes/login_mobile.png">
</p>

### Sign Up
##### Desktop Version
<p align="center">
  <img alt="login" src="/app/wireframes/sign_up.png">
</p>

##### Mobile Version
<p>
  <img alt="login" src="/app/wireframes/sign_up_mobile.png">
</p>

I deviated a lot in the end from my wireframes in order to make my webpage better with more functionality, better searches and adding a admin tab which i did not consider in the start of this project.

## User Stories

As a user, I want to be able to:

* View reviews from any device (mobile, tablet, desktop).
* View reviews from other users to get new ideas.
* Easily navigate through the reviews, games, users by various main filters.
* View all reviews without beeing logged in.
* Rate reviews.
* Iterate through all reviews.
* Search reviews by user, rating and game.
* Suggest new games.
* Login and add my Reviews.
* Easily see all of the reviews I have submitted and iterate through them.
* Get the inspiration for the next game to play, by seeing top games or most reviewed games.
* Edit the reviews I've added.
* Delete the reviews I've submitted.
* Have a moderator that has access to everything in order to delete disturbing reviews and add new games.

## Features

### Existing Features

* **Navigation bar**        
    * For users to the site who are not logged in:    
      1. Index/Logo
      2. Browse Reviews      
      3. Top Games      
      4. All Games
      5. Login/Sign Up! 
   * For users who are logged in: 
      1. Index/Logo
      2. Browse Reviews      
      3. Top Games      
      4. All Games
      5. Your Reviews
      6. Logout
    * For admin/moderator: 
      1. Index/Logo
      2. Admin Tab
      3. Browse Reviews      
      4. Top Games      
      5. All Games
      6. Your Reviews
      7. Logout
   * The navbar is collapsed into a burger icon on small screens. The options remain the same, but they are instead accessed using a side navigation element which can be accessed through 'burger' icon at the top right. 
   
* **Footer**
   The footer social media links.

* **Cards**
    I used cards to illustrate all the reviews and games. There are 2 different types of cards.
        * Game cards show description of games, links to wikipedia, rating and pictures.
        * Review cards show from what game the review is, who wrote it, what rating was given and the review.
        * All cards are interactive and expand in order to show the complete description.
        * If user is logged in and accesses their own reviews then there are also edit and delete buttons.
    
    I also used a type of card/carousel in order to make it easier to navigate through big amounts of data for the admin which expands on interaction in order to review the description and beeing able to edit and delete everything.

* **Browsing**
    In order to browse all the reviews i implemented pagination, sorting and search in order to showcase all the reviews by user, game or rating as well as not to overcrowd the user.

* **Top Games**
    By accesing this page, the database updates all the games in order to show the correct average, total rating and total reviews, then renderes the page with the correct games in the order you want to see them. It only whos the top 6 games and is supposed to be a quick access for guests and users to maybe check out something new.

* **All Games**
    Here you can see all the games currently on the webpage/database, their description, average rating, picture and get redirected to their wikipedia page.

* **Your Reviews**
    On this page users can do all the CRUD operations.

    Here user can create (Crud), read (cRud), edit (crUd) and delete (cruD) all of their reviews as well as suggest a new game to be available for review to the moderator.
    Only available if you are logged in

* **Log In**
   The login page has an input form where the users have to enter their username and password.
   Upon failed login you'll get notified by a message, and on the bottom there is a redirect to the Sign Up option
   Disapears if logged in.

* **Sign Up**
    You can browse the webpage without beeing logged in but a lot of features are disabled if you do. I have built-in authentication and authorization on log in and checked if either user or email is already in the database before account creation. All passwords are hashed for security purposes!
    When a user registers,they are automatically logged in and redirected to the index page.
    Disapears if logged in.
    
* **Logout**
   Users log out by the navigation bar which will prompt a modal.
   Only available if you are logged in.

### Future Features

* **Search bar**
    I would like to implement a search where a user/guest could write in anything and it checks the database for users, games or snippets of description in order to show all the results containing that.
* **Review Rating**
    Users beeing able to rate other reviews and not just games is not yet implemented but i would like that to be able to in the future.

## Technologies Used

### Languages
*   HTML  
*   CSS
*   JavaScript
*   Python3

### Libraries
* Google Fonts
* Font Awesome
* Materialize
* Flask
* Jinja
* PyMongo

### Tools
* Visual Studio Code
* MongoDB Atlas
* Git
* GitHub
* AdobeXD

### Hosting
* Heroku

## Testing
Most of the testing was manual testing during the development and having the webpage and code already posted so that friends, family and coworkers could review the code and give feedback during development.

Several people have tested how the page displays on different devices, registered their own accounts, added their reviews, edited and deleted and given feedback to the general UX design of the page.

If you'd like to test the page yourself feel free to browse as a guest or create a user!
Please keep in mind not to use a password you use anywhere else as the passwords are only hashed.

### Validation Services
I tested my code with the following validation services:
* W3C Markup Validation  
* W3C CSS validation
* JSHint

On my local machine i used the standard validation and autocorrect of:
* VScode
* Werkzeug
* autopep8

### Responsiveness
Since my project was hosted almost immideately and i constantly had people looked at my progress i got a lot of feedback in regards to responsiveness and I also addressed all the issues that were brought up. To my knowledge there are no responsiveness issues at the current time.

Throughout the project I used chrome developer tools continuously and have constantly been checking weird css mistakes and responsiveness.

### Devices Used
These are the devices used throughout the testing/development:
* Samsung Galaxy S8 – Android 8.0
* OnePlus 6T - OxygenOS, Android 10
* Apple Macbook Air - Safari browser
* Apple iPhone 6,7 &8S - Safari Browser
* iPad Mini - Safari Browser
* Desktop - Chrome v.74
* Desktop - Firefox v.67
* OnePlus 6T - OxygenOS, Android 10
* Samsung Galaxy S8 – Android 8.0

### Browsers Used
These are the browsers used throughout the testing/development:
    Chrome
    Firefox
    Microsoft EdgeThe site has been tested successfully on 

## Features Testing
 * **Creating**
    Me and others have created and tried to create several accounts, with and without email, wrong emails, tried to create duplicates. Logged in to existing accounts.

    We also created reviews in different sizes, with different rating, same rating, suggested games, checked that the counters update correctly and won't get overwritten, made sure that my personal ID iteration for users, reviewsm game and suggestions works as intended.

    We also tried all that with the admin account and as a guest.
    
    Everything seemed to work as expected
* **Reading**
    Checking all the possibilities of the browse tab kind of made sure that everything was read as intended and didn't spit out any errors. When i started the browse tab i started having all sorts of problems with both reading, sorting, and iterating through items, in hindsight it might have been easier to have all the reviews as a list of objects under each game in the games collection instead of several different collections, but i had already gotten so far in the coding that I decided against it.

    I instead created a counter and stored all the information that is posted as session variables and that seemed to fix all my previous issues. 

    Since then I have clicked on everything, double checked all the sorting so that it sorts as intended, made sure that the id's given to each review, game and user is as intended and checked the pagination, all the tabs that are supposed to read games, reviews and users.

    The admin tab specifically for the moderator also made sure that everything was read as it was supposed to be and that everything was showing up.

* **Updating**
    Several people and me ensured that everything that is to edit was editable and didn't throw out any errors by adding numbers, signs, weird letters and so on and it seemed to work nice.
    During my development I ended up accidentally updating the counters, which i use to create unique ID's, in an incorrect way and suddenly everything was wrong. I ended up fixing this and resolved to never update the counter except of incrementing it and haven't found any problems since.

* **Deleting**
    During the development of the project A LOT of people had created users, games, reviews and suggestions and we all therefore tested thoroughly that all the deletion worked as properly.

    Since I had over 200 reviews at some point I decided to implement the automatic deletion of all reviews connected to a game/user when a game or user is deleted. This ended up saving a lot of time and me converting completely over to the Admin tab for navigating, creating, updating and deleting things from the database and only using mongoAtlas UI to double check in between since it was easier and quicker to use my own Admin tab.

* **Known Issues**
    There are no known issues at this point.

## Deployment
### Deployment To Heroku
In order the deploy my project to Heroku I have completed the following steps:

 **VScode IDE**
* Created a Procfile with the command echo web: python run.py > Procfile. (Windows has a specific problem which I ran into where the Procfile is specifically declared as a .txt file and therefore ended up not beeing able to be read by heroku. Simply open the Procfile in Notepad++ copy everything, delete the file and save the copied information into a new Notepad++ file which will be saved and named Procfile without any extension.)
* Created a requirement.txt file so Heroku know what python modules it will need to run my application with the command pip freeze --local > requirements.txt
* Then git add and git commit the new prerequisites from the requirements.txt file and Procfile, then 'git push' the undertaking to GitHub.
* Created environmental variables, i.ex. client, db, admin_password, secret_key and added them to .gitignore in order not to upload any of my private information. There is an example of .env in the code. 

 **Heroku**
* After loging into heroku I created a new app, using the name best-reviews and set the region to Europe.
* Select application
* In the settings tab reveal config vars and add all your environmental variables there. For example client, db, admin_password and secret_key
* From the heroku dashboard of your newly created application, click on "Deploy" > "Deployment method" and select GitHub.
* Confirm the linking of the heroku app to the correct GitHub repository.
* In the heroku dashboard, click "Deploy".
* In the "Manual Deployment" section of this page, made sure the master branch is selected and then click "Deploy Branch".
* The site is now successfully deployed.

### Link to the deployed page:
* https://best-reviews.herokuapp.com/¨

## Credits
* All picture links, game descriptions and wikipedia links are taking from Wikipedia.
* Logo is taken from https://www.pexels.com/photo/pink-and-black-nintendo-ds-1462725/
* All of the reviews have been taken from https://www.metacritic.com/

### Tutorials
* https://www.youtube.com/watch?v=jJ4awOToB6k for learning how to create hash passwords
* https://stackoverflow.com for a lot of tips regarding everything, my go to place if i have a question regarding anything

### Acknowledgements
* Special thanks to friends, family and coworkers for helping me during development, testing and giving me ideas and implementations that i could use to create this project.
* https://github.com/stephyraju/spiceworld/blob/master/README.md I used this project as a guideline for my README.md, and
pagination, the section of how to deploy the project to heroku is almost completely copied since it was exactly what I did. 