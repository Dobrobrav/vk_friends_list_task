# VK FRIENDS REPORT GENERATOR
VK Friends Report Generator is a console application that generates a report consisting of your (or anyone's) friends' data and save it in one of the three formats (".csv", ".tsv", ".json")



### User instructions:
1. Clone the project into your IDE
   ...

### How to get vk access token:
1. Open https://vk.com/editapp?act=create
2. Create a standalone app
3. Open 'settings'
4. Turn the app on
5. Find App's ID and copy it
6. Insert https://oauth.vk.com/authorize?client_id=[APP'S-ID]&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&display=page into your browser's searchbar __(make sure to replace [APP'S-ID] with your app's id!!)__
7. Authenticate if necessary
8. Extract __access_token__ and __user_id__ values from the link in the searchbar

### Example output:
...


### How the app works:
...


### Used API endpoints:
This app uses the vk API endpoint https://api.vk.com/method/friends.get/ for getting friends list of a vk user.
#### Params:
 * access_token - token for accessing vk user data
 * user_id - id of a vk user
 * order - ordering field. "name" value is used for sorting the list by names in alphabetic order
 * count - maximum quantity of friends. Used for pagination
 * offset - how many friends to skip. Also used for pagination
 * fields - list of extra fields to be returned. "bdate, city, country, sex" value is used in the app to get birthday, city, country and sex information about each friend.
 * v - version of vk API. "5.131" is used

