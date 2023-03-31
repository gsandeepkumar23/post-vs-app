from flask import Flask, jsonify, request
import openai
import os
import traceback
app = Flask(__name__)

openai.api_key = " "

model_engine = "text-davinci-003"

def remove_special_characters(str):
    return str.replace("[^\w\s#]", '')

@app.route('/model-output', methods=['POST'])
def model_output_post():
    try:
        data = request.json
        title = remove_special_characters(data.get('title', ''))
        desc = remove_special_characters(data.get('desc', ''))
        prompt = remove_special_characters(data.get('prompt', '')[0])
        prompt=prompt+" "+title+" "+desc
        # print(prompt)
        print("Prompt:", prompt)

        # Check for the presence of the X-Request-Source header
        if 'X-Request-Source' in request.headers and request.headers['X-Request-Source'] == 'Postman':
            print('Request is coming from Postman')
        else:
            print('Request is coming from an application other than Postman')

        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # output_text = response.choices[0].text.strip()
        output_text = response.choices[0].text.lstrip()
        print("Output text:", output_text)

        # return remove_special_characters(output_text)
        return output_text
        
    except Exception as e:
        print('exception :bad response')
        # traceback.print_exc()
        print (e)
        return jsonify({"error": str(e)}), 500
    # except Exception as e: 
    #     print(str(e))
    

if __name__ == '__main__':
    app.run()
