# IBD app

## Build
Flask and PostgreSQL database

## Deploy
Heroku

## Background
Inflammatory Bowel Diseases include Ulcerative Colitis (UC) and Chron's disease. IBDs impact the digestive tract. The result is that people who suffer from IBD need to severely restrict food they have. It is also very difficult to maintain social life as eating out is often a major risk and eating wrong type of food can significantly worsen the condition. This app will allow people with IBD to identify meals that they had in a restaurant that did not hurt them and share that information with others.
## Implementation plan
Developed in Flask with Jinja and Bootstrap. See requirements.txt for details.
The app will allow user to either recommended meals in the area or search restaurant in general and add new recommendation.
For restaurant information the app is calling Yelp's API. Author chose Yelp instead of TripAdvisor as their API docs were easier to understand.
User recommendations will then be combined with restaurant information from Yelp to provide searchable database of recommendations.
## Status
App is in the minimum viable product stage of development, deployed on Heroku.
Currently users can:
-	register, log in, and log out
- log in required only to make a recommendation
- all pages have a navbar with links to all sub-pages
-	pull and view restaurant information using Yelp API based on location and additional search terms
-	front page with buttons pointing to browse posts and add a meal pages
- page for browsing posts based on location only (for now - as number of posts grow, add additional search term)
- list posts, restaurant with latest post on top
- page for adding posts by finding restaurants and adding comments to restaurants
- add post by making a recommendation against the restaurant user selected (restaurant list and descriptions from Yelp)
- internal error handling, error logging and error email alerts

The list above completes first stage of the development. App is deployed as new features are added.

## Roadmap
- Additional search term for recommendations
- Email support for reset password
- Pagination for post recommendation search
- Register last logged-in user activity (login, logout, post search, rest search)
- Users declare UC or CD
- Vote for a post
- User can delete own recommendations in page 'My posts'
- Send feedback to developer - get in touch with us
- About page
