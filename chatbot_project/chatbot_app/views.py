from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import requests

# Set your OpenAI API key here
openai.api_key = "your_openai_api_key_here"

# OMDb API Key (replace with your key)
omdb_api_key = "your_omdb_api_key_here"

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

        title = data["Title"]
        year = data["Year"]
        genre = data["Genre"]
        plot = data["Plot"]
        actors = data["Actors"]

        return f"Title: {title}\nYear: {year}\nGenre: {genre}\nActors: {actors}\nPlot: {plot}"
    
    except Exception as e:
        return f"Error occurred while fetching movie information: {e}"

@csrf_exempt  # To handle POST requests from users
def chatbot(request):
    """Handle user input and generate chatbot response."""
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()
        if "movie" in user_input.lower() or "film" in user_input.lower():
            movie_name = user_input.split("movie")[-1].strip()  # Extract the movie name
            response = get_movie_info(movie_name)
        else:
            # Add user input to conversation history
            conversation_history.append(f"You: {user_input}")

            # If conversation history exceeds max length, truncate it
            if len(conversation_history) > max_history_length * 2:
                conversation_history.pop(0)  # Remove the oldest entry

            # Prepare the prompt (conversation history + user input)
            prompt = "\n".join(conversation_history)

            try:
                openai_response = openai.Completion.create(
                    engine="text-davinci-003",  # You can use other models like "gpt-3.5-turbo"
                    prompt=prompt,
                    max_tokens=150,
                    n=1,
                    stop=None,
                    temperature=0.7  # Controls creativity
                )

                message = openai_response.choices[0].text.strip()

                # Add response to conversation history
                conversation_history.append(f"Chatbot: {message}")
                response = message

            except Exception as e:
                response = f"Error occurred: {e}"

        return JsonResponse({"response": response})

    return JsonResponse({"error": "Invalid method. Use POST."}, status=405)

def index(request):
    return render(request, 'chatbot_app/chatbot.html')
