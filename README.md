# VK FRIENDS REPORT GENERATOR
VK Friends Report Generator is a console application that generates a report consisting of your (or anyone else's) friends' data and save it in one of the three formats (".csv", ".tsv", ".json")



### User instructions:
1. Clone the project into your IDE
2. Type in terminal:
   ```console
   python main.py -a [ACCESS_TOKEN] -uid [USER_ID] -p [OUTPUT_FILE_PATH] -f [OUTPUT_FILE_FORMAT] -pg [PAGE] -l [LIMIT]
   ```
   * -a / --auth_token (required argument) – access token
   * -uid / --user_id (optional argument) – user id
   * -p / --output_path (optional argument, default: "report" in the working directory) – path to save the report
   * -f / --output_format (optional argument, default: "csv" – format of the report
   * -pg / --page (optional argument, if None, then no pagination) – requested page
   * -l / --limit (optional argument, default: 14, only works if _page_ is provided) – max page size
  
   #### Example input
   ```console
   python main.py -a vk1.a.m7VxRgYSK8UgTc1VXFdEFdFviqalIoQL2ljBAuFrVpzeyODYKOLqrG6UYod7NzMnmqYcFzv4RY2rZwiHY5X6WEyJg32v7Xo2QNae8lJgiuOgSAOzuGng8Az77eDfSRJvlQZrddlFFusfJVzCVQotvzV5vpjjRPju1VMWIzGdH8qRr_PxPe9mXP3k672Wwaqtugru2kZb67WTgt9PUD8DqQ -p res -f json -l 12 -pg 5
   ```   
     

### How to get vk access token:
1. Open https://vk.com/editapp?act=create
2. Create a standalone app
3. Open "settings"
4. Changes the app's state to "turned on"
5. Save the changes
6. Find App's ID and copy it
7. Insert https://oauth.vk.com/authorize?client_id=[APP'S-ID]&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&display=page into your browser's searchbar __(make sure to replace [APP'S-ID] with your app's id).__
   You should get somethings like this https://oauth.vk.com/authorize?client_id=123456&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&display=page
8. Authenticate if necessary
9. Extract __access_token__ and __user_id__ values from the link in the searchbar

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

