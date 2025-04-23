from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import requests
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the trained intent classifier
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'intent_classifier.pkl')
intent_classifier = joblib.load(model_path)

# Get the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Get the OMDb API key from environment variables
omdb_api_key = os.getenv('OMDB_API_KEY')

# Initialize conversation history
conversation_history = []
max_history_length = 10  # Limit the conversation history length

# List to store movie metadata for similarity calculation (can expand this)
movie_metadata_cache = {}

def get_movie_info(movie_name):
    """Fetch movie details from OMDb API and return metadata."""
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

        # Save movie metadata for similarity calculations
        title = data["Title"]
        year = data["Year"]
        genre = data["Genre"]
        plot = data["Plot"]
        actors = data["Actors"]

        # Cache the metadata for future recommendations
        movie_metadata_cache[title] = {"genre": genre, "plot": plot, "actors": actors}

        return f"Title: {title}\nYear: {year}\nGenre: {genre}\nActors: {actors}\nPlot: {plot}"

    except Exception as e:
        return f"Error occurred while fetching movie information: {e}"

def get_recommendations(movie_name):
    """Fetch similar movies based on genre and plot similarity."""
    if movie_name not in movie_metadata_cache:
        return "Movie metadata not available. Please fetch movie details first."

    # List of movie metadata for similarity (could be expanded with more movies)
    movie_texts = []
    movie_titles = []

    for title, metadata in movie_metadata_cache.items():
        movie_titles.append(title)
        movie_texts.append(metadata['genre'] + " " + metadata['plot'])

    # Vectorize the movie metadata texts using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(movie_texts)

    # Calculate cosine similarity between the input movie and all others
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Get top 5 recommendations based on similarity scores
    recommended_indices = cosine_sim.argsort()[0][-5:][::-1]
    recommendations = [movie_titles[i] for i in recommended_indices]

    return recommendations


@csrf_exempt
def chatbot(request):
    """Handle user input and generate chatbot response."""
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()

        # Get intent prediction with confidence
        probs = intent_classifier.predict_proba([user_input])[0]
        max_prob = max(probs)
        intent = intent_classifier.classes_[probs.argmax()]  # Get predicted intent

        print("Predicted intent:", intent, "Confidence:", max_prob)  # Debugging output

        # If the confidence is too low, default to general chat
        if max_prob < 0.6:
            intent = "general_chat"

        if intent == "movie_info":
            movie_name = user_input.split("movie")[-1].strip()  # Extract the movie name
            response = get_movie_info(movie_name)
        elif intent == "recommendation":
            movie_name = user_input.split("like")[-1].strip()  # Extract movie name from "recommend something like X"
            recommendations = get_recommendations(movie_name)
            response = f"Here are some similar movies to '{movie_name}':\n" + "\n".join(recommendations)
        elif intent == "followup_info":
            response = "Please provide more details about the movie you're asking about."
        elif intent == "greeting":
            response = "Hello! 😊 How can I assist you today?"
        elif intent == "goodbye":
            response = "Goodbye! See you next time!"
        else:
            # Default for general chat
            conversation_history.append(f"You: {user_input}")

            # If conversation history exceeds max length, truncate it
            if len(conversation_history) > max_history_length * 2:
                conversation_history.pop(0)  # Remove the oldest entry

            # Prepare the prompt (conversation history + user input)
            prompt = "\n".join(conversation_history)

            try:
                # Correct OpenAI API call using new structure
                openai_response = openai.completions.create(
                    model="gpt-3.5-turbo",  # You can use other models like "gpt-4" or "gpt-3.5-turbo"
                    prompt=prompt + "\nUser: " + user_input + "\nChatbot:",  # Use the conversation prompt format
                    max_tokens=150,
                    temperature=0.7
                )

                message = openai_response['choices'][0]['text'].strip()

                # Add response to conversation history
                conversation_history.append(f"Chatbot: {message}")
                response = message

            except Exception as e:
                response = f"Error occurred: {e}"

        return JsonResponse({"response": response})

    return JsonResponse({"error": "Invalid method. Use POST."}, status=405)

def index(request):
    return render(request, 'chatbot_app/chatbot.html')
