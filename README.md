# IBD app
## Background
Inflammatory Bowel Diseases include Ulcerative Colitis (UC) and Chron's disease. IBDs impact the digestive tract. The result is that people who suffer from IBD need to severely restrict food they have. It is also very difficult to maintain social life as eating out is often a major risk and eating wrong type of food can significantly worsen the condition. This app will allow people with IBD to identify meals that they had in a restaurant that did not hurt them and share that information with others.
## Implementation plan
Developed in Flask with Jinja and Bootstrap. See requirements.txt for details.
The app will allow user to either recommended meals in the area or search restaurant in general and add new recommendation.
For restaurant information the app is calling Yelp's API. Author chose Yelp instead of TripAdvisor as their API docs were easier to understand.
User recommendations will then be combined with restaurant information from Yelp to provide searchable database of recommendations.
## Current status
App is in the early stage of development
Currently users can:
-	log in, register, and log out,
- all pages have a navbar
-	see the front page,
- page for browsing posts based on location only (for now),
- page for adding posts by finding restaurants and adding comments to restaurants 
-	pull and view restaurant information using Yelp API based on location and one additional search term
- add post by making a comment against the restaurant user selected (restaurant list and descriptions from Yelp)

The list above completes first stage of the development.

Many new features will be added in the second stage of the development following test user group feedback.
