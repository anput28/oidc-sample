# OpenID Connect Sample Web App
This repo contains a simple web application that implements an authentication system following the OpenID Connect flows.<br>
This project has the goal of simulating the Signle Sign On authentication. In order to accomplish this goal the developed system involves three components:
- Back End, that performs the OIDC flows and expose a private endpoint.
- Front End, that try to access to the Back End's private endpoint.
- Identity Provider.

## Project Technologies:
- Front End: Angular 14.2.7
- Back End: Flask 2.2.3, Python 3.10
- Identity Provider: Auth0

## Implementation of OIDC Flows

![oidc](https://user-images.githubusercontent.com/61271430/234582355-0a8475ba-13e1-42b5-8389-9895c5f53ee9.png)

Step-by-step explanation:
1. User clicks the login button.
2. The Front End does a redirect to the login endpoint of the Back End.
3. The Back End does a redirect to the Identity Provider's authorization endpoint in to get the authorization code.
4. The Identity Provider displays the login page on the user's browser.
5. The user sends his credentials to the Identity Provider and authorizes the Back End to access his information.
6. The Identity Provider redirects to the redirect uri indicated by the Back End in the previous request, sending it the authorization code.
7. The Back End uses the authorization code to make a POST request to the Identity Provider's token endpoint to get the tokens (Id Token, Access Token, Refresh Token).
8. The Identity Provider sends the tokens.
9. The Back End saves the tokens in a session cookie and then redirects to the Front End home page sending the cookie to the browser.

## Identity Provider Configuration
For this project Auth0 was used as Identity Provider.<br>
The Back End component contains protected resources to which the Front End tries to access, so it was registered as an API in Auth0.<br>
The Front End components, instead, is an application that tries to access to a protected resources using the access token, so it was registered as a Single Page Application in Auth0.
