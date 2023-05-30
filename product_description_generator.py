import openai
import csv

openai.api_key = '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 '

def generate_description(prompt, description_length):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=description_length
    )
    description = response.choices[0].text.strip()
    return description

descriptions = []

with open('products.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        product_name = row['Product Name']
        prompt = row['Prompt']

        short_descriptions = []
        long_descriptions = []

        for _ in range(4):
            short_description = generate_description(prompt, 150)
            long_description = generate_description(prompt, 300)

            short_descriptions.append(short_description)
            long_descriptions.append(long_description)

        descriptions.extend([
            {
                'Product Name': product_name,
                'Short Description': short_description,
                'Long Description': long_description
            }
            for short_description, long_description in zip(short_descriptions, long_descriptions)
        ])

with open('product_descriptions.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Product Name', 'Short Description', 'Long Description'])
    writer.writeheader()
    writer.writerows(descriptions)

