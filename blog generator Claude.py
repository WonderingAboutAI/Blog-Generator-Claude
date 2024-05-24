import csv
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
dotenv_path = 'Path to ANTHROPIC_API_KEY.env'
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv('ANTHROPIC_API_KEY')
print("API Key:", api_key)  # Check what is printed

if not api_key:
    print("Error loading API key. Please check your .env file.")
    exit()  # Exit the script if no API key is found

# Initialize the Anthropic client with the API key
client = Anthropic(api_key=api_key)

def generate_blog_post(supporting_text_path):
    # Load supporting content from the text file
    supporting_content = ""
    if supporting_text_path:
        try:
            with open(supporting_text_path, 'r', encoding='utf-8') as file:
                supporting_content = file.read()
            print("Supporting content loaded successfully from the text file.")
        except Exception as e:
            print(f"Error reading supporting text file: {e}")
            return

    # Gather user inputs about blog details and preferences
    topic = input("Please desrcibe the topic of your blog and its intended audience: ")
    subtopics_count = int(input("Enter the number of subtopics: "))
    words_per_section = int(input("Enter the desired word count per section: "))
    blogger_identity = input("Please describe what kind of blogger you are (e.g., tech, health, etc.) and provide a short description of your background: ")
    writing_style = input("Enter your preferred writing style (conversational, formal, informal): ")
    word_choice = input("Enter any specific word choice preferences (e.g., use 'use' instead of 'utilize'): ")
    print(f"Generating an outline for the topic '{topic}' with {subtopics_count} subtopics, aiming for {words_per_section} words per section.")

    # Detailed system prompt based on the advanced template, including supporting content
    system_prompt = f"""
    You are a {blogger_identity} blogger writing in a {writing_style} style about '{topic}'. Include the following supporting content in your post: '{supporting_content}'. This post should engage a general audience interested in {topic}. The blog post should be structured with an introduction, {subtopics_count} main sections, and a conclusion. Avoid overused words such as 'crucial', 'explore', 'journey', and clichés like 'at the end of the day'. Focus on making complex ideas accessible without diluting the content's depth.
    """

    # Generate an outline including Introduction and Conclusion
    response = client.messages.create(
        max_tokens=1024,
        messages=[
            {"role": "user", "content": system_prompt + f" Generate a detailed outline about {topic} including an Introduction, {subtopics_count} detailed subtopics, and a Conclusion. Ensure each main section and subtopic starts with '**Section' for clarity. Include examples and references from experts. Be sure to cite sources."}
        ],
        model="claude-3-opus-20240229",
    )
    # Extracting text from the response object
    outline = '\n'.join(text_block.text for text_block in response.content)
    print("Outline generated successfully. Here's the outline:")
    print(outline)

    # Save the outline to a text file
    outline_filename = "blog_outline.txt"
    with open(outline_filename, "w") as file:
        file.write(outline)

    # Generate the full blog post based on the outline
    full_post_prompt = system_prompt + f" Now write a detailed blog post based on the following outline:\n{outline}\nAim for approximately {words_per_section * subtopics_count} words."
    response = client.messages.create(
        max_tokens=3000,
        messages=[
            {"role": "user", "content": full_post_prompt}
        ],
        model="claude-3-opus-20240229",
    )
    full_post_content = '\n'.join([text_block.text for text_block in response.content])
    print("Full blog post generated successfully.")

    # Save the full blog post to a text file
    text_filename = "complete_blog_post.txt"
    with open(text_filename, "w") as file:
        file.write(topic + "\n\n")
        file.write(full_post_content)

    return outline_filename, text_filename

# Example usage
supporting_text_path = 'content.txt'  # Specify the path to your supporting text file
generate_blog_post(supporting_text_path)
