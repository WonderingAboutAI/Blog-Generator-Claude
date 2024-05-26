import csv
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
dotenv_path = 'ANTHROPIC_API_KEY.env'
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv('ANTHROPIC_API_KEY')

if not api_key:
    print("Error loading API key. Please check your .env file.")
    exit()  # Exit the script if no API key is found

# Initialize the Anthropic client with the API key
client = Anthropic(api_key=api_key)

# Define the path to the supporting text file inside the script
supporting_text_path = 'content.txt'

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
    topic = input("Please describe what you'd like to write about: ")
    subtopics_count = int(input("Enter the number of subtopics: "))
    words_per_section = int(input("Enter the desired word count per section: "))
    blogger_identity = input("Write a few words about what you typically blog about, your point of view, and your intended audience: ")
    writing_style = input("Enter your preferred writing style (formal, informal, conversational): ")
    word_choice = input("Enter any specific word choice preferences (e.g., use 'use' instead of 'utilize'): ")
    print(f"Generating an outline for the topic '{topic}' with {subtopics_count} subtopics, aiming for {words_per_section} words per section.")

    # Modify the system prompt to include user preferences and language guidelines
    system_prompt = f"You are a {blogger_identity} blogger writing in a {writing_style} style. Here are the details to consider: {supporting_content} Preferred word choices: {word_choice}. Generate content accordingly."

    # Generate an outline including Introduction and Conclusion
    
    response = client.messages.create(
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f" Generate a detailed outline about {topic} including an Introduction, {subtopics_count} detailed subtopics, and a Conclusion. Ensure each main section and subtopic starts with '**Section' for clarity. Include examples and references from experts. Be sure to cite sources."}
        ],
        model="claude-3-opus-20240229",
        system=system_prompt
    )
    # Extracting text from the response object
    outline = [text_block.text.split('\n') for text_block in response.content]
    print("Outline generated successfully. Here's the outline:")
    print(outline)


    # Process the entire outline, capturing Introduction, each Subtopic, and Conclusion as distinct sections
    section_content = []
    current_section = []
    section_label = None  # Initialize as None to avoid capturing content before the first valid header
    for lines in outline:  # Here, lines is a list of strings
        for line in lines:  # Now line is a string
            if "**Section" in line or "**Introduction" in line or "**Conclusion" in line:
                if section_label is not None:  # Save current section if a label has been set
                    section_content.append({"label": section_label, "content": " ".join(current_section).strip()})
                current_section = []
                section_label = line.strip().replace('**', '')  # Update section label
            if section_label is not None:
                current_section.append(line.strip())
    if section_label is not None and current_section:  # Save the last section
        section_content.append({"label": section_label, "content": " ".join(current_section).strip()})

    print("Processed sections for content generation:")
    for section in section_content:
        print(section['label'])

    # Save to CSV
    csv_filename = "blog_outline.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Section Name', 'Outline Content', 'Blog Content'])  # Define column headers

    # Generate content for each processed section and write to CSV
    contents = []
    for section in section_content:
        prompt = f"Write a detailed blog post section in the first person about the following: {section['content']} Aim for approximately {words_per_section} words."
        response = client.messages.create(
            max_tokens=3000,
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="claude-3-opus-20240229",
            system=system_prompt
        )

        generated_content = [text_block.text.strip() for text_block in response.content]
        content_str = ' '.join(generated_content)  # Join list into single string
        contents.append({"section": section['label'], "content": content_str})
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([section['label'], section['content'], content_str])
        print(f"Generated content for {section['label']}")

    print("Blog content generated and saved to CSV.")

    # Create formatted text file
    text_filename = "blog_post.txt"
    with open(text_filename, mode='w') as file:
        for content in contents:
            file.write(content['section'] + "\n\n")  # Include section heading
            file.write(content['content'] + "\n\n")  # Include section content
    print("Blog post saved to text file.")    


    return csv_filename, text_filename

# Run function
generate_blog_post(supporting_text_path=supporting_text_path)
