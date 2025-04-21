import openai
import requests

# Set your OpenAI API key here
openai.api_key = "your_openai_api_key_here"

# OMDb API Key (replace with your key)
omdb_api_key = "your_omdb_api_key_here"

# JokeAPI URL
joke_api_url = "https://v2.jokeapi.dev/joke/Any"

# Weather API Key (replace with your key)
weather_api_key = "your_weather_api_key_here"
weather_api_url = "https://api.openweathermap.org/data/2.5/weather"

# Initialize conversation history
conversation_history = []
max_history_length = 10  # Limit the conversation history length

def get_movie_info(movie_name):
    """Fetch movie details from OMDb API."""
    base_url = "http://www.omdbapi.com/"
    params = {
        "t": movie_name,
        "apikey": omdb_api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if data.get("Response") == "False":
            return f"Sorry, I couldn't find any information about '{movie_name}'. Please check the spelling."
        
        # Extracting necessary movie details
        title = data.get("Title", "N/A")
        year = data.get("Year", "N/A")
        genre = data.get("Genre", "N/A")
        plot = data.get("Plot", "N/A")
        actors = data.get("Actors", "N/A")

        # Return formatted movie details
        return f"Title: {title}\nYear: {year}\nGenre: {genre}\nActors: {actors}\nPlot: {plot}"
    
    except Exception as e:
        return f"Error occurred while fetching movie information: {e}"

def get_joke():
    """Fetch a random joke from JokeAPI."""
    try:
        response = requests.get(joke_api_url)
        data = response.json()

        if data['type'] == 'single':
            return data['joke']
        elif data['type'] == 'twopart':
            return f"{data['setup']} \n{data['delivery']}"
        else:
            return "Sorry, I couldn't find a joke at the moment."
    except Exception as e:
        return f"Error occurred while fetching joke: {e}"

def get_weather(city_name):
    """Fetch weather details from OpenWeatherMap API."""
    params = {
        "q": city_name,
        "appid": weather_api_key,
        "units": "metric"
    }
    try:
        response = requests.get(weather_api_url, params=params)
        data = response.json()

        if data.get("cod") != 200:
            return f"Sorry, I couldn't retrieve weather information for {city_name}."
        
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return f"The current temperature in {city_name} is {temperature}°C with {description}."
    
    except Exception as e:
        return f"Error occurred while fetching weather information: {e}"

def chatbot_response(user_input):
    """Generate chatbot response."""
    # Check if the user is asking about a movie
    if "movie" in user_input.lower() or "film" in user_input.lower():
        movie_name = user_input.split("movie")[-1].strip()  # Extract the movie name from input
        return get_movie_info(movie_name)
    
    # Check if the user is asking for a joke
    elif "joke" in user_input.lower():
        return get_joke()

    # Check if the user is asking for the weather
    elif "weather" in user_input.lower():
        city_name = user_input.split("weather in")[-1].strip()
        return get_weather(city_name)

    # Add user input to conversation history
    conversation_history.append(f"You: {user_input}")
    
    # If conversation history exceeds max length, truncate it
    if len(conversation_history) > max_history_length * 2:
        conversation_history.pop(0)  # Remove the oldest entry (user or bot)

    # Prepare the prompt (conversation history + user input)
    prompt = "\n".join(conversation_history)

    try:
        # Generate response using OpenAI's GPT model
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use other models like "gpt-3.5-turbo" for faster response
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7  # Controls creativity. You can lower this for more deterministic answers
        )

        message = response.choices[0].text.strip()

        # Add response to conversation history
        conversation_history.append(f"Chatbot: {message}")

        return message

    except Exception as e:
        return f"Error occurred while generating chatbot response: {e}"

# Chatbot loop
print("Chatbot: Hello! I'm here to chat. Type 'exit' to quit.")
while True:
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye! It was nice chatting with you.")
        break

    # Get chatbot response
    response = chatbot_response(user_input)

    # Output the chatbot's response
    print("Chatbot:", response)
