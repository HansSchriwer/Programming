# Let's focus on integrating the machine learning model for action classification and the priority scoring system, as these can significantly enhance the email analysis without requiring external setup (like email client integration or GUI).
Here's an expanded version of our code incorporating these features:

import email
import re
from email.header import decode_header
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Existing functions (decode_email_subject, read_email, preprocess_text, extract_important_info, extract_dates)
# ... (keep these as they were in the previous version)

# New function for training the action classifier
def train_action_classifier(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    text_clf = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB()),
    ])
    
    text_clf.fit(X_train, y_train)
    
    print(f"Model accuracy: {text_clf.score(X_test, y_test):.2f}")
    
    return text_clf

# Sample training data (in a real scenario, you'd have much more data)
X = [
    "Urgent meeting tomorrow to discuss project deadlines",
    "Please review the attached document and provide feedback",
    "Invitation: Team building event next Friday",
    "Question about the new software implementation",
    "Action required: Sign off on the budget proposal",
    "FYI: Weekly project status update"
]
y = [
    "Schedule meeting",
    "Review document",
    "RSVP to event",
    "Respond to question",
    "Approval required",
    "For information"
]

# Train the model
action_classifier = train_action_classifier(X, y)

def determine_action(subject, body, entities, top_words):
    combined_text = subject + " " + body
    ml_action = action_classifier.predict([combined_text])[0]
    
    # We'll use the ML prediction as the primary action,
    # but we'll also keep our rule-based system as a fallback
    urgent_words = set(['urgent', 'important', 'asap', 'deadline'])
    action_words = set(['action', 'required', 'needed', 'necessary'])
    question_words = set(['question', 'query', 'clarification', 'help'])
    meeting_words = set(['meeting', 'conference', 'discussion', 'call'])
    
    if any(word in subject.lower() for word in urgent_words):
        return "Urgent: " + ml_action
    elif any(word in subject.lower() for word in action_words) or any(word[0] in action_words for word in top_words):
        return "Action Required: " + ml_action
    else:
        return ml_action

def calculate_priority(subject, sender, body, entities, top_words):
    score = 0
    
    # Check for urgent words in subject
    urgent_words = set(['urgent', 'important', 'asap', 'deadline'])
    if any(word in subject.lower() for word in urgent_words):
        score += 10
    
    # Check sender importance (you'd need to maintain a list of important senders)
    important_senders = ["boss@company.com", "client@bigclient.com"]
    if sender in important_senders:
        score += 5
    
    # Check for deadline mentions
    if any(ent[1] == 'DATE' for ent in entities):
        score += 3
    
    # Check for action words
    action_words = set(['action', 'required', 'needed', 'necessary'])
    if any(word[0] in action_words for word in top_words):
        score += 2
    
    # Classify priority based on score
    if score >= 15:
        return "High", score
    elif score >= 8:
        return "Medium", score
    else:
        return "Low", score

def analyze_email(email_content):
    subject, body = read_email(email_content)
    preprocessed_body = preprocess_text(body)
    entities, top_words, key_sentences = extract_important_info(preprocessed_body)
    dates = extract_dates(preprocessed_body)
    action = determine_action(subject, preprocessed_body, entities, top_words)
    
    # For the priority calculation, we'd normally get the sender from the email headers
    # Here, we'll just use a placeholder
    sender = "example@email.com"
    priority, priority_score = calculate_priority(subject, sender, preprocessed_body, entities, top_words)
    
    print(f"Subject: {subject}")
    print(f"\nPriority: {priority} (Score: {priority_score})")
    print("\nImportant entities:")
    for entity, label in entities:
        print(f"- {entity} ({label})")
    print("\nTop words:")
    for word, count in top_words:
        print(f"- {word}: {count}")
    print("\nKey sentences:")
    for sentence in key_sentences[:3]:  # Limit to top 3 sentences
        print(f"- {sentence}")
    if dates:
        print("\nDates mentioned:")
        for date in dates:
            print(f"- {date}")
    print(f"\nRecommended action: {action}")

# Example usage
email_content = """
Subject: Urgent: Project deadline approaching

Hello team,

I hope this email finds you well. I wanted to remind everyone that our project deadline is coming up next week on July 15th, 2024. We need to schedule a meeting to discuss the final details and ensure everything is on track.

Please let me know your availability for a meeting tomorrow or the day after. It's crucial that we address any remaining issues and questions before the deadline.

Best regards,
John Smith
Project Manager
"""

analyze_email(email_content)
Key improvements in this version:
1.	Machine Learning Action Classification: 
o	We've added a simple text classification model using scikit-learn.
o	The train_action_classifier function prepares and trains the model.
o	In a real-world scenario, you'd want a much larger training dataset and might consider more advanced models like BERT or other transformer-based models for better accuracy.
2.	Enhanced Action Determination: 
o	The determine_action function now uses the ML model as its primary method for determining the action.
o	It still incorporates some rule-based logic to add context (like "Urgent" or "Action Required") to the ML prediction when appropriate.
3.	Priority Scoring: 
o	The calculate_priority function assigns a numerical score based on various factors.
o	It then classifies the email as High, Medium, or Low priority based on this score.
o	This helps quickly identify which emails need immediate attention.
4.	Integrated Analysis: 
o	The analyze_email function now includes the priority calculation and displays this information in its output.
To further improve this system, you could consider:
1.	Regularly retraining the ML model with new data to improve its accuracy over time.
2.	Implementing a feedback mechanism where users can correct misclassifications, which could be used to improve the model.
3.	Fine-tuning the priority scoring system based on user feedback and specific organizational needs.
4.	Adding more features to the ML model, such as sender information, time of day, or historical interaction data.
5.	Implementing named entity recognition to better identify and categorize important information in the emails.

### Remember, when dealing with emails, it's crucial to handle data privacy and security carefully. Ensure you have the necessary permissions and security measures in place when implementing such a system in a real-world environment.

