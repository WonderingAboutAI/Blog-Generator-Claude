# Blog-Generator-Claude
This Python script prompts Claude to first generate a blog outline and then a complete blog post. The system prompt includes information on the blogger's preferred audience and voice as well as writing samples and style guidance drawn from a text file.

**You will need an Anthropic API key to run this script.** 

## Features

### Prompt Development
Allows users to define the blog's topic, number of subtopics, word count per section, blogging identity, writing style, and specific word preferences to shape the content's tone and complexity.

### Support for Lengthy Instructions 
Incorporates additional insights, examples, and/or style guidelines provided through a supporting text file, enhancing the relevancy and depth of the generated content. A path to this file is defined in the script.

### Phased Content Generation
Automatically prompts Claude to first generate a structured outline with clearly labeled sections and then generate a blog based on this outline. 

### Output Management
Outputs the outline and blog post into separate text files.

## Usage

To run the script:

1. Ensure that Python and necessary packages are installed.
2. Set up your .env file with your ANTHROPIC_API_KEY.
3. Define the path to your supporting text file directly in the script or modify the script to accept it as a command-line argument.
4. Execute the script and follow the on-screen prompts to input your blog post details.
5. Open outputs **blog_outline.txt and complete_blog_post.txt.**
