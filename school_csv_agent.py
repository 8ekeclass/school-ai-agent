import os
import pandas as pd
from google import genai
from google.genai import types

def load_school_data(csv_path):
    """Φορτώνει το αρχείο CSV και επιστρέφει μια κειμενική σύνοψη των δεδομένων."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Το αρχείο {csv_path} δεν βρέθηκε.")
    
    # Διάβασμα του CSV
    df = pd.read_csv(csv_path)
    
    # Μετατροπή των δεδομένων σε κείμενο (Markdown) για να τα καταλάβει το Gemini
    data_summary = df.to_markdown(index=False)
    return data_summary

def ask_school_agent(prompt, csv_data):
    """Στέλνει τα δεδομένα του σχολείου και την ερώτηση στο Gemini API."""
    # Ανάκτηση του API Key από το περιβάλλον (ή τοποθέτησέ το απευθείας εδώ αν προτιμάς)
    # π.χ. client = genai.Client(api_key="ΤΟ_API_KEY_ΣΟΥ")
    client = genai.Client(AQ.Ab8RN6KcfKUmpgydwsSgWnNt7-4bhd-3okEAfCd6yzHjGUbS2g)

    # Ορισμός των οδηγιών συστήματος για να συμπεριφέρεται ως σχολικός βοηθός
    system_instruction = (
        "Είσαι ένας έμπειρος σχολικός βοηθός δεδομένων (School CSV Agent). "
        "Σου παρέχονται δεδομένα μαθητών/βαθμολογιών σε μορφή πίνακα. "
        "Απάντησε στις ερωτήσεις του χρήστη με ακρίβεια, βασιζόμενος αποκλειστικά στα δεδομένα που βλέπεις."
    )

    # Κατασκευή του τελικού μηνύματος που περιλαμβάνει τα δεδομένα και την ερώτηση
    full_content = f"Ακολουθούν τα σχολικά δεδομένα:\n\n{csv_data}\n\nΕρώτηση χρήστη: {prompt}"

    # Κλήση του μοντέλου Gemini 2.5 Flash (το προτεινόμενο για γενικές εργασίες κειμένου)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=full_content,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2, # Χαμηλό temperature για μεγαλύτερη ακρίβεια στα δεδομένα
        ),
    )
    
    return response.text

if __name__ == "__main__":
    # Πριν τρέξεις το αρχείο, σιγουρέψου ότι έχεις ορίσει το API Key στο τερματικό σου:
    # export GEMINI_API_KEY="το_κλειδί_σου" (για Mac/Linux)
    # set GEMINI_API_KEY="το_κλειδί_σου" (για Windows CMD)
    
    # Όνομα του CSV αρχείου σου (άλλαξέ το αν έχεις διαφορετικό όνομα αρχείου)
    CSV_FILE = "school_data.csv"
    
    try:
        print("Φόρτωση σχολικών δεδομένων...")
        school_data = load_school_data(CSV_FILE)
        
        print("\nΟ School CSV Agent είναι έτοιμος! Πληκτρολογήστε 'exit' για έξοδο.")
        while True:
            user_question = input("\nΡωτήστε κάτι για τα σχολικά δεδομένα: ")
            if user_question.lower() == 'exit':
                break
                
            if not user_question.strip():
                continue
                
            print("Σκέφτομαι...")
            answer = ask_school_agent(user_question, school_data)
            print(f"\nΑπάντηση Agent:\n{answer}")
            
    except FileNotFoundError:
        print(f"\n[Σφάλμα]: Παρακαλώ δημιουργήστε ένα αρχείο με όνομα '{CSV_FILE}' στον ίδιο φάκελο.")
        # Παράδειγμα περιεχομένου για το CSV
        print("Παράδειγμα δομής CSV (Όνομα,Τμήμα,Βαθμός,Απουσίες):")
        print("Γιώργος Παπαδόπουλος,Α1,18.5,2\nΜαρία Κωνσταντίνου,Α1,19.2,0")
    except Exception as e:
        print(f"\nΠροέκυψε σφάλμα: {e}")
