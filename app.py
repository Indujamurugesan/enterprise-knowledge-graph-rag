import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from generate_answer import generate_answer
from ingest_document import ingest_document
from document_processor import extract_text
from entity_extractor import extract_and_store


# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)

CORS(app)


# ==========================================
# Upload Configuration
# ==========================================

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "txt"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ==========================================
# Check File Type
# ==========================================

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================
# Health Check
# ==========================================

@app.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify({
        "status": "online",
        "message": "Enterprise RAG API is running"
    })


# ==========================================
# Ask Question
# ==========================================

@app.route(
    "/ask",
    methods=["POST"]
)
def ask():

    data = request.get_json()

    question = data.get(
        "question",
        ""
    ).strip()


    if not question:

        return jsonify({
            "error": "Question is required"
        }), 400


    try:

        answer = generate_answer(
            question
        )

        return jsonify({
            "question": question,
            "answer": answer
        })


    except Exception as error:

        print(
            "❌ ASK ERROR:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# ==========================================
# Upload + Process Document
# ==========================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_document():

    # --------------------------------------
    # Check file
    # --------------------------------------

    if "file" not in request.files:

        return jsonify({
            "error": "No file uploaded"
        }), 400


    file = request.files["file"]


    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400


    if not allowed_file(
        file.filename
    ):

        return jsonify({
            "error": "Only PDF and TXT files are allowed"
        }), 400


    try:

        # ----------------------------------
        # Save file
        # ----------------------------------

        filename = os.path.basename(
            file.filename
        )

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(
            file_path
        )


        print()
        print("=" * 50)
        print("📄 DOCUMENT UPLOADED")
        print("=" * 50)

        print(
            f"📁 File: {filename}"
        )


        # ----------------------------------
        # Extract text
        # ----------------------------------

        text = extract_text(
            file_path
        )

        print(
            f"✅ Extracted {len(text)} characters"
        )


        if not text.strip():

            return jsonify({
                "error": "No text found in document"
            }), 400


        # ----------------------------------
        # Store chunks in ChromaDB
        # ----------------------------------

        chunk_count = ingest_document(
            file_path
        )


        # ----------------------------------
        # Extract entities
        # ----------------------------------

        extract_and_store(
            text
        )


        # ----------------------------------
        # Success
        # ----------------------------------

        print()
        print(
            "🎉 DOCUMENT PROCESSING COMPLETE"
        )


        return jsonify({

            "message":
                "Document uploaded and processed successfully",

            "filename":
                filename,

            "characters":
                len(text),

            "chunks":
                chunk_count,

            "status":
                "processed"
        })


    except Exception as error:

        print()
        print(
            "❌ DOCUMENT PROCESSING ERROR:"
        )

        print(error)


        return jsonify({
            "error": str(error)
        }), 500


# ==========================================
# Start Server
# ==========================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print("🚀 Enterprise Knowledge RAG API")
    print("=" * 50)
    print(
        "🌐 Server: http://127.0.0.1:5000"
    )
    print("=" * 50)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )