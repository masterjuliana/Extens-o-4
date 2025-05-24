import PyPDF2
import re  # Para expressões regulares (se necessário)

def extract_questions_from_pdf(pdf_path):
    questions = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""  # Extrai o texto da página

    # Dividir o texto em blocos que parecem perguntas e respostas
    blocks = re.split(r'(\n\d+\n.*?)\n\d+\n', text) # Tentativa de separar por numeração

    for i in range(1, len(blocks), 2):
      question_text = blocks[i].strip()
      answer_text = blocks[i+1].strip() if i + 1 < len(blocks) else "Resposta não encontrada"
      questions.append({'question': question_text, 'correct_answer': answer_text})
    return questions

pdf_path = 'perguntas-e-respostas-sobre-hidraulica.pdf'
extracted_questions = extract_questions_from_pdf(pdf_path)

for q in extracted_questions:
    print(q)