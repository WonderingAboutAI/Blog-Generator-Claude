# Blog-Generator-Claude
**Version 1** of this Python script prompts Claude to first generate a blog outline and then a complete blog post based on the outline. The system prompt includes information on the blogger's preferred audience and voice as well as writing samples and style guidance drawn from a text file.

**Version 2** prompts Claude to generare posts by feeding it one section of the outline at a time. It also saves the outline and blog copy in a .csv file with columns named Section Name, Blog Content, and Outline Content and supports the same system detailed system prompt described above.

**You will need an Anthropic API key to run this script.** 

## Features

### Prompt Development
Allows users to define the blog's topic, number of subtopics, word count per section, blogging identity, writing style, and specific word preferences to shape the content's tone and complexity.

### Support for Lengthy Instructions 
Incorporates additional insights, examples, and/or style guidelines provided through a supporting text file, enhancing the relevancy and depth of the generated content. A path to this file is defined in the script.

### Phased Content Generation
#### Version 1
Automatically prompts Claude to first generate a structured outline with clearly labeled sections and then generate a blog based on this outline. 

#### Version 2
Automatically prompts Claude to generate a structured outline with clearly labeled sections and then feeds each section of the outline to Claude for writing in a separate promot.

### Output Management
#### Version 1
Outputs the outline and blog post into separate text files.

#### Version 2
Outputs the outline sections and corresponding blog copy to a .csv. Outputs complete blog copy into a text file.

## Usage

To run the script:

1. Ensure that Python and necessary packages are installed.
2. Set up your .env file with your ANTHROPIC_API_KEY.
3. Define the path to your supporting text file directly in the script or modify the script to accept it as a command-line argument.
4. Execute the script and follow the on-screen prompts to input your blog post details.
5. Open outputs. For Version 1: **blog_outline.txt and complete_blog_post.txt.**. For Version 2: **blog_outline.csv and blog_post.txt.**
