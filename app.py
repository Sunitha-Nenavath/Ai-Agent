from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -----------------------------
# Career Recommendation API
# -----------------------------


@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.json
    career = data["career"].lower()

    recommendations = {
        "software engineer": [
            "Learn Programming Basics",
            "Practice Data Structures",
            "Build Real World Projects",
            "Learn System Design",
            "Practice Coding Interviews",
        ],
        "ai engineer": [
            "Learn Python",
            "Study Machine Learning",
            "Learn Deep Learning",
            "Work on AI Projects",
            "Learn TensorFlow / PyTorch",
        ],
        "data scientist": [
            "Learn Python",
            "Learn Statistics",
            "Learn Machine Learning",
            "Practice Data Analysis",
            "Build ML Projects",
        ],
        "data analyst": [
            "Learn Excel",
            "Learn SQL",
            "Learn Python for Data Analysis",
            "Learn Power BI / Tableau",
            "Practice Data Visualization",
        ],
        "devops engineer": [
            "Learn Linux",
            "Learn Docker",
            "Learn Kubernetes",
            "Learn CI/CD Pipelines",
            "Learn AWS / Azure",
        ],
        "system architect": [
            "Learn System Design",
            "Learn Cloud Architecture",
            "Learn Distributed Systems",
            "Learn Microservices",
            "Study High Scalability Systems",
        ],
    }

    result = recommendations.get(career, ["No recommendation found for this career"])

    return jsonify({"skills": result})


# -----------------------------
# AI Career Mentor API
# -----------------------------


@app.route("/mentor", methods=["POST"])
def mentor():

    data = request.json
    question = data["question"].lower()

    if "software engineer" in question:
        answer = "To become a software engineer learn programming languages like Java or Python, master data structures, and build real projects."

    elif "ai engineer" in question:
        answer = "To become an AI engineer learn Python, Machine Learning, Deep Learning, and build AI projects using TensorFlow or PyTorch."

    elif "data scientist" in question:
        answer = "To become a data scientist learn Python, statistics, machine learning, and practice data analysis with real datasets."

    else:
        answer = "Focus on learning programming, building projects, and improving problem solving skills."

    return jsonify({"answer": answer})


# -----------------------------
# Resume Upload API
# -----------------------------


@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return jsonify({"message": "No file uploaded"})

    file = request.files["resume"]

    return jsonify({"message": "Resume uploaded successfully"})


# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
