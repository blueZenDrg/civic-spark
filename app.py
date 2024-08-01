from flask import Flask, render_template, request, jsonify, send_file
from civic_spark_app import CivicSparkApp
from html_report import generate_html_report
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
api_key = os.environ.get("GEMINI_API_KEY")
civic_app = CivicSparkApp(api_key)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_process', methods=['POST'])
def start_process():
    data = request.json
    idea = civic_app.input_idea(data['description'], data['country'], data['city'], data['user_age'])
    questions = civic_app.get_refining_questions(idea)
    return jsonify({'questions': questions})

@app.route('/refine_idea', methods=['POST'])
def refine_idea():
    data = request.json
    idea = civic_app.ideas[-1]
    civic_app.add_refined_details(idea, data['answers'])
    return jsonify({'message': 'Idea refined successfully'})

@app.route('/get_global_examples', methods=['POST'])
def get_global_examples():
    idea = civic_app.ideas[-1]
    civic_app.provide_global_examples(idea)
    return jsonify({'examples': idea.global_examples})

@app.route('/assess_feasibility', methods=['POST'])
def assess_feasibility():
    idea = civic_app.ideas[-1]
    civic_app.assess_local_feasibility(idea)
    return jsonify({'feasibility': idea.local_feasibility})

@app.route('/get_breakthroughs', methods=['POST'])
def get_breakthroughs():
    idea = civic_app.ideas[-1]
    civic_app.fetch_relevant_breakthroughs(idea)
    return jsonify({'breakthroughs': idea.relevant_breakthroughs})

@app.route('/get_full_solution', methods=['POST'])
def get_full_solution():
    idea = civic_app.ideas[-1]
    civic_app.provide_full_solution(idea)
    return jsonify({'solution': idea.full_solution})

@app.route('/generate_report', methods=['POST'])
def generate_report():
    idea = civic_app.ideas[-1]
    idea_data = {
        'description': idea.description,
        'city': idea.city,
        'country': idea.country,
        'refined_details': idea.refined_details,
        'global_examples': idea.global_examples,
        'local_feasibility': idea.local_feasibility,
        'relevant_breakthroughs': idea.relevant_breakthroughs,
        'full_solution': idea.full_solution
    }
    try:
        html_content = generate_html_report(idea_data, api_key)
        filename = f"report_{idea.city}_{idea.country}.html"
        with open(filename, 'w') as f:
            f.write(html_content)
        return jsonify({'success': True, 'filename': filename})
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})



@app.route('/download_report/<filename>')
def download_report(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)