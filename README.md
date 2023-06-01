<a name="readme-top"></a>

# Students' Marks Telegram bot
## Description
This Python Telegram bot is designed for publishing students' marks. 

## Getting Started
### Configuring
Create a copy from `configs.json.example` file and rename the copy to `configs.json`.

```json
{
    "database":{
        "host":"", // Database Host.
        "user":"", // Database Username.
        "password":"", // Database Password.
        "database-name":"" // Database Name.
    },
    "telegram-bot":{
        "token":"", // Bot Access Token.
        "secret":"", // Generate your own secret number to be added to the flask endpoint url.
        "webhook":"" // Your webhook, ex, `https://yoursitedomain/{}`. The curly parentheses will be replaced with the specified secret.
    },
    "marks":{
        "template-message":"", // The file name for a text file that contains a template text message to be sent to the student along with their marks.
        "marks-file":"" // CSV file contains the students' marks.
    },
    "proxy-url":"" // Proxy server.
}
```

You should edit `Student.py` for parsing your CSV row to a student JSON object.

You should edit/extend `TemplateFiller` for filling the template message.

For changing the error messages you should create your own `messages.json` and edit the `flask_app.py` following line:

`messages = json.load(open(os.path.join(my_dir, '<your-file-name-here>.json')))`

```json
{
    "welcome-message":"",
    "enter-student-id":"",
    "wrong-student-id":"",
    "query-your-own-id":"",
    "unknown-message":"",
    "ensure-student-id":""
}
```

### Database
You should create a mysql database that has two tables as following:
#### Log table
This table records all the requests.

Table create sql:
```sql
CREATE TABLE `log` (
  `request_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `content` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
```

#### Student users table
This table pairs the student's Telegram user ID with their student ID, ensuring that users cannot request marks for other students.

Table create sql:
```sql
CREATE TABLE `student_users` (
  `std_id` varchar(10) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
```

## Contact

Iyas Ashaikhkhalil - [Linkedin](https://www.linkedin.com/in/eyaskhalil/) - eyasanwar@gmail.com

Project Link: [https://github.com/EyasAnwar/students-marks-bot](https://github.com/EyasAnwar/students-marks-bot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>