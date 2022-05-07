# Authentication With Flask
Here with this project we are going to learn Authentication with Flask So have Fun.

## Project overview

![project_overview](https://user-images.githubusercontent.com/57592040/167265729-29c3fd07-41f9-49d3-ac2f-8808c427a780.gif)

In this overview we can see how we login , register and logout and how the user need to be login to get to the secret page and download the pdf file as well, plus how the home page changed as current user is already login or logout.

**What we will discuss with this project?**

1. secure your users passwords by using `werkzeug.security` tools 
2. Manage user session by using `flask_login`  extension.
3. update the pages if the current user is authenticated.

**I will not discuss adding adding and styling web pages templates or flask starter configurations, so lets began.**

#### secure your users passwords by using `werkzeug.security` tools 

In sample way we need to save our users passwords encrypted in our database instead of saving them as plan text so if our database stolen by bad guys at least the need ages to decrypting our users passwords and to do so we are going to use `generate_password_hash` function from `werkzeug.security` library 
