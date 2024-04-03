# Flask endpoint that combines both analysis and explanation generation
@app.route('/analyze-page', methods=['POST'])
def analyze_page():
    data = request.json
    file_path = data.get('file_path')
    selected_page = data.get('selected_page')  # Make sure you handle page selection appropriately.

    # Perform the analysis to get the improved code
    improved_html_content, suggestions = analyze_code(file_path, selected_page)
    
    # Generate explanations for each improvement
    explanations = explain_code_changes(suggestions)

    # Return both the improved code and the explanations
    return jsonify({
        'improved_html': improved_html_content,
        'suggestions': suggestions,
        'explanations': explanations
    })
