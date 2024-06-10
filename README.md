# Introduction 
Voltrox Social Media Task: Implement a basic backend system for user profiles and a social media feed using any programming language and database of your choice. You are encouraged to be creative and add additional features to enhance functionality and user experience.

### Primary Features to Implement:

**User Profile Management:**
- View and edit personal details (Full name, Email Address).
- Update profile pictures.

**Social Media Feed:**
- Post updates with text content.
- Like and reply to posts.
- Display the number of likes and replies on each post.
- Enhance the feed with tags or categories such as #Politics, #Cityparty, #Freedom, etc.

### Additional Features:
- Implemented api functionality to find posts by tags.
- Include multimedia support (images, videos) in posts.
- Real-time updates without needing to refresh the page using django channels.
- Implement user authentication and authorization.
- Added signup and login with google 

# Getting Started

Follow these steps to get the code up and running on your system:

## 1. Installation Process

1. **Clone the Repository:**
   ```sh
   git clone <repository_url>
   ```

2. **Create a Virtual Environment:**
   ```sh
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. **Install the Required Packages:**
   ```sh
   pip install -r requirements.txt
   ```

5. **Add Environment Variables:**
   Create a `.env` file in the root directory and add the necessary environment variables as specified in `example.env`.

6. **Install and Run Redis:**
   - Install Redis from [Redis.io](https://redis.io/download).
   - Start the Redis server:
     ```sh
     redis-server
     ```

## 2. Build and Test

1. **Run the Django Development Server:**
   ```sh
   python manage.py runserver
   ```

2. **Access the Application:**
   Open your web browser and go to the link provided in the terminal to view the Swagger documentation.

3. **Connect to the WebSocket:**
   Use the following WebSocket URL to connect:
   ```
   ws://localhost:8000/ws/feed/?token=<your_jwt_token>
   ```
   Note: Replace `<your_jwt_token>` with the correct bearer token for the logged-in user.


# Put together  by:
Desmond Nnebue
nnebuedesmond@gmail.com