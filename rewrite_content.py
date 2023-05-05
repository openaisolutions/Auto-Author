import openai
import yaml

# Load your API key
api_key = "your_api_key"
openai.api_key = api_key

def load_toc(file_path):
    # Load the table of contents from a YAML file
    with open(file_path, 'r') as toc_file:
        toc = yaml.load(toc_file, Loader=yaml.SafeLoader)
    return toc

def revise_toc(toc):
    print("Current table of contents:")
    for i, chapter in enumerate(toc['chapters']):
        print(f"{i+1}. {chapter['title']}")
        for j, section in enumerate(chapter['sections']):
            print(f"    {i+1}.{j+1}. {section['title']}")

    # Get user input
    chapter_index = int(input("Enter the chapter index to revise: ")) - 1
    section_index = int(input("Enter the section index to revise: ")) - 1
    new_title = input("Enter the new title for the section: ")

    # Revise the table of contents
    toc['chapters'][chapter_index]['sections'][section_index]['title'] = new_title

    print("Revised table of contents:")
    for i, chapter in enumerate(toc['chapters']):
        print(f"{i+1}. {chapter['title']}")
        for j, section in enumerate(chapter['sections']):
            print(f"    {i+1}.{j+1}. {section['title']}")

    return toc


def generate_gpt3_response(prompt):
    model_engine = "gpt-3.5-turbo"

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].text.strip()
    return message

def editorial_analysis(toc):
    issues = []

    for i, chapter in enumerate(toc['chapters']):
        for j, section in enumerate(chapter['sections']):
            content = section.get('content', '')

            # Create a prompt for GPT-3.5-turbo to analyze the section
            prompt = (
                f"As an expert book editor, critically analyze the following content from chapter {i + 1}, section {j + 1} titled '{section['title']}':\n\n"
                f"{content}\n\n"
                f"Editorial Analysis:"
            )

            # Get the analysis from GPT-3.5-turbo
            analysis = generate_gpt3_response(prompt)
            print(f"Editorial Analysis for Chapter {i + 1}, Section {j + 1} - {section['title']}:\n{analysis}\n")

            # If there are critical issues, add them to the issues list
            if "critical issue" in analysis.lower():
                issues.append({"chapter": i, "section": j, "analysis": analysis})

    return issues


def get_recommendations(toc, issues):
    # Code to get recommendations for improvement and re-writing
    recommendations = []

    for issue in issues:
        chapter_index = issue['chapter']
        section_index = issue['section']
        section = toc['chapters'][chapter_index]['sections'][section_index]

        # Create a prompt for GPT-3.5-turbo to generate recommendations for the section
        prompt = (
            f"Provide recommendations to improve the following chapter {chapter_index + 1}, section {section_index + 1} titled '{section['title']}' with the identified issue '{issue['issue']}':\n\n"
            f"Section Topic: {section['title']}\n\n"
            f"Issue: {issue['issue']}\n\n"
            f"Recommendations:"
        )

        # Get the recommendations from GPT-3.5-turbo
        recommendations_text = generate_gpt3_response(prompt)

        # Add the recommendations to the recommendations list
        recommendations.append({
            'chapter': chapter_index,
            'section': section_index,
            'issue': issue['issue'],
            'recommendations': recommendations_text
        })

    return recommendations


def rewrite_sections(toc, recommendations):
    for recommendation in recommendations:
        chapter_index = recommendation['chapter']
        section_index = recommendation['section']
        section = toc['chapters'][chapter_index]['sections'][section_index]

        # Create a prompt for GPT-3.5-turbo to rewrite the section based on the recommendation
        prompt = (
            f"Rewrite the following content from chapter {chapter_index + 1}, section {section_index + 1} titled '{section['title']}' according to the given recommendation:\n\n"
            f"{section['content']}\n\n"
            f"Recommendation:\n{recommendation['analysis']}\n\n"
            f"Rewritten Content:"
        )

        # Get the rewritten content from GPT-3.5-turbo
        rewritten_content = generate_gpt3_response(prompt)

        # Update the content in the table of contents
        toc['chapters'][chapter_index]['sections'][section_index]['content'] = rewritten_content
        print(f"Rewritten Content for Chapter {chapter_index + 1}, Section {section_index + 1} - {section['title']}:\n{rewritten_content}\n")

    return toc


def check_anti_patterns(toc):
    api_key = "your_api_key_here"
    openai.api_key = api_key
    model = "gpt-3.5-turbo"

    anti_patterns = {}

    for chapter_index, chapter in enumerate(toc['chapters']):
        for section_index, section in enumerate(chapter['sections']):
            section_id = f"chapter{chapter_index + 1}_section{section_index + 1}"

            # Construct a prompt to check for anti-patterns in the section
            prompt = f"Check the following section of a calculus textbook for anti-patterns:\n\nTitle: {section['title']}\nContent: {section['content']}\n\nAnti-patterns detected:"
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.5,
            )
            detected_anti_patterns = response.choices[0].text.strip()

            if detected_anti_patterns:
                anti_patterns[section_id] = detected_anti_patterns

    return anti_patterns




def main():
    # Load the table of contents from the YAML file
    toc = load_toc('_toc.yaml')

    # Revise the table of contents based on user input
    revised_toc = revise_toc(toc)

    # Perform a critical editorial analysis for each section
    issues = editorial_analysis(revised_toc)

    # Get recommendations for improvement and re-writing based on issues
    recommendations = get_recommendations(revised_toc, issues)

    # Rewrite sections based on recommendations
    rewritten_sections = rewrite_sections(revised_toc, recommendations)

    # Check for any anti-patterns in the rewritten content
    anti_patterns = check_anti_patterns(rewritten_sections)

    # Regenerate content for sections that still need improvement
    final_toc = regenerate_content(rewritten_sections, anti_patterns)

    # Save the final table of contents to the file
    save_toc(final_toc, '_toc.yaml')


if __name__ == "__main__":
    main()
