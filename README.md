# IBD app
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
-	register, log in, and log out,
- log in required only to make a recommendation,
- all pages have a navbar with links to all sub-pages,
-	front page with cards pointing to browse posts and add a meal pages,
- page for browsing posts based on location only (for now - as number of posts grow, add additional search term),
- page for adding posts by finding restaurants and adding comments to restaurants,
-	pull and view restaurant information using Yelp API based on location and additional search terms,
- add post by making a recommendation against the restaurant user selected (restaurant list and descriptions from Yelp)

The list above completes first stage of the development. App is deployed as new features are added.

## Roadmap
- User New Relic to keep app from going to sleep
- Better error logging on Heroku
- Additional search term for recommendations 
- Pagination for restaurant search and recommendation search
- register last login and logout time for user
- Users declare what kind of IBD condition recommendation is for
- Endorse a recommendation
- Edit or delete own recommendations
- Add user profile page
- Better application structure with blueprints
- Chat with developer or message to developer
