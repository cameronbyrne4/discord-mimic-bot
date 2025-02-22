# Cam-Bot: A Personalized Discord AI Companion

https://youtu.be/9dGA6i9_-Bw

I built this while studying abroad at the National University of Singapore. With a 16 hour time zone difference to home, it's a struggle to keep in contact with my close friends due to our mismatched work and sleep schedules and the fact that we aren't in the same stages of the day. Like in the morning, we could typically talk about what we want to accomplish with the day. I made this project to allow my friends an outlet to talk to me when I'm not present, and learned some new technologies while working on it!

A Discord bot that mimics a specific person's texting style and personality, complete with contextual memory and scheduled interactions. Built with Python, Discord.py, MongoDB, and OpenAI's GPT-3.5.

## 🌟 Features

- **Personality Mirroring**: Mimics a specific person's texting style, slang usage, and emoji patterns
- **Contextual Memory**: Remembers previous conversations and maintains context
- **Scheduled Messages**: Sends automated morning and night messages
- **MongoDB Integration**: Stores chat history and user interactions
- **Style Analysis**: Analyzes message patterns, common phrases, and emoji usage

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- MongoDB
- Discord Bot Token
- OpenAI API Key

### Environment Variables

Create a `.env` file in the root directory:
DISCORD_TOKEN=your_discord_token
MONGODB_URI=your_mongodb_uri
OPENAI_API_KEY=your_openai_api_key

### Installation

1. Clone the repository
git clone https://github.com/yourusername/cam-bot.git
cd cam-bot

2. Create and activate virtual environment
cd backend
python -m venv newenv
source newenv/bin/activate # On Windows: newenv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Start the bot
python -m backend.app.main
or what I've been doing
cd backend
uvicorn app.main:app --reload


### Adding the Bot to Your Discord Server

1. **Create a Discord Application**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on "New Application" and give it a name.

2. **Create a Bot User**:
   - In your application settings, navigate to the "Bot" tab.
   - Click "Add Bot" and confirm.

3. **Get Your Bot Token**:
   - Under the "Bot" tab, you will see a "Token" section. Click "Copy" to copy your bot token.

4. **Invite the Bot to Your Server**:
   - In the "OAuth2" tab, under "Scopes", select `bot`.
   - Under "Bot Permissions", select the permissions your bot needs (e.g., `Send Messages`, `Read Message History`).
   - Copy the generated URL and paste it into your browser to invite the bot to your server.

### Customizing the Bot for Different Users

To prevent abuse and ensure fair usage of OpenAI tokens, users are required to create their own bot instances. This allows each user to customize their bot's personality and settings without impacting others.

1. **Modify User-Specific Settings**:
   - In the `AIService` class, you can adjust the character description and style characteristics to match the user you want the bot to mimic as well as note personality traits. These are texting conventions and contexts that might go beyond what the iMessage data can convey.

### Querying Your Library/Messages/chat.db Data

To extract messages from your iMessage database, you can use an SQL viewer like SQLPro. This is because I did not have authorization to work with chat.db directly from my program. Follow these steps:

1. **Open SQLPro** (or your preferred SQL viewer).
2. **Connect to your chat.db**:
   - Navigate to `~/Library/Messages/chat.db` and open the database file.

3. **Run the Following Query**:
sql
SELECT
message.text,
message.date,
message.is_from_me,
handle.id
FROM message
LEFT JOIN handle ON message.handle_id = handle.ROWID
WHERE message.text IS NOT NULL
AND message.is_from_me = 1
ORDER BY message.date DESC
LIMIT 1000;

4. **Export the Results**:
   - After running the query, export the results to a JSON file.
   - Save the JSON file in the `app/scripts` directory, naming it `my_1000_messages.json`

5. **Run the iMessage Parser**:
   - After exporting the JSON file, run the `imessage_parser.py` script to process the messages.
   - You can run the script using the following command:
   ```
   python -m backend.app.services.imessage_parser
   ```
   - This will parse the messages and prepare them for use by the bot.

### Bot Commands
**Using Commands**:
   - Once the bot is running in your Discord server, you can interact with it using commands in any text channel where the bot has access.
   - **Basic Commands**:
     - `!chat <message>`: Talk to the bot.
     - `!hello`: Basic greeting test.

### Example Interactions
User: !chat what's up?
Bot: yo just chillin at the lib rn tryna study but its mad boring 💀💀
User: !chat what's my favorite color?
Bot: bruh u told me earlier its blue


## 🛠 Technical Implementation

### AI Service
The bot uses OpenAI's GPT-3.5 model with custom prompting to maintain consistent personality. Reference:
python:backend/app/services/ai_service.py
startLine: 141
endLine: 188

### Message History
MongoDB stores and retrieves chat history for context-aware responses. Reference:
python:backend/app/services/message_service.py
startLine: 27
endLine: 41

### Scheduled Messages
Automated messages are sent at specific times (10 AM and 1 AM PST). Reference:
python:backend/app/bot/discord_bot.py
startLine: 43
endLine: 68

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-3.5
- Discord.py team
- MongoDB team
- All contributors and testers

## 📞 Contact

Cameron Byrne - [LinkedIn](https://www.linkedin.com/in/cameronbyrne00/)

Project Link: [https://github.com/cameronbyrne4/cam-bot](https://github.com/cameronbyrne4/cam-bot)

